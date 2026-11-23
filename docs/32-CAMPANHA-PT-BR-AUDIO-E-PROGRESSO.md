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

## Medição da sessão de áudio no Win32

Em 2026-11-22, o piloto PT-BR USA Rev 1 rodou no Windows 10 22H2 (build 19045) em perfis isolados, com salvamento desabilitado. O ensaio executou o host Win32 em duas rodadas para cada fase. Cada rodada observou 720 quadros com o personagem parado após 4.800 quadros de preparação. A cadência alvo do host era 60,0988 Hz.

O medidor do Windows foi associado ao PID do jogo. A sessão reportou dois canais e o ensaio coletou o pico geral da sessão, em escala de 0 a 1. A análise excluiu o primeiro segundo e o último meio segundo da série de leituras. [Medidores de pico do Windows](https://learn.microsoft.com/en-us/windows/win32/coreaudio/peak-meters)

| Fase | Rodada | Duração analisada | Leituras | Leituras com pico zero | Maior intervalo entre leituras |
| --- | --- | ---: | ---: | ---: | ---: |
| Jungle Hijinxs | 1 | 10,38 s | 667 | 0 | 27,82 ms |
| Jungle Hijinxs | 2 | 10,42 s | 671 | 0 | 16,55 ms |
| Reptile Rumble | 1 | 10,67 s | 686 | 0 | 31,80 ms |
| Reptile Rumble | 2 | 10,53 s | 674 | 0 | 33,20 ms |

Em todas as rodadas, a imagem final (framebuffer) e o estado da memória de trabalho (WRAM) coincidiram com o teste sem janela da mesma fase. A mediana do intervalo de apresentação ficou entre 16,64 e 16,67 ms. Em Reptile Rumble, o host registrou oito quadros acima do prazo na primeira rodada e seis na segunda. O maior intervalo de apresentação foi de 69,40 ms.

As 2.698 leituras confirmam sinal na sessão de áudio do jogo nos trechos medidos. O ensaio usou leituras espaçadas, com o personagem parado. A escuta no dispositivo e a verificação de cortes audíveis ou distorções continuam pendentes. Os 59 testes da suíte Python passaram. As evidências locais estão em `evidence/2026-11-22/audio-win32/`. [Medição em movimento](#áudio-em-movimento-e-na-transição-para-a-caverna)

## Áudio em movimento e na transição para a caverna

Em 2026-11-22, uma compilação local de QA reproduziu trechos do [roteiro da campanha](../recipes/usa-rev1/campaign-to-ending-title.inputs) no host Win32. O teste avançou até o quadro inicial e executou cada trecho com cadência alvo de 60,0988 Hz e salvamento desabilitado. Registrou se cada bloco PCM tinha amostras não nulas antes de ser enviado ao Windows, além dos picos da sessão do próprio processo. Os timestamps usam o mesmo contador de alta resolução. A análise descartou 250 ms de cada ponta do intervalo em comum. [Medidor do Windows](https://learn.microsoft.com/en-us/windows/win32/api/endpointvolume/nf-endpointvolume-iaudiometerinformation-getpeakvalue)

| Trecho e quadros da campanha | Rodada | Leituras | Leituras de pico zero | Maior intervalo entre apresentações do host |
| --- | --- | ---: | ---: | ---: |
| Jungle Hijinxs, 5.341–6.200 | 1 | 879 | 25 | 31,85 ms |
| Jungle Hijinxs, 5.341–6.200 | 2 | 875 | 24 | 22,84 ms |
| Jungle Hijinxs, extensão até 6.400 | 1 | 1.093 | 97 | 27,80 ms |
| Cabana, mapa e Reptile Rumble, 14.401–15.850 | 1 | 1.506 | 85 | 29,53 ms |
| Cabana, mapa e Reptile Rumble, 14.401–15.850 | 2 | 1.611 | 172 | 1.489,64 ms |
| Cabana, mapa e Reptile Rumble, 14.401–15.850 | 3 | 1.504 | 84 | 25,42 ms |

As pausas do PCM nos quadros 5.998–6.025, 14.454–14.493 e 14.988–15.037 se repetiram. O primeiro pico zero de cada grupo correspondente chegou entre 109 e 130 ms após o início do PCM silencioso. A extensão em Jungle Hijinxs também registrou a volta do áudio após a pausa dos quadros 6.197–6.237. Os seis ensaios abriram a sessão estéreo, concluíram a sequência e reproduziram os códigos de cena da V13, além da imagem e da WRAM finais da execução sem janela.

Na segunda passagem pela caverna, houve uma interrupção adicional entre os quadros 15.739 e 15.740. O intervalo entre apresentações foi de 1.489,64 ms, com 1.483,37 ms decorridos antes do início do quadro seguinte e 6,18 ms de execução do núcleo. O medidor registrou 86 leituras consecutivas de pico zero, distribuídas por 1,33 s. O jogo gerou PCM ativo nos quadros imediatamente anterior e posterior. O áudio voltou durante a mesma rodada. O evento ocorreu em uma das três passagens e a causa segue em investigação.

O ensaio mediu a sessão Win32 com a janela oculta e registrou intervalos do host. A escuta no dispositivo em jogo segue pendente. Os 59 testes Python passaram. Os logs, o código local de QA e a comparação estão em `evidence/2026-11-22/audio-em-movimento/`.

### Repetição no piloto e diagnóstico da espera

Entre 2026-11-22 e 2026-11-23, o piloto PT-BR do jogador foi testado seis vezes a partir do atalho `--caverna`, com salvamento desabilitado e 17 s de comandos automatizados por rodada. Quatro rodadas usaram a janela oculta e duas usaram a janela visível. Três rodadas usaram o log de quadros. A cópia de teste tinha o mesmo SHA-256 do executável do jogador (`537f4be9984d154d546819cbde14b69b939e994c156e0bf7ce7e611cc3042c83`).

As 6.239 leituras analisadas da sessão tiveram sinal. Nas três rodadas com log, o maior intervalo de apresentação do host foi de 36,01 ms. O atalho começa dentro da caverna. O roteiro completo da transição foi testado à parte com instrumentação de QA.

Duas novas passagens executaram os mesmos 1.450 quadros da cabana até Reptile Rumble. A instrumentação registrou separadamente o tempo gasto no relógio de quadros, na fila de áudio, na fila de mensagens e na gravação dos logs. O quadro 15.740 sucede o intervalo de 1,49 s registrado no ensaio anterior.

| Medição do host | Passagem 1 | Passagem 2 |
| --- | ---: | ---: |
| Intervalo de apresentação no quadro 15.740 | 18,31 ms | 14,76 ms |
| Maior intervalo de apresentação no trecho | 44,46 ms | 30,06 ms |
| Maior espera acumulada pelo relógio em um quadro | 17,64 ms | 16,98 ms |
| Maior tempo de gravação do log de quadros | 0,20 ms | 15,39 ms |
| Chamadas de espera por um slot de áudio | 0 | 0 |

Os dois replays recuperaram as pausas do PCM nos quadros 14.454–14.493 e 14.988–15.037. As cenas e os hashes de imagem e WRAM finais coincidiram com a referência sem janela. A interrupção longa permaneceu restrita à ocorrência anterior. O teste original registrava o tempo total entre quadros, e a causa dessa espera segue em investigação em DKC-BUG-5. A escuta no dispositivo continua pendente na V09.

Os 59 testes Python e os dois alvos do CTest passaram na configuração base e no piloto. As evidências locais do diagnóstico estão em `evidence/2026-11-22/diagnostico-caverna/`. A segunda tentativa instrumentada foi interrompida na preparação. As duas passagens completas estão em `trace-1-transition/` e `trace-3-transition/`.

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

## Visitas de serviço em Monkey Mines

Em 2026-11-23, o piloto PT-BR da USA Rev 1 foi testado em três visitas independentes. Cada desvio começou no mapa em Cranky's Cabin, quadro 60.258, com seis vidas e dez bananas. A rota de referência é o [roteiro até Necky's Nuts](../recipes/usa-rev1/campaign-to-neckys-nuts-map.inputs), executado até esse quadro.

| Visita | Quadros | O que foi confirmado |
| --- | --- | --- |
| Cranky's Cabin | 60.619–61.463 | Saudação, dica que preserva Winky e Barrel Cannon Canyon, instrução da tecla X e despedida em PT-BR. A última confirmação voltou ao mapa com a cabana selecionada (`0x00EF`). |
| Funky's Flights | 60.560–61.804 | Fala em PT-BR, acesso ao mapa aéreo, seleção de Kongo Jungle (`0x00EC`) e chegada ao mapa de Kongo Jungle com Jungle Hijinxs selecionada. |
| Candy's Save Point | 60.862–61.619 | Saudação em PT-BR, entrada no barril de save, seleção do slot 1 e retorno ao mapa (`0x00FB`). O título do menu de salvamento apareceu em inglês. |

O slot 1 gravou 2.048 bytes com SHA-256 `5c7a9c8dfa47e90b7ad018561764fdeaa18309883e4e24aa7ce522c49d7b27ce`. Um boot frio exibiu **00:11 e 10%** no menu, voltou ao ponto da Candy em Monkey Mines no quadro 2.400 e entrou na cabana no quadro 4.801, com a instrução de salvamento em PT-BR. Em outro perfil, o piloto sem janela carregou o mesmo slot e percorreu o mapa até **Necky's Nuts**. A arena de Master Necky abriu no quadro 3.446 (`entrance=0x00E1`, `scene=0x000C`). O save e o backup permaneceram idênticos à gravação da Candy.

O coletor repetiu o prefixo desde o menu em um perfil vazio e gerou um novo estado no quadro 60.258. Os desvios independentes a partir desse estado e do marco arquivado produziram 14 capturas correspondentes idênticas, três estados finais idênticos e a mesma SRAM em cada visita. A captura da reabertura na Candy também coincidiu entre o coletor e o executável sem janela. Os 59 testes Python passaram. Evidências locais em `evidence/2026-11-23/monkey-mines/`.

### Comandos dos desvios

Use os primeiros 60.258 quadros do roteiro até Necky's Nuts como prefixo em cada perfil de teste. Os dois comandos finais do roteiro original, direita e 150 quadros de espera, ficam após o ponto de partida dos desvios. A tabela usa máscaras hexadecimais, durações em quadros e parênteses para indicar grupos repetidos.

| Visita | Entradas após o quadro 60.258 |
| --- | --- |
| Cranky | `0001 1`, `0000 360`, quatro vezes (`0001 1`, `0000 210`) |
| Funky | Duas vezes (`0040 1`, `0000 150`), `0001 1`, `0000 360`, `0001 1`, `0000 250`, `0040 1`, `0000 330`, `0001 1`, `0000 300` |
| Candy | Três vezes (`0040 1`, `0000 150`), `0010 1`, `0000 150`, `0001 1`, `0000 260`, `0080 20`, `0081 30`, `0000 310`, `0001 1`, `0000 135` |

A reabertura da cabana usa [cold-load.inputs](../recipes/usa-rev1/cold-load.inputs) em um novo processo com o mesmo diretório de save. Para entrar na arena, execute os primeiros 2.400 quadros do roteiro frio, depois `0020 1`, `0000 150`, quatro vezes (`0080 1`, `0000 150`), `0001 1` e `0000 290`.

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

## Saída de Clam City

O [roteiro de 94.899 quadros](../recipes/usa-rev1/campaign-to-bumble-b-rumble-map.inputs) mantém os comandos até Clam City no mapa. A rota principal sobe pelo primeiro corredor, passa por ostras e cardumes, quebra dois barris DK e ativa o checkpoint. Depois de cruzar o trecho dos tubarões, os comandos ajustam a profundidade para passar pelos Croctopus e alcançar a saída subaquática. O mapa de Vine Valley seleciona Bumble B Rumble automaticamente.

| Quadro | Resultado |
| --- | --- |
| 88800 | Clam City aberta, `entrance=0x00DE`, `scene=0x0003`, sete vidas |
| 90302 | Cardume ultrapassado |
| 91237 | Segundo barril DK aberto no alto do corredor |
| 91916 | Barril de checkpoint ativado |
| 93270 | Travessia dos tubarões concluída e corredor superior alcançado |
| 93797 | Seta de saída visível |
| 94899 | Bumble B Rumble selecionada, `entrance=0x00E5`, sete vidas e 59 bananas |

O piloto headless e o coletor de QA repetiram os 94.899 quadros desde o menu em perfis novos, sem restaurar snapshots. O registro confirmou sete vidas durante toda a fase. As capturas finais PPM foram idênticas. O SHA-256 do framebuffer registrado pelo piloto é `b00f5ff62f8141ad9ba653f24b41bbf561529b2fef4885744d1030321429a28a`. Os 59 testes Python passaram.

Para repetir, use o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com um perfil novo, 94.899 quadros e o roteiro de Bumble B Rumble. O próximo teste começa pela entrada no chefe.

## Queen B. e chegada a Gorilla Glacier

O [roteiro de 98.224 quadros](../recipes/usa-rev1/campaign-to-gorilla-glacier-map.inputs) mantém os comandos até a seleção de Bumble B Rumble e acrescenta a luta contra Queen B. Os Kongs atravessam a arena durante as investidas da chefe e lançam os barris quando ela volta a ficar vulnerável. Após a vitória, um toque em B fecha a sequência da banana gigante e o mapa geral seleciona Gorilla Glacier. Outro toque em B abre o mapa do mundo com Snow Barrel Blast selecionada.

| Quadro | Resultado |
| --- | --- |
| 95060 | Arena de Bumble B Rumble, `entrance=0x00E5`, `scene=0x000C`, sete vidas |
| 95134 | Primeiro golpe confirmado, com quatro golpes restantes |
| 95631 | Segundo golpe confirmado, com três golpes restantes |
| 96133 | Terceiro golpe confirmado, com dois golpes restantes |
| 96666 | Quarto golpe confirmado, com um golpe restante |
| 97287 | Último golpe confirmado |
| 97417 | Banana gigante e animação de vitória |
| 97923 | Gorilla Glacier selecionado no mapa geral, `entrance=0x00E8` |
| 98224 | Snow Barrel Blast selecionada no mapa de Gorilla Glacier, `entrance=0x0024`, sete vidas e 59 bananas |

O piloto headless e o coletor de QA repetiram os 98.224 quadros desde o menu em perfis novos, sem restaurar snapshots. O registro confirmou sete vidas durante a luta e a transição. As capturas finais PPM foram idênticas. O SHA-256 do framebuffer registrado pelo piloto é `d1f768136cde67e731ff9f28a2ab1c81095d6d7971cb0126cf12cbcb62832359`. Os 59 testes Python passaram.

Para repetir, use o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com um perfil novo, 98.224 quadros e o roteiro de Gorilla Glacier. O próximo teste começa pela entrada em Snow Barrel Blast.

## Saída de Snow Barrel Blast

O [roteiro de 103.582 quadros](../recipes/usa-rev1/campaign-to-slipslide-ride-map.inputs) mantém os comandos até a abertura de Gorilla Glacier. Em Snow Barrel Blast, os Kongs passam pelos Neckys, atravessam as sequências de canhões e ativam o checkpoint sob a nevasca. Na sequência final, um disparo para baixo entra no atalho indicado pela dica do Cranky. As bananas do atalho rendem uma vida extra, e o percurso volta à encosta antes da saída. De volta ao mapa, um toque à direita seleciona Slipslide Ride. [Dicas de Gorilla Glacier](24-DICAS-GORILLA-GLACIER-PT-BR.md).

| Quadro | Resultado |
| --- | --- |
| 98450 | Snow Barrel Blast aberta, `entrance=0x0024`, `scene=0x0004`, sete vidas |
| 98627 | Primeiro canhão giratório alcançado |
| 101074 | Barril de checkpoint ativado sob a nevasca |
| 101329 | Segundo Kong recuperado pelo barril DK |
| 102136 | Atalho alcançado pelo disparo para baixo |
| 102221 | Vida extra registrada |
| 102676 | Desembarque na encosta final |
| 102863 | Placa de saída visível |
| 103316 | Retorno ao mapa de Gorilla Glacier |
| 103582 | Slipslide Ride selecionada, `entrance=0x006D`, oito vidas e 89 bananas |

O piloto headless e o coletor de QA repetiram os 103.582 quadros desde o menu em perfis novos, sem restaurar snapshots. O registro confirmou que a vida extra foi a única alteração no contador de vidas durante a fase. As capturas finais PPM foram idênticas. O SHA-256 do framebuffer registrado pelo piloto é `9e97b2a9f07e0f3d3d9df21ff477a7d05dce38544def0545733adc1ea5635265`. Os 59 testes Python passaram.

Para repetir, use o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com um perfil novo, 103.582 quadros e o roteiro de Slipslide Ride. O próximo teste começa pela entrada em Slipslide Ride.

## Saída de Slipslide Ride

O [roteiro de 109.605 quadros](../recipes/usa-rev1/campaign-to-ice-age-alley-map.inputs) mantém os comandos até o mapa de Slipslide Ride. A fase alterna subidas em cordas azuis, descidas em cordas roxas e saltos para contornar os Zingers. A rota ativa o checkpoint após três cordas, recupera Donkey no barril DK e usa o canhão automático para alcançar a passagem superior. Perto da saída, Diddy sobe com 16 saltos alternados entre duas cordas roxas. O mapa seleciona Ice Age Alley automaticamente depois da saída.

| Quadro | Resultado |
| --- | --- |
| 103808 | Slipslide Ride aberta, `entrance=0x006D`, `scene=0x0009`, oito vidas |
| 104525 | Primeira descida na corda roxa |
| 104918 | Vida extra registrada após completar 100 bananas |
| 105996 | Barril de checkpoint ativado |
| 106171 | Donkey recuperado no barril DK |
| 106382 | Passagem superior alcançada pelo canhão automático |
| 106759 | Travessia das quatro cordas azuis concluída |
| 107182 | Plataforma da letra N alcançada |
| 108874 | Topo da subida final alcançado |
| 109391 | Ice Age Alley selecionada automaticamente no mapa |
| 109605 | Mapa de Gorilla Glacier estabilizado, `entrance=0x00A7`, nove vidas e 57 bananas |

O piloto headless e o coletor de QA repetiram os 109.605 quadros desde o menu em perfis novos, sem restaurar snapshots. O registro confirmou que a vida extra foi a única alteração no contador de vidas durante a fase. As capturas finais PPM foram idênticas. O SHA-256 do framebuffer registrado pelo piloto é `b100aada153ead145a468d5b49f1194942365a3303b311f7889cc44b5d9327fb`. Os 59 testes Python passaram.

Para repetir, use o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com um perfil novo, 109.605 quadros e o roteiro de Ice Age Alley. O próximo teste começa pela entrada em Ice Age Alley.

## Saída de Ice Age Alley

O [roteiro de 114.560 quadros](../recipes/usa-rev1/campaign-to-croctopus-chase-map.inputs) mantém os comandos até o mapa de Ice Age Alley. Os Kongs buscam Expresso à esquerda da entrada e atravessam o primeiro vão com ele. Depois de desmontar, a rota usa o barril DK para recuperar Donkey, cruza as cordas e ativa o checkpoint. O canhão automático leva à margem seguinte. Mais à frente, o salto do pneu alcança outra corda. Donkey cruza os últimos vãos e Diddy passa pelo Klaptrap final depois do encontro com o último Manky Kong. O mapa seleciona Croctopus Chase automaticamente depois da saída.

| Quadro | Resultado |
| --- | --- |
| 109831 | Ice Age Alley aberta, `entrance=0x00A7`, `scene=0x0004`, nove vidas |
| 110089 | Expresso montado |
| 110676 | Travessia do vão com Neckys concluída |
| 110948 | Donkey recuperado no barril DK |
| 111380 | Terceira corda antes do checkpoint alcançada |
| 111746 | Barril de checkpoint ativado |
| 111793 | Margem seguinte alcançada pelo canhão automático |
| 112403 | Corda alcançada com o salto do pneu |
| 113334 | Última corda alcançada com Donkey |
| 113852 | Diddy passou pelo último Manky Kong |
| 113985 | Klaptrap final ultrapassado |
| 114375 | Croctopus Chase selecionada automaticamente no mapa |
| 114560 | Mapa de Gorilla Glacier estabilizado, `entrance=0x003E`, nove vidas e 80 bananas |

O piloto headless e o coletor de QA repetiram os 114.560 quadros desde o menu em perfis novos, sem restaurar snapshots. O contador registrou nove vidas durante toda a fase. As capturas finais PPM foram idênticas. O SHA-256 do framebuffer registrado pelo piloto é `b0b890560c37f0007719b8208fa1e7cc79e9d47f739265d41fd6b9878fdca6f7`. Os 59 testes Python passaram.

Para repetir, use o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com um perfil novo, 114.560 quadros e o roteiro de Croctopus Chase. O próximo teste começa pela entrada em Croctopus Chase.

## Saída de Croctopus Chase

O [roteiro de 125.724 quadros](../recipes/usa-rev1/campaign-to-torchlight-trouble-map.inputs) mantém os comandos até o mapa de Croctopus Chase. Diddy passa pelo primeiro Croctopus no corredor subaquático e recupera Donkey no barril DK. A rota cruza os túneis, ativa o checkpoint e ganha uma vida extra ao completar 100 bananas. Diddy é atingido nos últimos túneis e Donkey segue sozinho até a saída. Ao voltar ao mapa, Cranky's Cabin fica selecionada. Um toque para cima seleciona Torchlight Trouble.

| Quadro | Resultado |
| --- | --- |
| 114821 | Croctopus Chase aberta, `entrance=0x003E`, `scene=0x0003`, nove vidas |
| 115690 | Donkey recuperado no barril DK |
| 116782 | Passagem vertical do lado leste alcançada |
| 118658 | Corredor oeste alcançado |
| 119602 | Barril de checkpoint visível |
| 119650 | Barril de checkpoint ativado |
| 120930 | Subida concluída após a perseguição no corredor pós-checkpoint |
| 121171 | Vida extra registrada após completar 100 bananas |
| 125058 | Saída subaquática alcançada |
| 125398 | Retorno ao mapa com Cranky's Cabin selecionada |
| 125524 | Torchlight Trouble selecionada com um toque para cima |
| 125724 | Mapa estabilizado, `entrance=0x0014`, dez vidas e 11 bananas |

Em um perfil de QA separado, a perda de uma vida após o checkpoint devolveu o jogo ao mapa com Croctopus Chase selecionada. Ao entrar de novo, o piloto abriu `entrance=0x003F` e reposicionou Donkey no barril de checkpoint.

O executável headless anterior rejeitava roteiros acima de 120 mil quadros. A validação de `FRAMES` passou a aceitar inteiros positivos até o limite representável pelo contador. O executável atualizado informa o intervalo aceito ao receber um argumento inválido. A comparação de 4.800 quadros com o build anterior produziu o mesmo relatório de imagem, áudio e memória. [Código do headless](../runner/usa_rev1.c).

O coletor de QA e o piloto headless reproduziram os 125.724 quadros desde o menu em perfis novos. O registro de vidas mostrou apenas o ganho da vida extra em Croctopus Chase. A imagem final PPM e o arquivo de salvamento coincidiram byte a byte. O SHA-256 do framebuffer registrado pelo piloto é `4c7d16001badce81c5b5ce3e0efc6bca6963fe3a72cbd821ea2a69c152b64136`. Os 59 testes Python passaram.

Para repetir, compile o piloto atualizado e use o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com um perfil novo, 125.724 quadros e o roteiro de Torchlight Trouble. O próximo teste começa pela entrada em Torchlight Trouble. [Script de compilação do piloto](../scripts/build_ptbr_pilot.ps1).

## Saída de Torchlight Trouble

O [roteiro de 129.094 quadros](../recipes/usa-rev1/campaign-to-gorilla-glacier-candy-map.inputs) preserva os comandos até o mapa de Torchlight Trouble. Donkey abre a caixa de Squawks com um salto. As capturas mostram a caverna escura antes da abertura e o facho iluminando o terreno à frente depois dela. A lanterna é a função descrita para Squawks no manual original. [Manual de Donkey Kong Country](https://www.nintendo.co.jp/clvs/manuals/common/pdf/CLV-P-SAALE.pdf).

A rota principal passa pelos barris em chamas e pelas plataformas móveis, ativa o checkpoint e recupera Diddy no barril DK. Diddy termina a travessia das serras e cruza a saída. De volta ao mapa, um toque para a direita seleciona Candy's Save Point.

| Quadro | Resultado |
| --- | --- |
| 125985 | Torchlight Trouble aberta, `entrance=0x0014`, `scene=0x0001`, dez vidas |
| 126066 | Squawks liberado e facho visível |
| 126489 | Plataforma horizontal alcançada |
| 126739 | Elevador alcançado |
| 127125 | Barril de checkpoint ativado |
| 127225 | Diddy recuperado no barril DK |
| 128081 | Última plataforma móvel alcançada |
| 128398 | Placa de saída visível |
| 128893 | Retorno ao mapa de Gorilla Glacier |
| 129094 | Candy's Save Point selecionado, `entrance=0x00FC`, dez vidas e 34 bananas |

Em um perfil separado, uma queda após o checkpoint devolveu o jogo ao mapa com uma vida a menos. Ao entrar novamente, o piloto abriu `entrance=0x0013` e posicionou Diddy no checkpoint com Squawks e a lanterna acesa.

O coletor de QA e o piloto headless reproduziram os 129.094 quadros desde o menu em perfis novos. O contador ficou em dez vidas durante a rota principal da fase. A imagem final PPM e o arquivo de salvamento coincidiram byte a byte. O SHA-256 do framebuffer registrado pelo piloto é `aafc8caff451ef7ecef95fbfd50ee527420c10951be71012e96ba4a7f6f15f8d`. Os 59 testes Python passaram.

Para repetir, use o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com um perfil novo, 129.094 quadros e o roteiro de Candy's Save Point. O próximo teste é o salvamento da Candy em Gorilla Glacier.

## Salvamento da Candy em Gorilla Glacier

O [roteiro de 129.851 quadros](../recipes/usa-rev1/campaign-to-gorilla-glacier-candy-save.inputs) preserva a rota até o mapa da Candy. A sequência entra em Candy's Save Point, salta no barril e confirma o slot 1. A tela mostra 00:28 e 21% antes de voltar ao mapa.

| Quadro | Resultado |
| --- | --- |
| 129094 | Candy's Save Point selecionado em Gorilla Glacier |
| 129355 | Diálogo da Candy em PT-BR |
| 129715 | Tela de salvamento com o slot 1 selecionado, 00:28 e 21% |
| 129851 | Confirmação concluída e retorno ao mapa, `entrance=0x00FC`, dez vidas e 34 bananas |

Na reabertura, o menu de seleção exibiu os mesmos 00:28 e 21% no slot 1. Ao carregar, os Kongs voltaram ao ponto da Candy em Gorilla Glacier. A nova sessão começou com cinco vidas e zero bananas. Três toques para a esquerda no mapa, passando por Torchlight Trouble e Funky's Flights, selecionam Rope Bridge Rumble.

O coletor de QA e o headless reproduziram os 129.851 quadros desde o menu em perfis novos. Os dois gravaram o mesmo arquivo de 2.048 bytes, com SHA-256 `b48f8b1daf9c266fe691df3050bd8e4e3d4eea7ede647c67c3649391e1b6109e`. Na reabertura em processos novos, Win32 e headless produziram a mesma imagem e o mesmo conteúdo de WRAM e SRAM. O arquivo em disco e o backup automático coincidiram. Os 59 testes Python passaram.

Para reproduzir a gravação, use a seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com um perfil novo, 129.851 quadros e o roteiro de salvamento em Gorilla Glacier. Depois que o processo encerrar, use o mesmo `DKC_REV1_SAVE_DIR` em uma nova execução de 4.801 quadros com o [roteiro de reabertura](../recipes/usa-rev1/cold-load.inputs).

## Saída de Rope Bridge Rumble

O [roteiro de 134.644 quadros](../recipes/usa-rev1/campaign-to-really-gnawty-rampage-map.inputs) mantém os comandos até o salvamento da Candy. Três toques para a esquerda no mapa selecionam Rope Bridge Rumble. A rota recupera Donkey num barril DK antes do checkpoint e Diddy num segundo barril DK depois dele. Diddy cruza a última sequência de pneus e os três Zingers antes da saída.

| Quadro | Resultado |
| --- | --- |
| 130304 | Rope Bridge Rumble selecionada, `entrance=0x00CE` |
| 130565 | Entrada na fase, dez vidas e 34 bananas |
| 130692 | Primeiro pneu usado para cruzar o vão inicial |
| 131057 | Impulso alto do pneu para alcançar a rota superior |
| 131673 | Primeiro barril DK aberto na sequência de pneus suspensos |
| 132016 | Checkpoint ativado, dez vidas e 49 bananas |
| 132872 | Diddy recuperado no segundo barril DK |
| 133155 | Trecho de plataformas móveis e Zingers atravessado |
| 133876 | Última sequência de três pneus suspensos atravessada |
| 134170 | Último vão transposto por cima dos três Zingers |
| 134524 | Retorno ao mapa de Gorilla Glacier após a saída |
| 134644 | Really Gnawty Rampage selecionada automaticamente, `entrance=0x00E2`, dez vidas e 53 bananas |

Em um perfil separado, uma morte após o checkpoint devolveu o jogador ao mapa com nove vidas. A nova entrada começou no checkpoint (`entrance=0x00CF`), junto ao barril intermediário. A rota principal manteve as dez vidas da Candy e o mesmo arquivo de salvamento do slot 1.

As 45 capturas da reprodução desde o menu coincidiram com as da repetição iniciada no estado de QA do mapa da Candy. Os 59 testes Python passaram. Para repetir, use um perfil novo e o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com o roteiro de Really Gnawty Rampage e 134.644 quadros. A próxima etapa começa no mapa, com o chefe selecionado.

## Really Gnawty e chegada a Kremkroc Industries Inc.

O [roteiro de 137.350 quadros](../recipes/usa-rev1/campaign-to-oil-drum-alley-map.inputs) mantém os comandos até Really Gnawty Rampage. Na arena, os Kongs desviam dos saltos altos e atingem o chefe de cima. Após o quinto golpe, a animação mostra a banana gigante. Um toque em B leva ao mapa geral, que seleciona Kremkroc Industries Inc. Outro toque em B abre o mapa industrial com Oil Drum Alley selecionada.

| Quadro | Resultado |
| --- | --- |
| 134885 | Arena de Really Gnawty Rampage, `entrance=0x00E2`, `scene=0x000C` |
| 134949 | Primeiro golpe confirmado, quatro golpes restantes |
| 135202 | Segundo golpe confirmado, três golpes restantes |
| 135638 | Terceiro golpe confirmado, dois golpes restantes |
| 135940 | Quarto golpe confirmado, um golpe restante |
| 136308 | Quinto golpe confirmado |
| 136548 | Animação de vitória e banana gigante |
| 137049 | Kremkroc Industries Inc. selecionada no mapa geral, `entrance=0x00E7` |
| 137350 | Oil Drum Alley selecionada no mapa industrial, `entrance=0x0040`, dez vidas e 53 bananas |

O coletor de QA reproduziu o roteiro desde o menu em um perfil novo. As 13 capturas coincidiram com as da repetição iniciada no estado de QA do mapa de Really Gnawty Rampage. O teste manteve dez vidas e 53 bananas durante a luta e a transição. O arquivo do slot 1 manteve o mesmo conteúdo da validação da Candy. Os 59 testes Python passaram.

Para repetir, use um perfil novo e o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com o roteiro de Oil Drum Alley e 137.350 quadros. A próxima etapa começa pela entrada em Oil Drum Alley.

## Saída de Oil Drum Alley

O [roteiro de 142.970 quadros](../recipes/usa-rev1/campaign-to-trick-track-trek-map.inputs) mantém os comandos até a seleção de Oil Drum Alley. Na rota principal, Donkey usa o canhão oculto para voltar à plataforma alta, ativa o checkpoint e recupera Diddy num barril DK. Diddy usa os pneus suspensos para atravessar a sequência final de tambores.

| Quadro | Resultado |
| --- | --- |
| 137611 | Entrada em Oil Drum Alley, `entrance=0x0040`, `scene=0x0007`, dez vidas e 53 bananas |
| 138972 | Canhão oculto lança Donkey do corredor baixo |
| 139607 | Barril intermediário ativado, dez vidas e 60 bananas |
| 140126 | Primeiro fosso após o checkpoint atravessado |
| 141081 | Diddy recuperado no barril DK |
| 141239 | Travessia dos dois tambores sobre o fosso concluída |
| 142186 | Segundo pneu suspenso alcançado na sequência final |
| 142352 | Último tambor ultrapassado |
| 142730 | Retorno ao mapa de Kremkroc Industries Inc. |
| 142970 | Trick Track Trek selecionada automaticamente, `entrance=0x002F`, dez vidas e 64 bananas |

Em um perfil separado, uma queda depois do checkpoint devolveu o jogador ao mapa com nove vidas. Ao entrar novamente, o jogo abriu `entrance=0x0044` e retomou na plataforma do barril intermediário.

A reprodução desde o menu em perfil novo e a repetição iniciada no estado de QA do mapa de Oil Drum Alley geraram 49 capturas idênticas. O arquivo do slot 1 manteve o mesmo conteúdo da validação da Candy. Os 59 testes Python passaram. Para repetir, use um perfil novo e o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com o roteiro de Trick Track Trek e 142.970 quadros. A próxima etapa começa pela entrada em Trick Track Trek.

## Saída de Trick Track Trek

O [roteiro de 153.169 quadros](../recipes/usa-rev1/campaign-to-elevator-antics-map.inputs) mantém os comandos até o mapa de Trick Track Trek. A rota principal embarca na primeira plataforma, cruza os Neckys e os projéteis, ativa o checkpoint junto à segunda plataforma e recupera Diddy em um barril DK. No fim do trilho, Diddy pula para a passarela e passa pelos barris antes da saída.

| Quadro | Resultado |
| --- | --- |
| 143261 | Entrada estável em Trick Track Trek, `entrance=0x002F`, `scene=0x0006`, dez vidas e 64 bananas |
| 143464 | Primeira plataforma em movimento, dez vidas e 66 bananas |
| 147470 | Fim do primeiro trilho alcançado |
| 147699 | Checkpoint ativado e segunda plataforma alcançada, dez vidas e 73 bananas |
| 148174 | Barril DK aberto e Diddy na segunda plataforma |
| 150686 | Gêmeos Gnawty ultrapassados |
| 152401 | Fim do segundo trilho alcançado, dez vidas e 79 bananas |
| 152446 | Salto para a passarela final concluído |
| 152769 | Retorno ao mapa de Kremkroc Industries Inc. |
| 153169 | Elevator Antics selecionada, `entrance=0x0018`, dez vidas e 79 bananas |

Em um perfil separado, uma queda depois do checkpoint devolveu o jogador ao mapa com nove vidas. A nova entrada abriu `entrance=0x0039` e retomou com Donkey junto à segunda plataforma, com a câmera em 32.954.

A execução desde o menu em perfil novo e a repetição iniciada no estado de QA do mapa de Trick Track Trek geraram 42 capturas idênticas. O executável headless do piloto PT-BR repetiu toda a sequência desde o menu e coincidiu com o coletor na imagem final, na WRAM e no arquivo de salvamento. O slot 1 preservou os 2.048 bytes e o SHA-256 `b48f8b1daf9c266fe691df3050bd8e4e3d4eea7ede647c67c3649391e1b6109e` da validação da Candy. Os 59 testes Python passaram. A cobertura desta etapa acompanha o percurso principal e o retorno pelo checkpoint. Bônus e escuta no dispositivo seguem na matriz de validação.

Para reproduzir desde o menu, use um perfil novo e o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com o roteiro de Elevator Antics e 153.169 quadros. As evidências locais ficam em `trick-verified-live/`, `trick-verified-snapshot/`, `trick-verified-stock/` e `trick-final-confirmation-1118/` dentro da pasta de campanha em `evidence/2026-11-10/pt-BR/campaign-start/`. O estado `trick-verified-live/elevator-antics-selecionada.snap` permite retomar a exploração local. A próxima etapa começa pela entrada em Elevator Antics.

## Saída de Elevator Antics

O [roteiro de 160.795 quadros](../recipes/usa-rev1/campaign-to-poison-pond-map.inputs) preserva as entradas até o mapa de Elevator Antics. A rota cruza as cordas do ninho de Zingers, ativa o checkpoint, usa um barril contra Krusha e atravessa os conjuntos de elevadores. No trecho final, Diddy desce pelo fosso para passar sob o teto baixo e sobe no elevador do outro lado. As bananas na saída rendem a 11ª vida, sem perda de vidas na rota principal.

| Quadro | Resultado |
| --- | --- |
| 153169 | Elevator Antics selecionada no mapa, `entrance=0x0018`, `scene=0x0006`, dez vidas e 79 bananas |
| 153460 | Entrada estável na fase, `entrance=0x0018`, `scene=0x0001` |
| 155722 | Saída do ninho de Zingers |
| 156939 | Estrela do checkpoint ativa, dez vidas e 94 bananas |
| 157952 | Krusha atingido por um barril |
| 159722 | Travessia sob o teto baixo entre elevadores, dez vidas e 99 bananas |
| 160127 | 11ª vida obtida na saída |
| 160514 | Retorno ao mapa com Elevator Antics selecionada |
| 160795 | Poison Pond selecionada ao mover para a direita, `entrance=0x0022`, `scene=0x0001`, 11 vidas e zero bananas |

Em um perfil de QA separado, a partir do quadro 156.939, o teste atravessou o primeiro patamar e perdeu uma vida. Ao selecionar Elevator Antics de novo, Diddy reapareceu na área do checkpoint no quadro 158.010, com `entrance=0x0023`, câmera 39.325, nove vidas e 94 bananas.

As 60 capturas do coletor coincidiram entre a execução iniciada no menu com retomada no quadro 158.878 e a repetição iniciada no mapa de Elevator Antics. Em um perfil novo, o executável headless do piloto PT-BR executou os 160.795 quadros sem retomada e reproduziu a mesma imagem final, WRAM e SRAM. O slot 1 manteve os 2.048 bytes do salvamento na Candy, com SHA-256 `b48f8b1daf9c266fe691df3050bd8e4e3d4eea7ede647c67c3649391e1b6109e`. Os 59 testes Python passaram. A cobertura desta etapa inclui o percurso principal e o retorno pelo checkpoint. Bônus e escuta no dispositivo seguem na matriz de validação.

Para reproduzir, use um perfil novo e o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com o roteiro de Poison Pond e 160.795 quadros. O SHA-256 do roteiro é `97930af7d22914fb8ed2c4400301cc9851560c7929296b557e81974e9fa829ed`. As evidências locais ficam em `ea-live/`, `ea-live-tail/`, `ea-full-reference/`, `ea-verified-stock/` e `ea-confirmation/` na pasta `evidence/2026-11-10/pt-BR/campaign-start/`. O estado `ea-live-tail/poison-pond-selecionada.snap` permite retomar pela entrada em Poison Pond.

## Saída de Poison Pond

O [roteiro de 169.930 quadros](../recipes/usa-rev1/campaign-to-mine-cart-madness-map.inputs) preserva as entradas até o mapa de Poison Pond. Diddy nada entre os peixes e as primeiras serras e recupera Donkey em um barril DK. A rota ativa o checkpoint, usa os recuos dos corredores para esperar as serras passarem e cruza o último cardume junto ao teto, com 11 vidas durante a fase. Consultei o guia de T_Hayes para localizar as bifurcações de Poison Pond. [Guia no GameFAQs](https://gamefaqs.gamespot.com/snes/588282-donkey-kong-country/faqs/16178).

| Quadro | Resultado |
| --- | --- |
| 160795 | Poison Pond selecionada no mapa, `entrance=0x0022`, `scene=0x0001`, 11 vidas |
| 161086 | Entrada estável no corredor subaquático, `entrance=0x0022`, `scene=0x0003` |
| 162916 | Donkey retorna pelo primeiro barril DK usado no roteiro |
| 164420 | Estrela do checkpoint ativa, 11 vidas e 19 bananas |
| 165722 | Diddy recuperado na sala leste antes das serras giratórias |
| 167624 | Donkey recuperado na sala oeste |
| 168136 | Abrigo lateral alcançado no corredor vertical das duas serras |
| 168997 | Duas serras finais ultrapassadas, 11 vidas e 24 bananas |
| 169649 | Volta ao mapa com Poison Pond selecionada |
| 169930 | Mine Cart Madness selecionada com um toque para cima, `entrance=0x0027`, `scene=0x0003`, 11 vidas e 24 bananas |

Em um perfil de QA separado, a tentativa iniciada no quadro 164.420 perdeu uma vida em uma serra. Poison Pond voltou a aparecer no mapa no quadro 164.930, com dez vidas. Após a transição do mapa e a nova entrada, Donkey reapareceu nas coordenadas `896, 27103`, junto ao checkpoint, no quadro 165.451 (`entrance=0x002A`, `scene=0x0003`, câmera 767).

O coletor de QA do piloto PT-BR repetiu o roteiro desde o menu e, em outro perfil, a partir do mapa de Poison Pond. As 42 capturas e a WRAM final foram idênticas. O salvamento do slot 1 manteve 2.048 bytes e o SHA-256 `b48f8b1daf9c266fe691df3050bd8e4e3d4eea7ede647c67c3649391e1b6109e` da validação da Candy. Os 59 testes Python passaram. Bônus, segredos e escuta em dispositivo fazem parte da matriz geral.

Para reproduzir, use um perfil novo e o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com o roteiro de Mine Cart Madness e 169.930 quadros. O SHA-256 do roteiro é `1e672479f86cde381ceadaaf5ebf10c2ab29e0a9153d92a6aeb8dfaad5a20464`. As evidências locais ficam em `pp-live/`, `pp-snapshot/` e `pp-confirmation/` na pasta `evidence/2026-11-10/pt-BR/campaign-start/`. O estado `pp-live/mine-cart-madness-selecionada.snap` permite retomar pela entrada em Mine Cart Madness.

## Saída de Mine Cart Madness

O [roteiro de 176.304 quadros](../recipes/usa-rev1/campaign-to-blackout-basement-map.inputs) parte do menu e preserva todas as entradas até o mapa de Mine Cart Madness. No percurso, Diddy salta de um carrinho ao outro, usa os trilhos inferiores e superiores, passa pelos Neckys e pelos Zingers, usa os pneus para atravessar os vãos e salta do último carrinho até a saída. A rota principal mantém 11 vidas.

| Quadro do replay | Observação |
| ---: | --- |
| 169930 | Mine Cart Madness selecionada no mapa, `entrance=0x0027`, `scene=0x0003`, 11 vidas e 24 bananas |
| 170296 | Aproximação ao primeiro carrinho, `entrance=0x0027`, `scene=0x0005` |
| 170541 | Diddy no primeiro carrinho |
| 170932 | Primeira troca de carrinho após o vão |
| 172515 | Checkpoint acionado após os três vãos, com 43 bananas |
| 173085 | Terceiro vão após o checkpoint ultrapassado |
| 173369 | Transferência para o próximo carrinho com impulso do pneu |
| 174159 | Salto do pneu sobre o Kritter no carrinho |
| 174631 | Terceiro Zinger vermelho da subida ultrapassado |
| 175367 | Aterrissagem após saltar do último carrinho |
| 175503 | Diddy na saída, após o último Gnawty |
| 176304 | Blackout Basement selecionada com um toque para a direita, `entrance=0x0041`, `scene=0x0005`, 11 vidas e 60 bananas |

Em um perfil de QA separado, a reprodução a partir do checkpoint do quadro 172.515 deixou o carrinho seguir sem comandos até perder uma vida. O quadro 173.315 mostrou a volta ao mapa com dez vidas. Um toque em B e 175 quadros sem comandos recolocaram Diddy no carrinho junto ao checkpoint no quadro 173.491, em `x=6748`, `y=240`, com `entrance=0x003B`, `scene=0x0005` e câmera 6665.

O coletor de QA headless do piloto PT-BR no Windows, com USA Rev 1, reproduziu o trajeto desde o menu e, em outro perfil, a partir do mapa de Mine Cart Madness. As 57 capturas e a WRAM final foram idênticas. A SRAM do slot 1 manteve 2.048 bytes e o SHA-256 `b48f8b1daf9c266fe691df3050bd8e4e3d4eea7ede647c67c3649391e1b6109e` do salvamento validado na Candy. Os 59 testes Python passaram. Os bônus, os segredos e o áudio em dispositivo seguem na matriz geral de validação.

Para reproduzir, use um perfil novo e o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com o roteiro de Blackout Basement e 176.304 quadros. O SHA-256 do roteiro é `c0e73c169e66ff5c17e61d5a709d83bd4211b6b5e6518d13a5cf81581d25647e`. As evidências locais ficam em `mc-live/`, `mc-snapshot/` e `mc-confirmation/` na pasta `evidence/2026-11-10/pt-BR/campaign-start/`. O estado `mc-live/blackout-basement-selecionada.snap` permite retomar pela entrada em Blackout Basement.

## Saída de Blackout Basement

O [roteiro de 181.287 quadros](../recipes/usa-rev1/campaign-to-boss-dumb-drum-map.inputs) começa no menu e preserva todas as entradas até o mapa de Blackout Basement. A rota usa pneus, cordas, elevadores e plataformas que afundam. Donkey assume o controle após o último grupo de Kritters e passa pelo Klaptrap final. A rota principal mantém 11 vidas.

| Quadro do replay | Observação |
| ---: | --- |
| 176304 | Blackout Basement selecionada, `entrance=0x0041`, `scene=0x0005`, 11 vidas e 60 bananas |
| 176485 | Entrada iluminada, `entrance=0x0041`, `scene=0x0007`, Diddy em `x=12217` |
| 176535 | Cenário escuro na mesma posição, com Diddy visível |
| 178245 | Checkpoint acionado com o salto do pneu, 65 bananas |
| 178508 | Primeira corda no extremo direito do balanço |
| 178834 | Diddy chega ao primeiro elevador |
| 179080 | Segunda corda no extremo direito do balanço, após passar pelos dois Klumps |
| 179323 | Segunda plataforma do par de elevadores |
| 179623 | Segunda plataforma horizontal |
| 179920 | Três Klaptraps ultrapassados após a primeira plataforma que afunda |
| 180163 | Quarta plataforma que afunda na sequência final |
| 180537 | Manky Kong e os barris ultrapassados |
| 180877 | Volta ao mapa de Kremkroc Industries Inc. |
| 181287 | Boss Dumb Drum selecionado automaticamente, `entrance=0x00E3`, `scene=0x0007`, 11 vidas e 72 bananas |

Em uma repetição a partir do quadro escuro 176.535, oito quadros de corrida levaram Diddy de `x=12217` a `x=12228` com o cenário ainda escuro. Oito quadros depois, a iluminação voltou e Diddy chegou a `x=12250`. A fração de pixels com luminância zero nas quatro capturas foi 61,24%, 97,79%, 97,67% e 60,17%, na ordem da transição da luz para o escuro, do movimento no escuro e do retorno da luz.

Em outro perfil de QA, a partir do checkpoint no quadro 178.245, foram usados 45 quadros de corrida para a direita e 700 sem comandos. A tentativa perdeu uma vida e voltou ao mapa no quadro 178.990. Um toque em B e 185 quadros sem comandos recolocaram Donkey em `x=16544`, `y=276` no quadro 179.176, junto ao pneu do checkpoint, com dez vidas, `entrance=0x0045`, `scene=0x0007` e câmera 16472.

O coletor headless do piloto PT-BR para Windows com USA Rev 1 reproduziu a rota desde o menu e desde o mapa de Blackout Basement em perfis independentes. As 57 capturas e a WRAM final coincidiram. A SRAM do slot 1 manteve 2.048 bytes e o SHA-256 `b48f8b1daf9c266fe691df3050bd8e4e3d4eea7ede647c67c3649391e1b6109e` do salvamento validado na Candy. Os 59 testes Python passaram. Bônus, segredos e áudio em dispositivo seguem na matriz geral.

Para reproduzir, use um perfil novo e o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com o roteiro de Boss Dumb Drum e 181.287 quadros. O SHA-256 do roteiro é `963bcd893495e028a40eacc676d1ff7f799690635fb7dce920d5375b47fc34d0`. As evidências locais ficam em `bb-live/`, `bb-snapshot/` e `bb-confirmation/` dentro de `evidence/2026-11-10/pt-BR/campaign-start/`. O estado `bb-live/boss-dumb-drum-selecionado.snap` permite retomar pela entrada no chefe.

## Boss Dumb Drum e chegada a Chimp Caverns

O [roteiro de 185.077 quadros](../recipes/usa-rev1/campaign-to-tanked-up-trouble-map.inputs) preserva os comandos desde o menu até o mapa de Boss Dumb Drum. Donkey se desloca lateralmente para desviar das quedas do tambor. Ele derrota os pares de Kritters, Slippas e Klumps com rolamentos e os pares de Klaptraps e Armys com saltos. O tambor cai no centro e a animação mostra a banana gigante. O roteiro segue até Chimp Caverns no mapa geral e entra no mapa local com um toque em B.

| Quadro do replay | Observação |
| ---: | --- |
| 181287 | Boss Dumb Drum selecionado no mapa, `entrance=0x00E3`, `scene=0x0007`, 11 vidas e 72 bananas |
| 181548 | Arena carregada, `scene=0x000C` |
| 181860 | Par de Kritters derrotado |
| 182261 | Par de Slippas derrotado |
| 182842 | Par de Klaptraps derrotado |
| 183421 | Par de Klumps derrotado |
| 184110 | Par de Armys derrotado. Tambor retorna ao centro |
| 184385 | Banana gigante ao lado de Donkey na animação de vitória |
| 184886 | Chimp Caverns selecionado no mapa geral, `entrance=0x00E6` |
| 185077 | Tanked Up Trouble selecionada no mapa de Chimp Caverns, `entrance=0x0030`, `scene=0x000C`, 11 vidas e 72 bananas |

No piloto headless PT-BR para Windows com USA Rev 1, o replay desde o menu chegou ao quadro 181.287 e produziu um estado idêntico byte a byte ao marco de Boss Dumb Drum da validação anterior. A verificação foi retomada desse estado em um novo processo após o limite de espera do coletor. Outra execução partiu do estado salvo na validação de Blackout Basement. Os comandos do roteiro coincidiram quadro a quadro com os registrados, e as duas reproduções da luta e da transição coincidiram nas 33 capturas e na WRAM final. A SRAM do slot 1 preservou os 2.048 bytes da Candy. Os 59 testes Python passaram. A seleção no mapa é o ponto final desta validação.

Para reproduzir, use um perfil novo e o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com o roteiro de Tanked Up Trouble e 185.077 quadros. O SHA-256 do roteiro é `e219e4fb560a8bd2f4ac50decb85ffa53dc189c95855a17c80275ebd296e86ef`. As evidências locais estão em `dd-live/`, `dd-resumed/`, `dd-snapshot/` e `dd-confirmation-v2/` dentro de `evidence/2026-11-10/pt-BR/campaign-start/`. O estado `dd-resumed/tanked-up-trouble-selecionada.snap` permite retomar pela entrada em Tanked Up Trouble.

## Saída de Tanked Up Trouble

O [roteiro de 194.983 quadros](../recipes/usa-rev1/campaign-to-manic-mincers-map.inputs) preserva as entradas anteriores até a seleção de Tanked Up Trouble. A rota principal registra 23 abastecimentos nas duas plataformas sobre trilhos. Os saltos incluem rebotes em Neckys e pneus, desvios pelos canhões e a passagem por Zingers. O contato com inimigos alternou o personagem ativo em trechos da rota. O contador permaneceu em 11 vidas da entrada à saída.

| Quadro | Resultado |
| --- | --- |
| 185077 | Tanked Up Trouble selecionada no mapa de Chimp Caverns, `entrance=0x0030`, `scene=0x000C`, 11 vidas e 72 bananas |
| 185312 | Entrada na fase, `scene=0x0006`, com câmera em 39.290 |
| 185758 | Primeiro abastecimento registrado na plataforma |
| 188606–188865 | O indicador mostra duas luzes laranja antes do desvio para o nono barril e cinco verdes após a volta do canhão |
| 189184 | Barril de checkpoint ativado em x=43.990, antes da segunda plataforma |
| 193852 | 23º abastecimento registrado, após a coleta do barril em x=50.337 |
| 194137–194550 | Plataforma para no fim do trilho. Os saltos passam pela seta e alcançam a passarela elevada com a placa EXIT |
| 194862 | Retorno ao mapa de Chimp Caverns com a ligação para a próxima fase aberta |
| 194983 | Manic Mincers selecionada após um toque para cima, `entrance=0x0012`, `scene=0x0006`, câmera em zero, 11 vidas e 93 bananas |

O teste independente partiu do checkpoint ativado no quadro 189.184. A entrada `0082 210` seguida de `0000 700` provocou a queda e devolveu a seleção a Tanked Up Trouble no quadro 190.094, com 10 vidas. Um toque em B (`0001 1`) e 195 quadros neutros reabriram a fase pelo checkpoint no quadro 190.290, com `entrance=0x003A`, câmera em 43.914 e Donkey em x=43.986.

O piloto headless PT-BR para Windows usou a ROM USA v1.1 (Rev 1). A execução desde o menu em perfil novo registrou os mesmos comandos quadro a quadro que o roteiro. A execução a partir do estado salvo no mapa produziu as mesmas 81 capturas PPM e os mesmos 128 KiB de WRAM final. Os 2.048 bytes da SRAM do slot 1 coincidiram com a gravação da Candy. Os 59 testes Python passaram. A cobertura deste marco vai até a seleção no mapa e inclui a retomada pelo checkpoint. A revisão de bônus, áudio em janela e entrada em Manic Mincers segue pendente.

Para repetir, use um perfil novo e o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com o roteiro de Manic Mincers e 194.983 quadros. O SHA-256 do roteiro é `df60a8c69adcee2ed9a9420438b3762cb4911dea8ee042223d898a2c227cb6d5`. As evidências locais ficam em `tu-live/`, `tu-snapshot/` e `tu-confirmation/` dentro de `evidence/2026-11-10/pt-BR/campaign-start/`. O estado `tu-live/manic-mincers-selecionada.snap` permite retomar pela entrada em Manic Mincers.

## Saída de Manic Mincers

O [roteiro de 200.157 quadros](../recipes/usa-rev1/campaign-to-misty-mine-map.inputs) preserva as entradas anteriores até a seleção de Manic Mincers. A rota principal alterna passagens por baixo dos Mincers e saltos sobre eles. Exercita Mincers fixos, verticais, orbitais e um que rola pelo chão. Diddy assume o controle após contato com um par de Mincers e recupera Donkey com um barril DK depois do checkpoint. Donkey termina a fase após Diddy ser atingido no quarto fosso. A coleta de bananas rende uma vida e o contador chega a 12.

| Quadro | Resultado |
| --- | --- |
| 194983 | Manic Mincers selecionada em Chimp Caverns, `entrance=0x0012`, `scene=0x0006`, 11 vidas e 93 bananas |
| 195058 | Transição para a fase, `scene=0x0001` |
| 196155 | Contador de vidas sobe de 11 para 12 após a 100ª banana |
| 196761 | Diddy ultrapassa o Mincer fixo e o Mincer que rola pelo chão |
| 196978 | Checkpoint ativado. O barril estava em x=20.485 |
| 197368 | Donkey recuperado pelo barril DK após o primeiro Krusha |
| 197856–198895 | Travessia de quatro fossos com plataformas. No segundo, Diddy volta à plataforma entre dois Mincers e salta novamente até a outra margem |
| 199669–199730 | Donkey usa o pneu para saltar acima dos dois Mincers empilhados em x=26.502 |
| 200036 | Retorno ao mapa de Chimp Caverns com a ligação para a próxima fase aberta |
| 200157 | Misty Mine selecionada, `entrance=0x000A`, `scene=0x0001`, câmera em zero, 12 vidas e 16 bananas |

O teste em perfil separado carregou o checkpoint ativado no quadro 196.978. A entrada `0080 220` seguida de `0000 420` provocou a morte e devolveu a seleção a Manic Mincers no quadro 197.618 com 11 vidas. Um toque em B (`0001 1`) e 230 quadros neutros reabriram a fase no quadro 197.849, com `entrance=0x0029`, câmera em 20.413 e Diddy em x=20.485.

O piloto headless PT-BR rodou em Windows com a ROM USA v1.1 (Rev 1) e perfis de QA isolados. A reprodução desde o menu registrou os comandos do roteiro quadro a quadro. As 55 capturas PPM e os 128 KiB de WRAM final coincidiram com a reprodução iniciada no estado salvo do mapa. A SRAM do slot 1 preservou os 2.048 bytes da gravação da Candy. Os 59 testes Python passaram. O teste cobre a rota principal e a reentrada pelo checkpoint. Bônus, áudio em janela e a entrada em Misty Mine seguem pendentes.

Para repetir, use um perfil novo e o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com o roteiro de Misty Mine e 200.157 quadros. O SHA-256 do roteiro é `10c577579dd78c14a93bc95b00285b6c555a2fa3a571bd0bab0f471ff04e9d11`. As evidências locais ficam em `mm-live/`, `mm-snapshot/` e `mm-confirmation/` dentro de `evidence/2026-11-10/pt-BR/campaign-start/`. O estado `mm-live/misty-mine-selecionada.snap` permite retomar pela entrada em Misty Mine.

## Saída de Misty Mine

O [roteiro de 206.398 quadros](../recipes/usa-rev1/campaign-to-loopy-lights-map.inputs) preserva as entradas anteriores até a seleção de Misty Mine. A rota principal inclui subida e descida em cordas, troca entre cordas sobre o fosso, saltos entre os barris que geram inimigos e um salto a partir do topo de um barril até a margem da seta. O contador permaneceu em 12 vidas. Diddy assume após o contato de Donkey com um Klaptrap e conclui a fase.

| Quadro | Resultado |
| --- | --- |
| 200157 | Misty Mine selecionada em Chimp Caverns, `entrance=0x000A`, `scene=0x0001`, 12 vidas e 16 bananas |
| 200457 | Transição para a mina, `scene=0x0002` |
| 201178–201928 | Subida na primeira corda e descida na segunda |
| 202585–202711 | Donkey sobe e salta de uma corda para a seguinte sobre o fosso |
| 203014 | Checkpoint ativado. O barril estava em x=6.437 |
| 203231–203407 | Rota superior pela corda longa até a margem direita |
| 205496–205685 | Diddy parte do topo de um barril, cruza o fosso e salta sobre os quatro barris de Slippas após a seta |
| 206086 | Retorno ao mapa com a ligação seguinte aberta |
| 206207 | Seleção de Funky's Flights como ponto de passagem no mapa, `entrance=0x00F8` |
| 206398 | Loopy Lights selecionada, `entrance=0x0036`, `scene=0x0002`, câmera em zero, 12 vidas e 50 bananas |

O teste de checkpoint partiu do quadro 203.014. As entradas `0082 102`, `0080 1`, `0082 30`, `0083 53`, `0010 31`, `0020 155` e `0000 220` levaram à queda da corda longa e ao retorno ao mapa no quadro 203.606 com 11 vidas. Um toque em B (`0001 1`) seguido de 230 quadros neutros reabriu Misty Mine pelo checkpoint no quadro 203.837, com `entrance=0x002D`, câmera em 6.365 e Donkey em x=6.437.

O bônus da corda longa foi verificado em outro perfil a partir do quadro 203.231. A descida levou ao salto para a direita e à sala de bônus no quadro 203.487, com `entrance=0x0033`. A captura do quadro 204.066 mostra as quatro letras KONG. A recompensa elevou o contador a 13 vidas. A saída devolveu os dois Kongs à mina no quadro 204.528, com `entrance=0x0080`, Donkey em x=8.656 e 63 bananas.

| Quadro ao fim do trecho | Entradas para repetir o bônus após o quadro 203.231 |
| --- | --- |
| 203326 | `0020 95` |
| 203487 | `0083 60`, `0082 101` |
| 203592 | `0082 42`, `0083 43`, `0010 20` |
| 203699 | `0010 37`, `0000 70` |
| 203959 | `0020 73`, `0000 18`, `0010 126`, `0000 43` |
| 204173 | `0020 72`, `0000 142` |
| 204528 | `0010 63`, `0083 64`, `0082 48`, `0000 180` |

O piloto headless PT-BR rodou em Windows com a ROM USA v1.1 (Rev 1). A reprodução desde o menu registrou os comandos do roteiro quadro a quadro. As 55 capturas PPM e os 128 KiB de WRAM final coincidiram com a reprodução iniciada no estado salvo do mapa. A SRAM da Candy preservou os mesmos 2.048 bytes. Os 59 testes Python passaram. A cobertura inclui a rota principal, o checkpoint e o bônus da corda longa. Outras salas de bônus, áudio em janela e entrada em Loopy Lights seguem pendentes.

Para repetir a rota principal, use um perfil novo e o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com o roteiro de Loopy Lights e 206.398 quadros. O SHA-256 do roteiro é `4cc9c7bc8a522c3d67eeade62ce8cc9ce5b078fd9f9933a243c5081c440b78e6`. As evidências locais ficam em `mi-live/`, `mi-snapshot/` e `mi-confirmation/` dentro de `evidence/2026-11-10/pt-BR/campaign-start/`. O estado `mi-live/loopy-lights-selecionada.snap` permite retomar pela entrada em Loopy Lights.

## Saída de Loopy Lights

O [roteiro de 212.344 quadros](../recipes/usa-rev1/campaign-to-platform-perils-map.inputs) preserva as entradas anteriores até a seleção de Loopy Lights. A rota cruza as plataformas móveis, usa pneus para saltar entre apoios sobre fossos e passa pelos Zingers e pelos barris rolantes da subida. Diddy recupera Donkey com um barril DK e Donkey assume após um contato com um Klaptrap. O contador permanece em 12 vidas.

| Quadro | Resultado |
| --- | --- |
| 206398 | Loopy Lights selecionada em Chimp Caverns, `entrance=0x0036`, `scene=0x0002`, 12 vidas e 50 bananas |
| 206685 | Diddy na caverna após saltar perto do primeiro barril de iluminação |
| 207261–207321 | Travessia entre as duas plataformas móveis do fosso |
| 208515–208661 | Barril de checkpoint fechado e depois ativado no ponto x=30.272 |
| 209015 | Donkey recuperado com o barril DK |
| 210111–210236 | Travessia nas duas plataformas que sobem e descem alternadamente |
| 210468–210775 | Saltos nos quatro pneus até a margem dos Zingers |
| 211362–211666 | Subida sobre os barris rolantes e descida para o trecho final |
| 212100 | Retorno ao mapa de Chimp Caverns com a ligação seguinte aberta |
| 212214 | Candy's Save Point selecionado durante a passagem, `entrance=0x00FE` |
| 212344 | Platform Perils selecionada, `entrance=0x002B`, `scene=0x0002`, câmera em zero, 12 vidas e 82 bananas |

O teste de iluminação partiu do quadro 207.771. As entradas `0082 1`, `0083 15`, `0000 43`, `0083 59` e `0000 60` posicionaram Diddy aos pés do barril em x=28.608. O barril estava em OFF no quadro 207.949. Um salto com `0001 15` seguido de `0000 61` deixou o barril em ON no quadro 208.025. Após mais 109 quadros neutros, o barril voltou a OFF. Com a mesma posição de câmera e de Diddy nos quadros 208.025 e 208.134, a média dos tons de cinza entre as linhas 32 e 207 da captura caiu de 13,56 para 1,03 na escala de 0 a 255.

O teste de checkpoint partiu do quadro 208.661 em perfil separado. As entradas `0082 123`, `0083 68`, `0082 1`, `0083 197` e `0000 218` causaram uma queda e trouxeram a seleção de volta a Loopy Lights no quadro 209.268 com 11 vidas. Um toque em B (`0001 1`) e 200 quadros neutros reabriram a fase no quadro 209.469 com `entrance=0x003D`, câmera em 30.200 e Diddy em x=30.272, na posição do checkpoint.

O piloto headless PT-BR rodou em Windows com a ROM USA v1.1 (Rev 1). O replay desde o menu registrou as entradas do roteiro quadro a quadro. As 61 capturas PPM e os 128 KiB de WRAM final coincidiram com a reprodução iniciada no estado salvo do mapa. A SRAM do slot 1 preservou os 2.048 bytes da gravação da Candy. Os 59 testes Python passaram. O teste cobre a rota principal, a iluminação, o checkpoint e a seleção seguinte. As salas de bônus, o áudio em janela e a entrada em Platform Perils ficaram fora deste teste.

Para repetir a rota principal, use um perfil novo e o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com o roteiro de Platform Perils e 212.344 quadros. O SHA-256 é `afaedbfb8c3b840f08bfd35eb475c57aaf9e659642741dc5e69fc5a5ae1abbd0`. As evidências locais ficam em `ll-live/`, `ll-snapshot/`, `ll-confirmation/` e `ll-equal/` dentro de `evidence/2026-11-10/pt-BR/campaign-start/`. O estado `ll-live/platform-perils-selecionada.snap` permite retomar pela entrada em Platform Perils.

## Saída de Platform Perils

O [roteiro de 220.624 quadros](../recipes/usa-rev1/campaign-to-neckys-revenge-map.inputs) preserva as entradas anteriores até a seleção de Platform Perils. A rota principal cruza plataformas horizontais, verticais e descendentes, usa pneus suspensos e abre caminho com barris de TNT nas plataformas guardadas pelos Krushas. Donkey recupera Diddy com um barril DK após o checkpoint. Diddy assume o controle após um contato de Donkey com um Zinger e conclui a fase. A coleta de bananas rende uma vida extra, e o contador termina em 13.

| Quadro | Resultado |
| --- | --- |
| 212344 | Platform Perils selecionada em Chimp Caverns, `entrance=0x002B`, `scene=0x0002`, 12 vidas e 82 bananas |
| 212430–212861 | Entrada na fase com `scene=0x0006`, passagem pelo primeiro Krusha e travessia na primeira plataforma horizontal |
| 213207–214403 | Travessia por plataformas horizontais e verticais, com a passagem entre dois Zingers |
| 214607–214682 | A 100ª banana rende a 13ª vida e zera o contador de bananas. Donkey rebate no Necky e alcança a ponte seguinte |
| 215622–215665 | Barril de checkpoint fechado e depois ativado na posição x=21.328 |
| 216059 | Donkey e Diddy na mesma plataforma após abrir o barril DK |
| 217365–217753 | Salto alto no pneu e descida pelos apoios guardados pelos Kritters |
| 217881–219499 | Travessia por plataformas com pneus suspensos e lançamentos de TNT nas passagens guardadas por Krushas |
| 218963 | Diddy assume após o contato de Donkey com um Zinger |
| 219656–219966 | Plataforma para a esquerda, salto para o apoio elevado e travessia para a última plataforma guardada |
| 220482 | Retorno ao mapa com o caminho para o chefe aberto |
| 220624 | Necky's Revenge selecionado, `entrance=0x00E4`, `scene=0x0006`, câmera em zero, 13 vidas e 24 bananas |

O teste de checkpoint partiu do quadro 215.665 em um perfil separado. As entradas `0082 183` e `0000 255` causaram uma queda e devolveram o controle ao mapa no quadro 216.103, com 12 vidas. Um toque em B (`0001 1`) e 203 quadros neutros reabriram a fase pelo checkpoint no quadro 216.307, com `entrance=0x002C`, câmera em 21.256 e Donkey em x=21.328.

O piloto headless PT-BR rodou em Windows com a ROM USA v1.1 (Rev 1). O replay desde o menu registrou as entradas do roteiro quadro a quadro. As 80 capturas PPM e os 128 KiB de WRAM final coincidiram com o replay iniciado no estado salvo do mapa. A SRAM do slot 1 preservou os 2.048 bytes da gravação da Candy. Os 59 testes Python passaram. As salas de bônus, o áudio em janela e a luta contra Necky's Revenge ficaram fora deste ensaio.

Para repetir a rota principal, use um perfil novo e o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com o roteiro de Necky's Revenge e 220.624 quadros. O SHA-256 é `9dc4396445f35e8a3d5aec193bc8d9662e725ad6cf875a87987931c771d0fd63`. As evidências locais ficam em `platform-perils-replay/`, `platform-perils-snapshot/`, `platform-perils-confirmation/` e `platform-perils-equal/` dentro de `evidence/2026-11-10/pt-BR/campaign-start/`. O estado `platform-perils-replay/neckys-revenge-selecionada.snap` permite retomar na entrada do chefe.

## Saída de Necky's Revenge

O [roteiro de 222.939 quadros](../recipes/usa-rev1/campaign-to-gang-plank-galleon-map.inputs) preserva os 220.624 quadros já validados desde o menu e acrescenta a entrada, a luta e a transição até Gang-Plank Galleon. O registro quadro a quadro identificou cinco ciclos com uma, duas, três, quatro e cinco nozes, respectivamente. Os saltos do pneu permitem desviar dos projéteis e acertar o chefe após cada sequência. Diddy participa dos dois primeiros golpes. Donkey prossegue sozinho após o contato de Diddy com um projétil e completa a luta. O contador de vidas permanece em 13.

| Quadro | Resultado |
| --- | --- |
| 220702 | Entrada na arena, `entrance=0x00E4` e `scene=0x000C` |
| 220919 | Primeiro golpe após uma noz, com quatro golpes restantes |
| 221144 | Segundo golpe após duas nozes, com três golpes restantes |
| 221392 | Terceiro golpe após três nozes, com dois golpes restantes |
| 221707 | Quarto golpe após quatro nozes, com um golpe restante |
| 222053 | Último golpe após cinco nozes e início da animação de derrota do chefe |
| 222324 | Banana gigante visível na arena |
| 222630 | Retorno ao mapa geral, `entrance=0x00E6` |
| 222735 | Seleção automática de Gang-Plank Galleon, `entrance=0x0068` |
| 222939 | Gang-Plank Galleon confirmado no mapa, `scene=0x000C`, câmera em zero, 13 vidas e 24 bananas |

O piloto headless PT-BR rodou em Windows com a ROM USA v1.1 (Rev 1). Dois processos com perfis isolados partiram, respectivamente, do estado gravado ao fim do replay desde o menu e do estado gravado ao fim do replay de Platform Perils. Os dois reproduziram os mesmos 2.315 quadros novos. As entradas registradas, as 24 capturas PPM e os 128 KiB de WRAM inicial e final coincidiram. A SRAM do slot 1 preservou os 2.048 bytes da gravação da Candy. Os 59 testes Python passaram. O ensaio cobre a luta e a transição de mapa no piloto headless. A validação em janela, o áudio e a luta final ficam para os ensaios correspondentes.

Para repetir a rota desde o menu, use o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com um perfil novo, o roteiro de Gang-Plank Galleon e 222.939 quadros. O SHA-256 do roteiro é `2a230e8f1c0655570920d6b2b000178e6e5a545d230c304095855e82c12bc794`. As evidências locais ficam em `neckys-revenge-from-menu-state/`, `neckys-revenge-from-map-state/` e `neckys-revenge-assembled/` dentro de `evidence/2026-11-10/pt-BR/campaign-start/`. O estado `neckys-revenge-from-menu-state/gang-plank-galleon-selecionado.snap` permite retomar na entrada do navio.

## Gang-Plank Galleon e final da campanha

O [roteiro de 254.444 quadros](../recipes/usa-rev1/campaign-to-ending-title.inputs) acrescenta 31.505 quadros ao roteiro que termina no mapa de Gang-Plank Galleon. O registro da luta contou dez lançamentos de coroa e dez golpes confirmados. Após os três primeiros golpes, o chefe fez séries de uma, duas e três investidas. Após o quarto, o quinto e o sexto golpes, vieram ondas de 9, 17 e 25 balas de canhão. O sétimo golpe abriu a sequência dos créditos falsos. King K. Rool se levantou e voltou a atacar com saltos e lançamentos da coroa até o décimo golpe. O contador permaneceu em 13 vidas e 24 bananas até o retorno ao título.

| Quadro | Resultado |
| --- | --- |
| 223021 | Entrada no navio, `entrance=0x0068` e `scene=0x000D` |
| 223432, 223745, 224161 | Primeiros três golpes, seguidos das séries de investidas |
| 224686, 225516, 226658 | Golpes quatro a seis, seguidos das três ondas de balas de canhão |
| 228089 e 228821 | Sétimo golpe e créditos falsos visíveis |
| 229811 | Cena de volta ao navio com controle devolvido, antes da primeira série de saltos |
| 230143 e 230601 | Oitavo e nono golpes após a retomada da luta |
| 231352 e 231604 | Décimo golpe e banana gigante visível |
| 231944 | Conversa de encerramento com Cranky Kong |
| 234194 | Depósito de bananas recuperado |
| 235094 e 242744 | Amostras da apresentação do elenco, com Necky e Candy Kong |
| 245894–250844 | Amostras dos créditos reais, da abertura aos últimos nomes e funções |
| 251210 e 254444 | Reinício automático e tela de título confirmada, `entrance=0x0000`, `scene=0x0001` |

Dois processos com perfis isolados reproduziram o trecho novo no piloto Windows PT-BR sem janela com a ROM local USA v1.1 (Rev 1). Os estados iniciais vieram dos dois replays do marco anterior, no quadro 222.939. As entradas executadas, 53 capturas PPM e 128 KiB de WRAM inicial e final coincidiram. Os 59 testes Python passaram. Este ensaio verificou os estados e as imagens do final. Áudio e apresentação em janela seguem para validação interativa. A cobertura das salas de bônus permanece parcial.

O jogo atualizou automaticamente os 2.048 bytes da SRAM durante a sequência de vitória. Em um terceiro perfil, um novo processo carregou o arquivo final sem restaurar um snapshot. O slot 1 mostrou **00:54 e 34%** no quadro 1.800. No quadro 2.400, o jogo selecionou Jungle Hijinxs no mapa de Kongo Jungle com cinco vidas e zero bananas. No quadro 4.801, a fase estava jogável. O arquivo e o backup gerado na reabertura coincidiram com a SRAM final dos dois replays.

As falas amostradas do Cranky no encerramento apareceram em PT-BR durante a campanha. Os créditos falsos e os rótulos dos créditos reais apareceram em inglês. A revisão posterior identificou sete registros no bloco falso e 25 no real e registrou os critérios para preservar nomes e a brincadeira do chefe. [Revisão dos créditos](15-PT-BR.md#revisão-em-jogo-dos-créditos).

Para reproduzir desde o menu, use um perfil novo e o comando da seção [Retomar em Mine Cart Carnage](#retomar-em-mine-cart-carnage) com o roteiro do final e 254.444 quadros. O SHA-256 do roteiro é `c55c1b2dba6e3f5e2539e3f5390ac56ee46e2570ccf00575e3e2f8eeac10ef26`. Para verificar a reabertura, execute o [roteiro de carregamento](../recipes/usa-rev1/cold-load.inputs) por 4.801 quadros com o mesmo diretório de save. As evidências locais ficam em `gang-plank-replay-menu-state/`, `gang-plank-replay-map-state/`, `gang-plank-postgame-reopen/` e `gang-plank-assembled/` dentro de `evidence/2026-11-10/pt-BR/campaign-start/`.

## Repetição determinística da rota principal

Em 2026-11-22, três processos do piloto PT-BR sem janela executaram os 254.444 quadros do [roteiro completo](../recipes/usa-rev1/campaign-to-ending-title.inputs), desde a inicialização em perfis vazios até o retorno à tela de título. Cada perfil teve sua própria pasta de saves. O teste registrou as entradas de fase e os IDs de cena quadro a quadro e comparou os estados de saída. Ambiente Windows 10 22H2, build 19045.6466, com o executável headless de SHA-256 `a53d58f9b22d00ae6975bbbdd8a3d490920b20d2b5edab32c85a99013540c059`.

| Evidência coincidente nas três rodadas | SHA-256 |
| --- | --- |
| Sequência de entradas e cenas | `9d64f4f36fcc60ca8eea933cb09bf166bd4592c88790bafc0eb8566318c92c0e` |
| Framebuffer final | `d46db4a861f6a6cb5668836eaa1ba7c5ae28f1fc1f1bd234b415bfe77792dd76` |
| WRAM final | `dcc58929ec569425f49db0afe25413258c3d88921dbe2d19c37e6700c03f287d` |
| VRAM final | `e77ba7edfc0e49cc47574a8157c3eb2ff7ec877c9d0920e81e94138675f9c263` |
| Hash acumulado do PCM estéreo | `4eab34a4399fea9a6ebae54b696f4ccc72d5f262fd83789c33184073a080ed45` |
| Arquivo SRAM de 2.048 bytes | `f51056fe02a631c24d6a3224322e3bb131e74e12401f49779d58e6d7be25934c` |

Depois da campanha, cada perfil foi reaberto em outro processo por 4.801 quadros com [cold-load.inputs](../recipes/usa-rev1/cold-load.inputs). As três rodadas chegaram a Jungle Hijinxs (`entrance=0x0016`) e mantiveram o save e a cópia de segurança idênticos à SRAM da vitória. A SRAM coincide também com a do ensaio anterior, que exibiu 00:54 e 34% no slot 1. As imagens finais confirmaram o título e a entrada em Jungle Hijinxs.

V13 foi aprovada para a rota principal automatizada no piloto sem janela. A escuta do áudio em janela e os caminhos de bônus fora do roteiro continuam na matriz V09/V14. Os 59 testes Python passaram. Logs, capturas e verificações locais em `evidence/2026-11-22/v13-campanha/`.
