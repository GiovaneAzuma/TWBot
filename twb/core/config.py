import collections
import logging
import sys
from pathlib import Path

from twb.core.filemanager import FileManager


class ConfigManager:
    @staticmethod
    def load_config() -> collections.OrderedDict:
        config_template = (
            Path(__file__).resolve().parent.parent / "templates" / "config.example.json"
        )
        template = FileManager.load_json_file(config_template)

        # Verifica se o arquivo de configuração existe
        if not FileManager.path_exists(f"{Path.cwd()}/config.json"):
            if ConfigManager.manual_config():
                return ConfigManager.load_config()

            logging.error("Nenhum arquivo de configuração encontrado. Encerrando...")
            sys.exit(1)

        config = FileManager.load_json_file(
            f"{Path.cwd()}/config.json", object_pairs_hook=collections.OrderedDict
        )

        # Verifica se o arquivo de configuração está desatualizado e faz o merge
        if template and config["build"]["version"] != template["build"]["version"]:
            logging.warning(
                "Arquivo de configuração desatualizado encontrado, mesclando (cópia antiga salva como config.bak)\n"
                "Remova o arquivo config.example.json para desativar este comportamento"
            )
            FileManager.copy_file(
                f"{Path.cwd()}/config.json", f"{Path.cwd()}/config.bak"
            )

            config = ConfigManager.merge_configs(config, template)
            FileManager.save_json_file(config, f"{Path.cwd()}/config.json")

            logging.info("Novo arquivo de configuração implantado")

        return config

    @staticmethod
    def manual_config():
        logging.info(
            "Olá e bem-vindo! Parece que você ainda não possui um arquivo de configuração"
        )
        config_template = (
            Path(__file__).resolve().parent.parent / "templates" / "config.example.json"
        )
        if not FileManager.path_exists(config_template):
            logging.error(
                "Oh não, config.example.json e config.json não existem. Você quebrou algo, não foi?"
            )
            return False

        logging.info(
            "Por favor, insira o URL atual (logado) do mundo em que você está jogando (ou q para sair)."
            "O URL deve ser algo parecido com isso:\n"
            "https://nl01.tribalwars.nl/game.php?village=12345&screen=overview"
        )
        input_url = input("URL: ").strip()
        if input_url.strip() == "q":
            return False

        server = input_url.split("://")[1].split("/")[0]
        game_endpoint = input_url.split("?")[0]
        sub_parts = server.split(".")[0]

        logging.info("Endpoint do jogo: %s", game_endpoint)
        logging.info("Mundo: %s", sub_parts.upper())

        if input("Isso parece correto? [nS]").lower() != "s":
            logging.info(
                "Certifique-se de que seu URL começa com https:// e contém a parte game.php?"
            )
            return ConfigManager.manual_config()

        browser_ua = input(
            "Insira o user-agent do seu navegador (para reduzir taxas de detecção). Apenas pesquise 'qual é o meu user-agent'> "
        ).strip()
        if len(browser_ua) < 10:
            logging.error(
                "Deve começar com Chrome, Firefox ou algo similar. Por favor, tente novamente."
            )
            return ConfigManager.manual_config()

        disclaimer = """
        Leia com atenção: Por favor, note que o uso deste bot causar bans, expulsões, incômodos e outras consequências.
        Faço o meu melhor para tornar o bot mais indetectável possível, mas a maioria dos problemas/bans estão relacionados à configuração.
        Certifique-se de configurar pausa razoáveis para o bot e, por favor, não me culpe se sua conta for banida ;)
        PS: Certifique-se de, regularmente (1-2 vezes por dia), fazer logout/login usando a sessão do navegador e fornecer o novo cookie.
        Usar uma única sessão por 24 horas seguidas provavelmente resultará em um banimento.
        """
        logging.info(disclaimer)

        if (
            input(
                "Você entende isso e ainda deseja continuar? Por favor, digite sim e pressione Enter> "
            ).lower()
            != "sim"
        ):
            logging.info("Adeus :)")
            sys.exit(0)
        config_template = (
            Path(__file__).resolve().parent.parent / "templates" / "config.example.json"
        )
        template = FileManager.load_json_file(
            config_template, object_pairs_hook=collections.OrderedDict
        )
        if not template:
            logging.error("Não foi possível abrir o arquivo config.example.json")
            return False

        template["server"]["endpoint"] = game_endpoint
        template["server"]["server"] = sub_parts.lower()
        template["bot"]["user_agent"] = browser_ua

        FileManager.save_json_file(template, f"{Path.cwd()}/config.json")
        logging.info("Novo arquivo de configuração implantado")
        return True

    @staticmethod
    def merge_configs(old_config, new_config):
        # Mescla configurações antigas com novas
        to_ignore = ["villages", "build"]
        for section in old_config:
            if section not in to_ignore:
                for entry in old_config.get(section, {}):
                    if entry in new_config.get(section, {}):
                        new_config[section][entry] = old_config[section][entry]

        villages = collections.OrderedDict()
        for v in old_config["villages"]:
            nc = new_config["village_template"]
            vdata = old_config["villages"][v]
            for entry in nc:
                if entry not in vdata:
                    vdata[entry] = nc[entry]
            villages[v] = vdata
        new_config["villages"] = villages
        return new_config
