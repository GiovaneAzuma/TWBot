"""
Arquivo usado para extração de dados
"""

import json
import re
from typing import Any, Dict, List
from requests.models import Response


class Extractor:
    """
    Define vários regexes não compilados para recuperação de dados.
    TODO: usar regexes compilados para eficiência de CPU.
    """

    @staticmethod
    def village_data(res):
        """
        Detecta dados da vila em uma página
        """
        if not isinstance(res, str):
            res = res.text
        grabber = re.search(r"var village = (.+);", res)
        if grabber:
            data = grabber.group(1)
            return json.loads(data, strict=False)

    @staticmethod
    def game_state(res: Response) -> Dict[str, Any]:
        """
        Detecta o estado do jogo que está disponível na maioria das páginas
        """
        if not isinstance(res, str):
            res = res.text
        grabber = re.search(r"TribalWars\.updateGameData\((.+?)\);", res)
        if grabber:
            data = grabber.group(1)
            return json.loads(data, strict=False)

    @staticmethod
    def building_data(res):
        """
        Obtém dados de construção do prédio principal
        """
        if not isinstance(res, str):
            res = res.text
        dre = re.search(r"(?s)BuildingMain.buildings = (\{.+?});", res)
        if dre:
            return json.loads(dre.group(1), strict=False)

        return None

    @staticmethod
    def get_quests(res):
        """
        Obtém dados de missões em quase todas as páginas
        """
        if not isinstance(res, str):
            res = res.text
        get_quests = re.search(r"Quests.setQuestData\((\{.+?})\);", res)
        if get_quests:
            result = json.loads(get_quests.group(1), strict=False)
            for quest in result:
                data = result[quest]
                if data["goals_completed"] == data["goals_total"]:
                    return quest
        return None

    @staticmethod
    def get_quest_rewards(res):
        """
        Detecta se há recompensas disponíveis para missões
        """
        if not isinstance(res, str):
            res = res.text
        get_rewards = re.search(r"RewardSystem\.setRewards\(\s*(\[\{.+?}]),", res)
        rewards = []
        if get_rewards:
            result = json.loads(get_rewards.group(1), strict=False)
            for reward in result:
                if reward["status"] == "unlocked":
                    rewards.append(reward)
        # Retorne todos eles
        return rewards

    @staticmethod
    def map_data(res):
        """
        Detecta outras vilas na página do mapa
        """
        if not isinstance(res, str):
            res = res.text
        data = re.search(r"(?s)TWMap.sectorPrefech = (\[(.+?)]);", res)
        if data:
            result = json.loads(data.group(1), strict=False)
            return result

    @staticmethod
    def smith_data(res):
        """
        Obtém dados de ferreiro
        """
        if not isinstance(res, str):
            res = res.text
        data = re.search(r"(?s)BuildingSmith.techs = (\{.+?});", res)
        if data:
            result = json.loads(data.group(1), strict=False)
            return result
        return None

    @staticmethod
    def premium_data(res):
        """
        Detecta dados na página de câmbio premium
        """
        if not isinstance(res, str):
            res = res.text
        data = re.search(r"(?s)PremiumExchange.receiveData\((.+?)\);", res)
        if data:
            result = json.loads(data.group(1), strict=False)
            return result
        return None

    @staticmethod
    def recruit_data(res):
        """
        Obtém dados de recrutamento para o prédio atual
        """
        if not isinstance(res, str):
            res = res.text
        data = re.search(r"(?s)unit_managers.units = (\{.+?});", res)
        if data:
            raw = data.group(1)
            quote_keys_regex = r"([\{\s,])(\w+)(:)"
            processed = re.sub(quote_keys_regex, r'\1"\2"\3', raw)
            result = json.loads(processed, strict=False)
            return result

    @staticmethod
    def units_in_village(res):
        """
        Detecta todas as unidades na vila
        """
        if not isinstance(res, str):
            res = res.text
        matches = re.search(r'<table id="units_home".*?</tr>(.*?)</tr>', res, re.DOTALL)
        # Nós obtemos o início da tabela e pegamos a segunda linha (onde estão localizadas as tropas "Desta vila")
        if matches:
            table_content = matches.group(1)
            unit_matches = re.findall(
                r"class=\'unit-item unit-item-(.*?)\'[^>]*>(\d+)</td>", table_content
            )
            # Encontre todas as tuplas (nome, quantidade) dentro da classe "unit-item unit-item-*troop-name*"
            units = [
                (re.sub(r"\s*tooltip\s*", "", unit_name), unit_quantity)
                for unit_name, unit_quantity in unit_matches
                if int(unit_quantity) > 0
            ]
            # Filtre as unidades com quantidade = 0, além disso, para o Paladino,
            # o nome seria "knight tooltip", então tivemos que remover isso.
            return units
        return []

    @staticmethod
    def active_building_queue(res):
        """
        Detecta entradas na fila de construção
        """
        if not isinstance(res, str):
            res = res.text
        builder = re.search('(?s)<table id="build_queue"(.+?)</table>', res)
        if not builder:
            return 0

        return builder.group(1).count('<a class="btn btn-cancel"')

    @staticmethod
    def active_recruit_queue(res):
        """
        Detecta entradas ativas de recrutamento
        """
        if not isinstance(res, str):
            res = res.text
        builder = re.findall(r"(?s)TrainOverview\.cancelOrder\((\d+)\)", res)
        return builder

    @staticmethod
    def village_ids_from_overview(res: str) -> List[str]:
        """
        Obtém vilas a partir da visão geral
        """
        if not isinstance(res, str):
            res = res.text
        villages = re.findall(r'<span class="quickedit-vn" data-id="(\w+)"', res)
        return list(set(villages))

    @staticmethod
    def units_in_total(res):
        """
        Obtém o total de unidades em uma vila
        """
        if not isinstance(res, str):
            res = res.text
        # Oculte as unidades de outras aldeias
        res = re.sub(r'(?s)<span class="village_anchor.+?</tr>', "", res)
        data = re.findall(
            r"(?s)class=\Wunit-item unit-item-([a-z]+)\W.+?(\d+)</td>", res
        )
        return data

    @staticmethod
    def attack_form(res):
        """
        Detecta campos de entrada no formulário de ataque
        ... porque há muitas :)
        """
        if not isinstance(res, str):
            res = res.text
        data = re.findall(r'(?s)<input.+?name="(.+?)".+?value="(.*?)"', res)
        return data

    @staticmethod
    def attack_duration(res):
        """
        Detecta a duração de um ataque
        """
        if not isinstance(res, str):
            res = res.text
        data = re.search(r'<span class="relative_time" data-duration="(\d+)"', res)
        if data:
            return int(data.group(1))
        return 0

    @staticmethod
    def report_table(res):
        """
        Obtém informações de um relatório
        """
        if not isinstance(res, str):
            res = res.text
        data = re.findall(r'(?s)class="report-link" data-id="(\d+)"', res)
        return data

    @staticmethod
    def get_daily_reward(res):
        """
        Detecta se há recompensas diárias não coletadas
        """
        if not isinstance(res, str):
            res = res.text
        get_daily = re.search(r"DailyBonus.init\((\s+\{.*}),", res)
        res = json.loads(get_daily.group(1))
        reward_count_unlocked = str(res["reward_count_unlocked"])
        if (
            reward_count_unlocked
            and res["chests"][reward_count_unlocked]["is_collected"]
        ):
            return reward_count_unlocked
        return None
