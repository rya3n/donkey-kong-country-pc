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

O [roteiro público de 40.473 quadros](../recipes/usa-rev1/campaign-to-mine-cart-carnage.inputs) contém os comandos do controle desde o menu até o início de Mine Cart Carnage. Os primeiros 35.218 quadros geram o save da Candy e 37.620 chegam a Monkey Mines.

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

Use os snapshots locais para consultar a exploração de Mine Cart Carnage e de Bouncy Bonanza. Para ampliar a rota validada, registre uma sequência contínua que chegue ao mapa de Monkey Mines após o carrinho e confirme o início de Bouncy Bonanza em novo perfil. Depois, conclua Bouncy Bonanza e as fases restantes. A validação da campanha, a escuta do áudio em janela, a revisão dos textos restantes e o aplicativo final seguem na [matriz de validação](05-VALIDACAO.md).
