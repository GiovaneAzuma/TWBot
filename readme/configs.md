# Manual de Configuração
Arquivo de ajuda para definir o seu arquivo de configuração personalizado.
## Server
**Username e senha**
Podem ser fornecidos para ‘login’ automático, não sendo necessários se has_recaptcha estiver habilitado ou se uma ‘string’ de ‘cookie’ for fornecida.

**Endpoint, Servidor e World**
Estas são as primeiras partes do URL onde o seu jogo TW está localizado. O Endpoint deve começar com "https://" e terminar em "game.php". Servidor e World correspondem ao servidor em que você está a jogar, sendo geralmente a primeira parte do URL após "https://".

**Has Re-capcha**
Isso não está relacionado à proteção contra ‘bots’ no jogo, apenas informa ao ‘script’ que o procedimento de ‘login’ regular deve ser ignorado e uma ‘string’ de ‘cookie’ deve ser usada.

**Servidor on TWStats**
Se o mundo do jogo ainda não estiver disponível em [https://br.twstats.com/](https://br.twstats.com/), defina como false. Isso buscará automaticamente dados relacionados ao mundo, como a população necessária para certos edifícios.

## Bot
Essa seção configura funcionalidades que não estão relacionadas ao jogo.
**Active Hours**
Define as horas em que o ‘bot’ deve estar ativo. O padrão é das 6h da manhã às 23h da noite. O horário será definido com base no seu fuso horário atual. Caso o seu fuso horário seja diferente do jogo, inclua a diferença de tempo!
**Active Delay, Inactive Delay e Inactive Still Active**
Active Delay configura o tempo mínimo que o ‘bot’ aguardará até a próxima execução durante as horas ativas. Inactive Delay faz o mesmo para as horas inativas. Se inactive_still_active estiver desativado, o ‘bot’ será completamente desligado durante as horas inativas e desconectará provavelmente a sua sessão, exigindo que você reinicie o ‘bot’ manualmente pela manhã.

## Notifications
As notificações, quando habilitadas, enviam mensagens para um canal no Telegram.

### Setup
Para enviar mensagens para um canal no Telegram, você precisará criar um ‘bot’ primeiro. Para isso, inicie uma conversa com o [BotFather](https://t.me/botfather) e crie um ‘bot’ (/newbot). Após criar o ‘bot’, você receberá um token, que deve ser adicionado ao parâmetro "notifications.token" no arquivo de configuração.

Depois, crie um canal e adicione o ‘bot’ como administrador. Envie uma mensagem para o canal e encaminhe-a para o [JsonDumpBot](https://t.me/JsonDumpBot) para obter o forward_origin.chat.id. Adicione este ‘ID’ ao parâmetro "notifications.channel_id" no arquivo de configuração.

Não se esqueça de habilitar o parâmetro "notifications.enabled" no arquivo de configuração.

## Building
O booleano manage_building pode desativar a construção globalmente, para que você não precise reconfigurar manualmente todas as suas aldeias.
**‘Default’**
Define o modelo de construção padrão. Um dos modelos recomendados é o purple_predator, mas modelos personalizados podem ser fornecidos na pasta builder modelos.

**Max Look-ahead**
Número máximo de construções na fila que serão verificadas caso as anteriores falhem (como falta de recursos ou requisitos não atendidos). Recomenda-se manter este número abaixo de 5 para evitar filas com as construções mais baratas primeiro.

**Max Queued ‘Items’**
Número de itens que podem ser enfileirados simultaneamente, padrão: 2. Contas de luxo podem ter mais, mas isso não é recomendado.

## Units
Configura como as unidades devem ser treinadas. Com a opção recruit ativada, as aldeias começarão automaticamente a produzir unidades após a conclusão do quartel. Inicialmente, serão criadas apenas algumas unidades para iniciar o procedimento de farm até que o quartel atinja um nível mais alto.

Modelos de unidades podem ser configurados na pasta troops modelo. As unidades são configuradas de cima para baixo, e o modelo mais baixo com o requisito de construção atendido será selecionado como o atual.

O modelo atual também define quais e quantas unidades de farm serão usadas pela session de farm.

**Upgrading**
Se "upgrade" estiver habilitado, o ‘script’ pesquisará automaticamente as unidades listadas no modelo atual. Isso suporta os dois sistemas de ‘upgrade’ e pesquisará automaticamente tudo (níveis 0-1, 0-3, 0-10) se houver tempo e recursos suficientes. ‘Upgrades’ de nível mais alto podem levar tempo, pois os recursos são geralmente gastos pelo construtor e recrutador.

**Batch size**
Quantidade de unidades que o ‘script’ tentará recrutar de uma só vez. Para estágios avançados do jogo (quartel nível 25+), é sugerido algo entre 500-1500. Para estágios iniciais, valores menores permitirão mais variação.
Nota: O tamanho do lote será sempre o máximo possível de unidades numa tentativa. Se os recursos forem insuficientes, o ‘script’ calculará o número mínimo de unidades possíveis.

## Farms
Configura as opções de farm para todas as aldeias. Cada aldeia atacará automaticamente aldeias bárbaras próximas. Se houver espiões disponíveis, a aldeia será espionada primeiro. Caso não haja tropas ou a muralha esteja no nível zero, ela será adicionada a listar farms.
Se não houver espiões ou eles ainda não estiverem pesquisados, o ‘script’ enviará um único ataque. Se retornar sem perdas, a aldeia será adicionada a listar farms.

Por padrão, o ‘script’ prioriza quantidade em vez de recursos, já que outros jogadores também podem estar a atacar a aldeia. Os parâmetros "default_away_time" e "full_loot_away_time" configuram os tempos de espera para atacar novamente aldeias de prioridade normal e alta, respetivamente.

## Market
A funcionalidade de mercado gerencia automaticamente os recursos da sua aldeia. Isso é especialmente útil quando o construtor está com poucos recursos específicos.
O parâmetro "max_trade_duration" configura o tempo máximo de negociação em horas. Recomenda-se manter este valor baixo para garantir que os recursos sejam trocados rapidamente e de forma eficiente.

**Trading frequency**
O trader removerá automaticamente itens listados por mais de "max_trade_duration" horas. Para negociações personalizadas, desative a opção "auto_remove".

**Trade multiplier**
Se o seu mundo não permitir trocas desiguais, desative esta opção. Por padrão, está configurado em 0,9, o que significa trocará 900 pedras por 1000 madeiras se 1000 forem solicitados pelo construtor. Recomenda-se manter o multiplicador abaixo de 1,0 para evitar prejuízos.

## World options
Atualmente, apenas o "quests_enabled" está a funcionar. Ele completa automaticamente as missões assim que os requisitos são atendidos. Quando isso acontece, o ‘script’ reinicia a execução atual para a aldeia, pois pode haver recompensas de recursos associadas à missão.

# Village configuration
Configura como as aldeias serão gerenciadas. Tanto a construção quanto as unidades podem sobrescrever as opções globais de modelo. Para que o ‘bot’ pule (temporariamente) a aldeia, desative a opção "managed".

**Building priority**
Quando "prioritize_building" estiver habilitado, o recrutador criará unidades apenas quando os itens enfileirados atingirem o valor "max_queued_items" definido.

**‘Snob’ priority**
Reservará recursos para a criação de ‘snobs’, e apenas o construtor terá prioridade mais alta. Também requisitará recursos do mercado para criação de moedas e ‘snobs’. O número de ‘snobs’ que podem ser criados numa aldeia pode ser configurado com o parâmetro "snobs".

**Custom farms**
Cada aldeia pode ter uma lista de farms personalizados no parâmetro "additional_farms", onde os ‘IDs’ das aldeias devem ser adicionados como ‘strings’.
*Nota: Esta opção pode ser perigosa! Se a aldeia for capturada por você ou outro jogador, o ‘bot’ continuará a atacar até que as tropas morram ou a entrada seja desativada no arquivo de cache da aldeia.*
