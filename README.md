# Tribal Wars Bot (TWB)
## Um bot de código aberto para o jogo Tribal Wars

## Aviso de atualização 2.0.2
Simplificação do projeto. Renomeado para TWBot. Mais informações e ‘download’ disponíveis no [PyPi]

[PyPi]: https://pypi.org/project/TWBot/

## Um Exemplo Simples

```python
# salve isso como app.py
from twb.bot import TWB


def main():
    TWB(config_path="config.json").run()


if __name__ == "__main__":
    main()
```

Nós também criamos um servidor no [Discord](https://discord.gg/8PuzHjttMy) para que você possa buscar ajuda com outros usuários.

*Funcionalidades:*
- Modo cooperativo (você pode continuar jogando no navegador enquanto o bot gerencia tarefas em segundo plano)
- Gerenciamento de construções
- Gerenciamento de defesa
- Gerenciamento de tropas
- Gerenciamento de bandeiras
- Adição automática de aldeias conquistadas
- Gerenciamento de farms
- Gerenciamento do mercado
- Mercado premium (pontos premium gratuitos :D)
- Gerenciamento de pesquisas (incluindo sistemas de nível)
- Criação automática de nobres
- Gerenciamento de relatórios
- "Bypass" do ReCaptcha utilizando o cookie do navegador (o bot funciona se a sessão do navegador for válida)

*Como fazer:*
- Instale a library
- Execute usando o exemplo acima
- O arquivo de configuração padrão (config.json) será criado na inicialização
	- Adicione pelo menos o endpoint e o servidor
	- Altere a seção de configuração village_template de acordo com suas necessidades


- Inicie o bot executando python twb.py e forneça o cookie com suas necessidades
- Se o login funcionar, você pode ajustar o arquivo config.json conforme necessário; ele será recarregado automaticamente quando alterado.
- Suas aldeias serão adicionadas automaticamente ao arquivo de configuração. Desative o parâmetro "managed" para que o bot pule a aldeia.
- Propriedades adicionais podem ser ajustadas executando o script manager.py.
- Você pode querer configurar o user-agent do bot no arquivo core/request.py com o seu próprio user-agent. Provavelmente não perceberão, mas é melhor prevenir. :)

Você pode encontrar o valor do cookie na seguinte localização (Chrome):

![Screenshot](readme/network.JPG)

Você precisa usar o valor do cabeçalho cookie:.

*Opcional: Se tudo estiver configurado corretamente e o bot estiver rodando, você pode usar o comando cd para entrar no diretório webmanager e iniciar a interface do bot executando server.py. Você pode acessar este dashboard visitando http://127.0.0.1:5000/ no navegador. Muitas novas funcionalidades serão adicionadas ao dashboard em breve.*

Mais informações sobre a configuração do bot podem ser encontradas no diretório readme!
