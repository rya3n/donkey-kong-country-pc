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
| 42185 | Mine Cart Carnage - J11 | Trecho repetido desde o menu (camera=6457, 5 vidas, 1 banana) |
| 43481 | Mine Cart Carnage - J22 | Metade da fase superada; vida extra acumulada (camera=11298, 6 vidas, 20 bananas) |
| 45086 | Mine Cart Carnage - J40 | Fim do trecho superior com trilhos quebrados (camera=16845, 6 vidas, 37 bananas) |
| 45146 | Mine Cart Carnage - J41/J42 | Transferência calculada de trilhos: queda do trilho superior quebrado para o carrinho no trilho inferior |
| 45255 | Mine Cart Carnage - J44 | Penúltimo salto superado (camera=17557, 6 vidas, 37 bananas) |
| 45428 | Mine Cart Carnage - J45 | Salto final para a estrutura de saída (w=138, j=35) executado com sucesso |
| 45570 | Mine Cart Carnage concluída a partir de snapshot | Saída alcançada com 6 vidas e 37 bananas |
| 45804 | Retorno ao Mapa de Monkey Mines | Transição concluída para o mapa de Monkey Mines e deslocamento automático pela trilha do mapa |
| 45948 | Mapa diante de Bouncy Bonanza | Chegada reproduzida a partir do snapshot local de Mine Cart Carnage. A sequência integral precisa ser reconstruída |

O [roteiro público de 40.473 quadros](../recipes/usa-rev1/campaign-to-mine-cart-carnage.inputs) contém os comandos do controle desde o menu até o início de Mine Cart Carnage. Os primeiros 35.218 quadros geram o save da Candy e 37.620 chegam a Monkey Mines. O [roteiro ampliado](../recipes/usa-rev1/campaign-to-bouncy-bonanza.inputs) mantém esse trecho e segue até Bouncy Bonanza.

## Travessia dos 45 obstáculos de Mine Cart Carnage em QA

Os valores abaixo foram registrados durante a exploração com pontos de restauração. A tabela serve como referência para reconstruir uma sequência contínua a partir do início da fase.

| Salto | Espera (w) | Pulo (j) | Quadro final | Câmera | Vidas | Bananas | Observações |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1–9 | — | — | 41905 | — | 5 | — | Saltos iniciais de carrinho sobre fendas e Krashes |
| 10 | 160 | 10 | 42035 | — | 5 | — | Salto curto preventivo |
| 11 | 120 | 30 | 42185 | 6457 | 5 | 1 | Salto longo sobre fenda |
| 12 | 100 | 30 | 42315 | 6840 | 5 | 4 | Salto sobre carrinho em sentido contrário |
| 13 | 290 | 25 | 42630 | 8179 | 5 | 5 | Travessia longa em alta velocidade |
| 14 | 85 | 30 | 42745 | 8596 | 5 | 5 | Salto sobre abismo |
| 15 | 114 | 25 | 42884 | 8991 | 5 | 8 | Salto sobre obstáculo |
| 16 | 45 | 25 | 42954 | 9150 | 5 | 10 | Salto rápido em sequência |
| 17 | 75 | 25 | 43054 | 9417 | 5 | 12 | Salto sobre carrinho |
| 18 | 80 | 30 | 43164 | 9853 | 5 | 12 | Salto sobre abismo |
| 19 | 33 | 30 | 43227 | 10155 | 5 | 14 | Salto em sequência |
| 20 | 38 | 30 | 43295 | 10469 | 5 | 17 | Salto sobre carrinho |
| 21 | 40 | 20 | 43355 | 10746 | 5 | 20 | Salto de aproximação |
| 22 | 91 | 35 | 43481 | 11298 | 6 | 20 | Balão de 1-Up coletado (+1 vida) |
| 23 | 82 | 35 | 43598 | 11650 | 6 | 20 | Salto sobre trilho interrompido |
| 24 | 92 | 35 | 43725 | 12031 | 6 | 20 | Salto longo sobre grande vão |
| 25 | 99 | 35 | 43859 | 12450 | 6 | 20 | Salto sobre carrinho reverso |
| 26 | 145 | 35 | 44039 | 13190 | 6 | 20 | Salto de longo alcance |
| 27 | 4 | 35 | 44078 | 13347 | 6 | 20 | Pulo imediato após aterrissagem |
| 28 | 94 | 35 | 44207 | 13723 | 6 | 23 | Salto sobre fenda |
| 29 | 75 | 35 | 44317 | 14095 | 6 | 23 | Salto sobre obstáculo reverso |
| 30 | 33 | 35 | 44385 | 14319 | 6 | 25 | Salto rápido em sequência |
| 31 | 75 | 15 | 44475 | 14672 | 6 | 27 | Salto curto sob obstáculo aéreo |
| 32 | 27 | 35 | 44537 | 14937 | 6 | 32 | Salto longo sobre fenda |
| 33 | 21 | 35 | 44593 | 15188 | 6 | 32 | Salto rápido de transição |
| 34 | 20 | 35 | 44648 | 15338 | 6 | 32 | Salto sobre carrinho |
| 35 | 43 | 35 | 44726 | 15594 | 6 | 32 | Salto longo |
| 36 | 5 | 25 | 44756 | 15675 | 6 | 32 | Salto rápido imediato |
| 37 | 35 | 35 | 44826 | 15912 | 6 | 34 | Salto sobre abismo |
| 38 | 70 | 35 | 44931 | 16216 | 6 | 37 | Salto longo |
| 39 | 34 | 35 | 45000 | 16467 | 6 | 37 | Salto sobre fenda |
| 40 | 51 | 35 | 45086 | 16845 | 6 | 37 | Salto para início do trilho quebrado |
| 41 | 10 | 20 | 45116 | — | 6 | 37 | Queda calculada do trilho quebrado |
| 42 | 10 | 20 | 45146 | — | 6 | 37 | Aterrissagem no carrinho do trilho inferior |
| 43 | 38 | 20 | 45204 | 17354 | 6 | 37 | Salto de manutenção no trilho inferior |
| 44 | 16 | 35 | 45255 | 17557 | 6 | 37 | Penúltimo salto longo |
| 45 | 138 | 35 | 45428 | 18315 | 6 | 37 | Salto final do carrinho para a caverna de saída |

## Validação de persistência a frio (Cold Save)

O script `cold_save.py` foi executado sobre o perfil de teste gerado pela campanha (`evidence/2026-11-10/pt-BR/campaign-start/gemini-clean-cold-report`), executando o executável headless e o aplicativo desktop Win32:

1. **Arquivo SRAM:** `saves/save.srm` com exatamente 2.048 bytes e dados de progresso válidos (`sram_sha256`: `72d519d25cce21886142567427185942b8f2480ee9c7f0a7d912730830ea3207`).
2. **Backup automático:** `saves/save.srm.bak` gerado na inicialização subsequente com hash idêntico ao original.
3. **Retorno ao ponto salvo:** Após selecionar o slot, o quadro 4.801 do boot frio mostra os Kongs na Candy. O arquivo foi carregado do disco e permaneceu idêntico após a execução.
4. **Coincidência Headless vs Desktop Win32:** Hashes de framebuffer (`7eea6811...`), WRAM (`14c7629c...`) e SRAM (`72d519d2...`) rigorosamente idênticos entre os ambientes.

## Retomar em Mine Cart Carnage

Execute da raiz do projeto, com o piloto PT-BR compilado e a ROM Rev 1 local, em um PowerShell sem opções de diagnóstico do jogo.

```powershell
$qa = New-Item -ItemType Directory -Path 'evidence/replay-mine-cart-carnage' -ErrorAction Stop
$previousSaveDir = $env:DKC_REV1_SAVE_DIR
$env:DKC_REV1_SAVE_DIR = $qa.FullName
try {
    & '.\build\ptbr-pilot\dkc_rev1_headless.exe' `
        '.\Donkey Kong Country (USA) (Rev 1).sfc' 40473 `
        (Join-Path $qa.FullName 'mine-cart-carnage') `
        '.\recipes\usa-rev1\campaign-to-mine-cart-carnage.inputs'
    if ($LASTEXITCODE -ne 0) { throw "Replay falhou com código $LASTEXITCODE" }
} finally {
    $env:DKC_REV1_SAVE_DIR = $previousSaveDir
}
```

O roteiro local de 45.948 quadros reproduziu os hashes registrados em `acd5d06`. No rastreio quadro a quadro, o salto 11 foi reproduzido em 42.185, com câmera 6.457 e cinco vidas. O roteiro perdeu uma vida no quadro 43.907. A captura final mostrou a área inicial de Mine Cart Carnage e o runner informou `entrance=46` (`0x002E`). A chegada a Bouncy Bonanza veio de uma execução com o snapshot `minecart_j44.snap` no quadro 45.255. A revisão repetiu essa execução e confirmou o mapa diante de Bouncy Bonanza em 45.948 e a entrada na fase em 46.239.

## Roteiro contínuo até Bouncy Bonanza

O novo roteiro preserva os comandos até o quadro 43.725. A partir daí, o primeiro salto ajustado espera 119 quadros e mantém B por 35. Os saltos seguintes foram alinhados pela posição da câmera, incluindo a transferência para o trilho inferior. O rastreio registra a entrada com quatro vidas e a coleta de uma vida extra no quadro 42.113. Nenhuma vida foi perdida na fase.

| Quadro | Resultado |
| --- | --- |
| 43945 | Carrinho inimigo ultrapassado, com câmera em 12.631 |
| 45284 | Transferência para o trilho inferior concluída, com câmera em 17.553 |
| 45981 | Mapa de Monkey Mines diante de Bouncy Bonanza, `entrance=0x0007` |
| 46272 | Bouncy Bonanza aberta, `entrance=0x0007`, `scene=0x0001`, cinco vidas e 40 bananas |

Para reproduzir desde o menu, use o mesmo comando da seção anterior com um perfil de teste novo, o [roteiro de Bouncy Bonanza](../recipes/usa-rev1/campaign-to-bouncy-bonanza.inputs) e 46.272 quadros. Para conferir o mapa, use 45.981 quadros em outro perfil novo. O teste usa a ROM USA v1.1 (Rev 1) e o piloto PT-BR.

O piloto headless e o coletor de QA repetiram os 46.272 quadros em perfis novos, sem carregar snapshots. As capturas finais PPM foram idênticas. No relatório do piloto, o SHA-256 do framebuffer é `269096de8875fa231a28dd3cc10aa8290fc2aaa7dd64098585c98c91d2959867`. Os 59 testes Python passaram.

## Saída de Bouncy Bonanza

O [roteiro de 50.529 quadros](../recipes/usa-rev1/campaign-to-stop-and-go-station-map.inputs) continua a partir da entrada registrada no quadro 46.272. A rota segue pelo túnel inferior, usa os pneus para passar pelos Zingers e cruza a plataforma móvel antes da placa de saída. A exploração usou snapshots para testar os saltos. As verificações finais começaram no menu em perfis novos e usaram apenas comandos do controle.

| Quadro | Resultado |
| --- | --- |
| 47601 | Zinger na região do barril de checkpoint ultrapassado |
| 47896 | Travessia do túnel inferior |
| 48911 | Chegada à plataforma após os dois primeiros pneus da sequência final |
| 49424 | Último grupo de Zingers ultrapassado |
| 49939 | Placa de saída visível |
| 50529 | Mapa de Monkey Mines com Stop & Go Station selecionada, `entrance=0x0031` |

O rastreio registra cinco vidas durante toda a fase. O piloto headless e o coletor de QA geraram capturas finais idênticas. O SHA-256 do framebuffer no relatório do piloto é `38f2bbff2765052d78197c186ac5a57b0e41191c544fc3226e230597b18611dd`. Os 59 testes Python passaram.

Para reproduzir, use o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com um perfil de teste novo, 50.529 quadros e o roteiro de Stop & Go Station. O marco final é a seleção no mapa. A próxima etapa da campanha começa pela entrada na fase.

## Saída de Stop & Go Station

O [roteiro de 55.451 quadros](../recipes/usa-rev1/campaign-to-millstone-mayhem-map.inputs) parte do menu e mantém os comandos anteriores até o quadro 53.291. A nova sequência aciona o barril para parar os Rockkrocs, encadeia os saltos nos três apoios e ajusta a espera nas plataformas móveis. O roteiro retorna ao mapa sobre Stop & Go Station e segue à direita pelo ponto de Funky até Millstone Mayhem.

| Quadro | Resultado |
| --- | --- |
| 50820 | Stop & Go Station aberta, `entrance=0x0031` e `scene=0x0002` |
| 52474 | Plataforma vertical atravessada |
| 53367 | Barril acionado antes dos três apoios com Rockkrocs |
| 53666 | Travessia dos três apoios concluída |
| 54052 | Trecho das plataformas móveis concluído |
| 55149 | Mapa de Monkey Mines após a saída de Stop & Go Station |
| 55451 | Millstone Mayhem selecionada no mapa, `entrance=0x0042`, cinco vidas e 93 bananas |

O rastreio confirmou cinco vidas desde a entrada até a saída de Stop & Go Station. O piloto headless e o coletor de QA repetiram os 55.451 quadros desde o menu em perfis novos, sem restaurar snapshots. As capturas finais PPM foram idênticas. O SHA-256 do framebuffer no relatório do piloto é `c75034a68e48605b69bc2c13a18c1d45408e2ae945fd9e60954feccade4edd25`. Os 59 testes Python passaram.

Para repetir, use o mesmo comando de reprodução em um perfil novo, com 55.451 quadros e o roteiro de Millstone Mayhem. A próxima etapa começa pela entrada na fase.

## Saída de Millstone Mayhem

O [roteiro de 60.409 quadros](../recipes/usa-rev1/campaign-to-neckys-nuts-map.inputs) preserva os 55.451 quadros até o mapa de Millstone Mayhem. A sequência passa pelas mós e pelos Kritters, ativa o barril de checkpoint e ajusta a corrida e os saltos para atravessar os vãos. No último, Diddy ganha distância rolando antes de saltar. O mapa aparece com Cranky's Cabin selecionada. Um toque à direita seleciona Necky's Nuts, a fase de Master Necky.

| Quadro | Resultado |
| --- | --- |
| 55742 | Millstone Mayhem aberta, `entrance=0x0042` e `scene=0x0008` |
| 57308 | Sexta vida obtida ao completar 100 bananas |
| 57600 | Barril de checkpoint ativado |
| 58161 | Travessia do vão com a mó concluída |
| 59763 | Último vão ultrapassado |
| 59898 | Saída acionada |
| 60258 | Mapa de Monkey Mines com Cranky's Cabin selecionada, `entrance=0x00EF` |
| 60409 | Necky's Nuts selecionada no mapa, `entrance=0x00E1`, seis vidas e 10 bananas |

O piloto headless e o coletor de QA repetiram os 60.409 quadros desde o menu em perfis novos, sem restaurar snapshots. O registro de transições confirmou que a vida extra foi a única alteração de vidas na fase. As capturas finais PPM foram idênticas. O SHA-256 do framebuffer no relatório do piloto é `f6ba6755159572b4fdc1115dbd95a5f124b3b9549167e9627cf897b24a0b4f3f`. Os 59 testes Python passaram.

Para repetir, use o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com um perfil novo, 60.409 quadros e o roteiro de Necky's Nuts. O próximo teste começa no mapa, pela entrada no chefe.

## Master Necky e chegada a Vine Valley

O [roteiro de 62.704 quadros](../recipes/usa-rev1/campaign-to-vine-valley-map.inputs) mantém os comandos até o mapa de Necky's Nuts e acrescenta a luta contra Master Necky. A sequência usa o pneu para atingir o chefe nos dois lados da arena. Após a vitória e a animação da banana gigante, o mapa geral seleciona Vine Valley. Um toque em B abre o mapa desse mundo com Vulture Culture selecionada.

| Quadro | Resultado |
| --- | --- |
| 60650 | Arena de Necky's Nuts, `entrance=0x00E1`, `scene=0x000C`, seis vidas |
| 60714 | Primeiro golpe confirmado, com quatro golpes restantes |
| 61414 | Quarto golpe confirmado, com um golpe restante |
| 61601 | Último golpe visível |
| 61951 | Banana gigante e animação de vitória |
| 62463 | Vine Valley selecionado no mapa geral, `entrance=0x00E9` |
| 62704 | Vulture Culture selecionada no mapa de Vine Valley, `entrance=0x00A5`, seis vidas e 10 bananas |

O piloto headless e o coletor de QA repetiram os 62.704 quadros desde o menu em perfis novos, sem restaurar snapshots. O registro de transições confirmou seis vidas durante a luta e a saída de Monkey Mines. As capturas finais PPM foram idênticas. O SHA-256 do framebuffer no relatório do piloto é `97fa79dc94aa494e5c9e94c4147c387c52c09e43b6e845f1cc763caeef4bfea8`. Os 59 testes Python passaram.

Para repetir, use o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com um perfil novo, 62.704 quadros e o roteiro de Vine Valley. A próxima etapa começa pela entrada em Vulture Culture.

## Saída de Vulture Culture

O [roteiro de 68.009 quadros](../recipes/usa-rev1/campaign-to-tree-top-town-map.inputs) mantém os comandos até a seleção de Vulture Culture e percorre a rota principal da fase. A sequência ajusta o tempo dos disparos para atravessar os vãos e passar pelos abutres e Zingers. Após a saída, o mapa de Vine Valley seleciona Tree Top Town automaticamente.

| Quadro | Resultado |
| --- | --- |
| 62995 | Vulture Culture aberta, `entrance=0x00A5`, `scene=0x000B`, seis vidas |
| 64536 | Travessia do primeiro grupo de abutres |
| 65185 | Trecho do barril de parceiro ultrapassado |
| 65419 | Sequência de barris giratórios atravessada |
| 67123 | Travessia dos barris após a placa de saída em andamento |
| 67440 | Saída acionada |
| 68009 | Tree Top Town selecionada no mapa, `entrance=0x00A4`, seis vidas e 38 bananas |

O piloto headless e o coletor de QA repetiram os 68.009 quadros desde o menu em perfis novos, sem restaurar snapshots. O registro confirmou seis vidas durante toda a fase. As capturas finais PPM foram idênticas. O SHA-256 do framebuffer no relatório do piloto é `1ee95b1b54e313b8d54fd88986494d534fc392e2e9c52b9274b38aab423b009d`. Os 59 testes Python passaram.

Para repetir, use o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com um perfil novo, 68.009 quadros e o roteiro de Tree Top Town. O próximo teste começa pela entrada nessa fase.

## Saída de Tree Top Town

O [roteiro de 72.546 quadros](../recipes/usa-rev1/campaign-to-forest-frenzy-map.inputs) mantém os comandos até a seleção de Tree Top Town. A sequência atravessa as pontes com Kritters, acerta o tempo dos disparos nos barris móveis e usa o pneu para alcançar a plataforma da saída. O mapa de Vine Valley mantém Tree Top Town selecionada após a conclusão. Um toque para baixo seleciona Forest Frenzy.

| Quadro | Resultado |
| --- | --- |
| 68300 | Tree Top Town aberta, `entrance=0x00A4`, `scene=0x000A`, seis vidas |
| 69085 | Primeira ponte com Kritters atravessada |
| 69886 | Barril de checkpoint ativado |
| 71700 | Sequência final de barris verticais ultrapassada |
| 72065 | Saída acionada |
| 72395 | Mapa de Vine Valley com Tree Top Town selecionada após a saída |
| 72546 | Forest Frenzy selecionada, `entrance=0x00D0`, seis vidas e 52 bananas |

O piloto headless e o coletor de QA repetiram os 72.546 quadros desde o menu em perfis novos, sem restaurar snapshots. O registro confirmou seis vidas durante toda a fase. As capturas finais PPM foram idênticas. O SHA-256 do framebuffer no relatório do piloto é `5087e31f22a58dffc91f4b1f4256a614b087b7d0faebb319aab73efc817f290d`. Os 59 testes Python passaram.

Para repetir, use o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com um perfil novo, 72.546 quadros e o roteiro de Forest Frenzy. O próximo teste começa pela entrada nessa fase.

## Saída de Forest Frenzy

O [roteiro de 78.949 quadros](../recipes/usa-rev1/campaign-to-temple-tempest-map.inputs) mantém os comandos até Forest Frenzy no mapa e percorre a rota principal da fase. Os comandos de subida e descida ajustam a altura dos Kongs nas cordas móveis para passar pelos Zingers. Depois de cruzar o trecho dos abutres, a rota volta ao chão, passa pelos últimos Kritters e segue até o mapa de Vine Valley.

| Quadro | Resultado |
| --- | --- |
| 72837 | Forest Frenzy aberta, `entrance=0x00D0`, `scene=0x000B`, seis vidas |
| 73712 | Travessia pelas primeiras cordas concluída |
| 74963 | Barril de checkpoint ativado |
| 76051 | Chegada à plataforma após os Zingers amarelos |
| 77955 | Última corda, após o trecho dos abutres |
| 78599 | Saída em andamento |
| 78949 | Temple Tempest selecionada no mapa, `entrance=0x0043`, seis vidas e 82 bananas |

O piloto headless e o coletor de QA repetiram os 78.949 quadros desde o menu em perfis novos, sem restaurar snapshots. O registro confirmou seis vidas durante toda a fase. As capturas finais PPM foram idênticas. O SHA-256 do framebuffer no relatório do piloto é `ae2227d1e6312579fd9b7b729af7eb9f6c8d16c10fa6f71e519f480f3b519c23`. Os 59 testes Python passaram.

Para repetir, use o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com um perfil novo, 78.949 quadros e o roteiro de Temple Tempest. O próximo teste começa pela entrada nessa fase.

## Saída de Temple Tempest

O [roteiro de 84.234 quadros](../recipes/usa-rev1/campaign-to-orang-utan-gang-map.inputs) mantém os comandos até Temple Tempest no mapa. A rota principal passa pelas rodas dos Gnawtys, ativa o checkpoint e usa as cordas e os saltos nos pneus para cruzar os vãos. Depois da saída, o mapa de Vine Valley seleciona Candy’s Save Point. Um toque para a direita seleciona Orang-utan Gang.

| Quadro | Resultado |
| --- | --- |
| 79240 | Temple Tempest aberta, `entrance=0x0043`, `scene=0x0008`, seis vidas |
| 80207 | Segunda perseguição atravessada até a borda do vão |
| 81188 | Barril de checkpoint ativado |
| 81718 | Sétima vida obtida ao completar 100 bananas |
| 83181 | Travessia dos pneus no trecho dos Zingers concluída |
| 83613 | Últimas cordas atravessadas e placas de saída visíveis |
| 84083 | Retorno ao mapa com Candy’s Save Point selecionado, `entrance=0x00FF` |
| 84234 | Orang-utan Gang selecionada, `entrance=0x000D`, sete vidas e 13 bananas |

O piloto headless e o coletor de QA repetiram os 84.234 quadros desde o menu em perfis novos, sem restaurar snapshots. O registro confirmou que a vida extra foi a única alteração no contador de vidas da fase. As capturas finais PPM foram idênticas. O SHA-256 do framebuffer registrado pelo piloto é `6d06a350fa50985de66cd87f5052390cf6014580a794882123fe2ef4a718beb6`. Os 59 testes Python passaram.

Para repetir, use o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com um perfil novo, 84.234 quadros e o roteiro de Orang-utan Gang. O próximo teste começa pela entrada nessa fase.

## Saída de Orang-utan Gang

O [roteiro de 88.509 quadros](../recipes/usa-rev1/campaign-to-clam-city-map.inputs) mantém os comandos até Orang-utan Gang no mapa. Na rota principal da fase, os Kongs cruzam as copas e as pontes de cipó, ativam o checkpoint, passam pelos barris dos Manky Kongs e descem até a saída. O mapa de Vine Valley seleciona Cranky’s Cabin após a conclusão. Um toque para a esquerda seleciona Clam City.

| Quadro | Resultado |
| --- | --- |
| 84525 | Orang-utan Gang aberta, `entrance=0x000D`, `scene=0x0000`, sete vidas |
| 85194 | Primeiras pontes de cipó atravessadas |
| 85790 | Barril de checkpoint ativado |
| 85976 | Barril DK quebra e o parceiro retorna |
| 87360 | Últimas pontes atravessadas e trilha inferior alcançada |
| 87888 | Placa de saída visível |
| 88358 | Retorno ao mapa com Cranky’s Cabin selecionada, `entrance=0x00F3` |
| 88509 | Clam City selecionada, `entrance=0x00DE`, sete vidas e 37 bananas |

O piloto headless e o coletor de QA repetiram os 88.509 quadros desde o menu em perfis novos, sem restaurar snapshots. O registro confirmou sete vidas durante toda a fase. As capturas finais PPM foram idênticas. O SHA-256 do framebuffer registrado pelo piloto é `318f1f5b2a03bfc341104d315df53ee9dd3ae132091c245c45862caa85a515c5`. Os 59 testes Python passaram.

Para repetir, use o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com um perfil novo, 88.509 quadros e o roteiro de Clam City. O próximo teste começa pela entrada nessa fase.
