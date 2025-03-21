# Manual de Configuração
Arquivo de ajuda para definir o seu arquivo de configuração personalizado.

## Servidor
**Username e Senha**
A partir da versão 1.2, isso não é mais necessário, já que o ‘login’ está protegido por um captcha.

**Endpoint, Servidor e World**
Estes são as primeiras partes da URL onde o seu jogo TW está localizado. O **Endpoint** deve começar com "https://" e terminar com "game.php". **Servidor** e **World** representam o servidor no qual você está a jogar, sendo geralmente a primeira parte da URL após "https://".

**Has Re-capcha**
Isso não está relacionado à proteção contra ‘bots’ do jogo. Apenas informa ao ‘script’ que o procedimento de ‘login’ regular deve ser ignorado e uma ‘string’ de ‘cookie’ será solicitada.

**Servidor on TWStats**
Se o mundo do seu jogo ainda não estiver disponível em [https://br.twstats.com/](https://br.twstats.com/), configure como **false**. Isso buscará automaticamente dados relacionados ao mundo, como a população necessária para certos edifícios.

## Registry Remoto
O ‘bot’ possui um recurso de registry remoto usando **MySQL** e arquivos.
Por padrão, cada início (execução de `twb.py`) cria um arquivo de ‘log’ baseado no timestamp atual.
Para registrar no **MySQL**, é necessário fornecer uma ‘string’ de conexão como:
`mysql://username:password@hostname:3306/database_name`
Ele deve criar automaticamente as tabelas necessárias, caso ainda não existam.

## Bot
Configura funcionalidades não relacionadas diretamente ao jogo.

**Active Hours**
Define as horas em que o ‘bot’ deve estar ativo. O padrão é das 6h da manhã às 23h da noite. O horário será ajustado para o seu fuso horário atual, então, se o fuso do jogo for diferente, ajuste a diferença!

**Active Delay, Inactive Delay e Inactive Still Active**
- **Active Delay**: Tempo mínimo que o ‘bot’ deve esperar entre execuções durante horas ativas.
- **Inactive Delay**: Configura o mesmo para horas inativas.
- **Inactive Still Active**: Se desativado, o ‘bot’ será completamente desligado durante horas inativas, possivelmente fazendo timeout da sessão.

**Forced Peace Times**
Array de horários em que ataques não podem ser realizados (ex.: natal). Deve ser configurado assim:
```json
[{"start:": "%d.%m.%y %H:%M:%S", "end":"%d.%m.%y %H:%M:%S"}, {"start:": "24.12.2001 17:00:00", "end":"27.12.2001 01:00:00"}]
```

## Construção
- **manage_building**: desativa globalmente a construção, evitando a necessidade de reconfigurar manualmente todas as vilas.
- **‘Default’**: define o modelo padrão de construção (ex.: "purple_predator"). Modelos personalizados podem ser adicionados na pasta de modelos do builder.
- **Max Look-ahead**: Número máximo de edifícios na fila a serem verificados se os anteriores falharem (ex.: falta de recursos). Recomenda-se manter abaixo de 5.
- **Max Queued Items**: Número de itens que podem ser enfileirados simultaneamente (padrão: 2).

## Unidades
Configura como as unidades serão treinadas:
- **recruit**: Vilas começam a produzir unidades automaticamente ao concluir quartéis.
- **Upgrading**: Quando habilitado, o script pesquisará automaticamente as unidades no modelo atual, incluindo ‘upgrades’ de nível.
- **Batch size**: Quantidade de unidades a serem recrutadas por vez. Para quartéis de nível alto (25+), sugere-se algo entre 500-1500.

## Farms
Configura as opções de farming:
- Ataca automaticamente vilas bárbaras próximas.
- Se espiões estiverem disponíveis, a vila será analisada antes do ataque.
- **default_away_time**: tempo (em segundos) antes de atacar novamente a mesma vila.

## Mercado
Gerencia automaticamente os recursos da vila:
- **max_trade_duration**: tempo máximo de negociação (em horas).
- **trade_multiplier**: Fator de troca (ex.: 0.9 significa 900 pedra para 1000 madeira).

## Opções do Mundo
- **quests_enabled**: Conclui automaticamente as missões ao atender os requisitos.

## Configuração de Vilas
Gerencia como as vilas são administradas.
- **Building Priority**: Dá prioridade à construção relativamente ao recrutamento.
- **‘Snob’ Priority**: Reserva recursos para criação de nobres.
- **Custom Farms**: Lista de farms personalizados para cada vila (‘IDs’ das vilas devem ser ‘strings’).
- **Gathering**: Habilita operações de coleta se as tropas não estiverem a ser usadas para farming.