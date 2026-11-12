# Áudio e progresso na campanha PT-BR

Sessão de 2026-11-10 em Windows, com o piloto de 217 diálogos e a ROM USA Rev 1. A comparação de áudio repetiu os 15.354 quadros do [primeiro percurso](31-INICIO-CAMPANHA-PT-BR.md).

Sessão continuada em 2026-11-11 em Windows, com o piloto de 217 diálogos e a ROM USA Rev 1. A fase Barrel Cannon Canyon foi concluída, Candy's Save Point foi visitado via navegação normal no mapa, e o teste de salvamento e persistência a frio foi validado com sucesso.

## Áudio da cabana até a caverna

O coletor local gravou o PCM estéreo de 16 bits a 32.040 Hz, quadro a quadro, nos builds inglês e PT-BR. Os hashes finais coincidiram com os de cada executável headless original. Os dois builds produziram o mesmo número de amostras por quadro.

| Quadros | Resultado da comparação |
| --- | --- |
| 1–14449 | PCM idêntico até o trecho da despedida do Cranky |
| 14450–14453 | Primeira diferença. Desvio máximo de três unidades da escala PCM de 16 bits |
| 14493–14987 | Diferença após a despedida, durante o retorno ao mapa e a transição para Reptile Rumble. O quadro 14493 é o único com amostras não nulas em apenas um dos builds |
| 15038–15354 | Diferença durante o início da caverna. Ainda não foi medido onde os dois PCM voltam a coincidir |

Os intervalos omitidos até o quadro 15354 coincidiram. Em janelas amostradas no mapa e na entrada da caverna, um deslocamento de 31 a 53 amostras, cerca de 1 a 2 ms, voltou a alinhar os sinais com correlação acima de 0,98. O deslocamento variou ao longo do percurso.

O teste em janela reproduziu 1.902 quadros após preparar o estado do mapa diante da cabana. O dispositivo abriu e o host encerrou com código 0, sem registrar falha na submissão do PCM. Os bytes enviados à API de áudio foram idênticos aos produzidos no headless PT-BR. O framebuffer e a WRAM finais também coincidiram.

| Intervalo entre apresentações | Resultado |
| --- | --- |
| Mediana | 16,63 ms |
| Percentil 95 | 18,73 ms |
| Maior intervalo | 43,19 ms |
| Quadros que ultrapassaram o prazo do host | 10 de 1.902 |

O executável de QA adicionou leitura do roteiro e captura de PCM ao host Win32. O teste mede a saída do aplicativo para a API de áudio. A escuta no dispositivo e o efeito perceptível da diferença ainda precisam de confirmação.

## Progressão pelo mapa

| Quadro | Cenário | Resultado |
| --- | --- | --- |
| 18113 | Reptile Rumble | Caverna concluída sem perda de vidas e retorno ao mapa |
| 24912 | Coral Capers | Fase concluída. Enguarde, checkpoint e subida pelos corredores aquáticos exercitados |
| 25589 | Funky's Flights | Visita pelo mapa. A fala do Jumbo Barrel exibiu “vocês” com o `ê` legível e alinhado ao tamanho das demais letras |
| 34466 | Barrel Cannon Canyon | Fase concluída sem perda de vidas (4 vidas preservadas). Sequências de canhões móveis e obstáculos de chão superados até a caverna de saída |
| 34818 | Candy's Save Point | Visita via navegação no mapa. Diálogo de Candy em PT-BR exibido e legível |
| 35218 | Candy Save (SRAM) | Salto no barril de salvar executado. Gravação da bateria `save.srm` confirmada (2.048 bytes, SHA-256: `72d519d2...`) |
| 35700 | Very Gnawty's Lair | Entrada na arena do chefe (entrance=00e0, scene=000c, 4 vidas) |
| 36510 | Very Gnawty derrotado | 5 golpes consecutivos desferidos com Donkey Kong sem sofrer dano. Salto evasivo executado sobre a carga mortal no quadro 36.570 |
| 36870 | Coleta da banana gigante | Banana gigante recolhida, disparo da fanfarra de vitória de fim de mundo |
| 37241 | Transição Ilha -> Monkey Mines | Mapa geral da ilha (entrance=00ec) concluído e entrada no Mundo 2: Monkey Mines (entrance=00ed) |
| 37620 | Mapa de Monkey Mines | Posição estabilizada no mapa do Mundo 2 com 4 vidas preservadas e 55 bananas |
| 37651 | Entrada Winky's Walkway | Botão B pressionado no mapa, entrada na fase (entrance=00d9, scene=000c -> 0006) |
| 39069 | Winky's Walkway - Plataformas | Travessia de abismos e plataformas elevadas com salto duplo e evasão de Zingers |
| 39268 | Winky's Walkway - Neckys | Sequência aérea sobre Neckys e plataformas suspensas concluída com sucesso |
| 39558 | Winky's Walkway - Topo | Rolo sobre Kritter no chão e salto sobre a borda final pousando no andaime superior |
| 39757 | Winky's Walkway Concluída | Salto para a rampa diagonal final, coleta de bananas e acionamento do barril de saída (4 vidas intactas, 72 bananas) |
| 39997 | Retorno ao Mapa | Dança da vitória do Diddy, fanfarra, fade-out e retorno ao mapa de Monkey Mines (entrance=002e, scene=0006) |
| 40092 | Trilha do Mapa | Deslocamento automático dos Kongs pela trilha do mapa concluído no ponto de Mine Cart Carnage |
| 40178 | Entrada Mine Cart Carnage | Botão B pressionado no quadro 40.093, fade-in concluído e fase carregada (entrance=002e, scene=0005, camera=17) |
| 40473 | Mine Cart Carnage - Início | Posição pronta na fase do carrinho de mina com 4 vidas preservadas e 72 bananas acumuladas |

O roteiro usa os comandos do controle desde o menu (`evidence/2026-11-10/pt-BR/campaign-start/campaign-to-mine-cart-carnage.inputs`). A rota inteira (40.473 quadros) pode ser reproduzida a partir de um perfil vazio desde o cold boot, gerando o arquivo de salvamento idêntico e avançando pelas fases de forma 100% determinística.

## Validação de persistência a frio (Cold Save)

O script `cold_save.py` foi executado sobre o perfil de teste gerado pela campanha (`evidence/2026-11-10/pt-BR/campaign-start/gemini-clean-cold-report`), executando o executável headless e o aplicativo desktop Win32:

1. **Arquivo SRAM:** `saves/save.srm` com exatamente 2.048 bytes e dados de progresso válidos (`sram_sha256`: `72d519d25cce21886142567427185942b8f2480ee9c7f0a7d912730830ea3207`).
2. **Backup automático:** `saves/save.srm.bak` gerado na inicialização subsequente com hash idêntico ao original.
3. **Menu File Select:** O carregamento da tela de seleção de arquivos (quadro 4.801 do boot frio) exibiu o primeiro arquivo com o progresso real acumulado.
4. **Coincidência Headless vs Desktop Win32:** Hashes de framebuffer (`7eea6811...`), WRAM (`14c7629c...`) e SRAM (`72d519d2...`) rigorosamente idênticos entre os ambientes.
