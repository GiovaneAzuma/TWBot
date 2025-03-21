# How-to  
Arquivo de ajuda para explicar o fluxo de trabalho do bot  

### Novo jogador  
O ‘bot’ deve funcionar a partir do momento em que você entra num mundo pela primeira vez.  
Ele irá automaticamente construir os primeiros prédios e completar as primeiras quests (se habilitadas).  
Quando o barracks for construído, o processo de recrutamento deverá começar.  
Assim que as primeiras unidades de **spear** começarem a ser treinadas, o processo de **farm** também deverá ser iniciado automaticamente.  

Com o tempo, o ‘bot’ também começará a determinar quais unidades pesquisar/atualizar.  

### Após algum tempo  
Se os prédios atingirem níveis mais altos, o ‘bot’ começará a criar negociações no **market**.  
Isso permite que o processo de construção continue a funcionar com alta eficiência.  

Sempre que o mundo tiver o sistema de "flags" habilitado, o ‘bot’ também tentará atualizar e configurar a **‘flag’** de "resource bonus" mais alta.  
Nesse ponto, o sistema de ajuste de **farming** (`manager.py`) deverá ser capaz de detetar quais farms têm os maiores/menores ganhos de recursos e ajustará automaticamente os parâmetros das vilas.  

### Após mais algum tempo  
Você chegará ao ponto em que outros jogadores poderão atacá-lo.  
Eles podem pensar que a sua vila é um alvo fácil, mas com os parâmetros corretos configurados, você terá um exército ótimo.  

Sempre que um ataque for detetado, o ‘bot’ interromperá o processo de **farming** e configurará automaticamente a **‘flag’** de "defence bonus" mais alta.  
Unidades valiosas (ou defensivas fracas) serão evacuadas caso você tenha mais de uma vila.  

Se o ‘bot’ também tiver a opção `manage_defence` habilitada, ele enviará unidades defensivas como suporte.  
Essa parte pode ser configurada por vila.  

### Meio/Fim de jogo  
Quando você alcançar o estágio em que o **‘snob’** for construído, você poderá configurar o parâmetro `snob` na vila como `1`.  
Isso iniciará a criação das moedas necessárias e treinará um **‘snob’**.  

Se você quiser testar algo experimental, pode configurar a configuração atual de **farm** para incluir um **‘snob’**.  
Isso começará, lentamente, a conquistar todas as vilas de farm ao redor :)  

Quando mais vilas forem adquiridas, você poderá configurar o ‘bot’ para copiar automaticamente a configuração existente para as novas vilas.  
De preferência, configure-as manualmente, já que você provavelmente desejará ajustar alguns detalhes.  

Também sugiro que você continue a jogar ocasionalmente usando a sessão no navegador.  
Você pode encontrar alguns **captcha's**, que o ‘bot’ não será capaz de resolver :)  

**Divirta-se!**
