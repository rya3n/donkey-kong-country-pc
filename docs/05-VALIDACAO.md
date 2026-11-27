# Plano de validação

Estado: protótipo Rev 1 com teste humano de fluidez e validação de persistência em processos novos, detalhada em [Salvamento de progresso](13-SAVES.md). Resultados automatizados não substituem a cobertura de campanha ou comparação com referência independente.

## Identidade mínima de uma execução

Registrar sistema operacional e hardware observado; SHA-256 da ROM; commits do projeto e da engine; comando e configuração de build; SHA-256 do executável; proporção de exibição e dimensões do framebuffer; opções gráficas; entrada usada; estado inicial; frames e duração; resultado e caminho dos artefatos.

Um estado inicial pode ser boot limpo ou um snapshot identificado por hash. Não reutilizar um save como evidência sem identificar a versão que o criou. Proteger uma cópia antes de testar persistência ou migração.

## Matriz inicial

| ID | Cenário | Aceitação proposta | Situação |
| --- | --- | --- | --- |
| V01 | Verificar ROM do perfil | Tamanho e SHA-256 exatos | Rev 1 aceita; v1.2 rejeitada no verificador e no host |
| V02 | Gerar e compilar | Comandos terminam com sucesso e executável é identificado | Protótipo Rev 1 compilado com MSVC; identidade no relatório |
| V03 | Testes do build e suíte pública | Resultados completos, sem falhas inexplicadas; skips justificados | CTest do port aprovado na Rev 1 base e no piloto PT-BR. Suíte pública no Ubuntu: 312 contabilizados, 307 aprovados, cinco pulos. Dois erros de ligação delimitados no Windows. [Resultados](#suíte-pública-do-upstream) |
| V04 | Boot, apresentação e menu | Imagem estável e progressão até seleção de jogo | Executado em janela; usuário confirmou a fluidez após a correção |
| V05 | Entrar em Jungle Hijinxs | Roteiro do boot até controle do personagem | Entrada reproduzida e sessão humana realizada; cobertura ampliada em V14 |
| V06 | Movimento e interação | Mover, pular, rolar, resgatar Diddy, trocar e usar barril | Aprovada no roteiro automatizado de um jogador em Jungle Hijinxs na base e no piloto PT-BR. O ensaio verificou rolamento, arremesso do barril DK, resgate, salto de Diddy e troca nos dois sentidos. [Resultados](31-INICIO-CAMPANHA-PT-BR.md#rolamento-barril-dk-e-troca-de-personagem-v06) |
| V07 | Morte e retorno | Ciclo completo sem travamento e com estado coerente | Retorno ao mapa e nova entrada confirmados em Jungle Hijinxs. Reentrada pelo checkpoint confirmada em Croctopus Chase, Torchlight Trouble, Rope Bridge Rumble, Oil Drum Alley, Trick Track Trek, Elevator Antics, Poison Pond, Mine Cart Madness, Blackout Basement, Tanked Up Trouble, Manic Mincers, Misty Mine, Loopy Lights e Platform Perils |
| V08 | Concluir fase e voltar ao mapa | Saída, transição e progressão corretas | Rota principal validada até Gang-Plank Galleon. O chefe final foi derrotado e o jogo voltou à tela de título após os créditos |
| V09 | Áudio e apresentação | Trecho identificado sem cortes persistentes ou defeitos visíveis | Aprovada para Reptile Rumble. Houve sinal nas 2.076 leituras da sessão do jogo com janela visível, somando a base e o piloto PT-BR. A escuta confirmou som sem cortes durante o movimento. A interrupção antiga ficou restrita ao ensaio original e o DKC-BUG-5 segue em investigação. [Áudio em janela](32-CAMPANHA-PT-BR-AUDIO-E-PROGRESSO.md#áudio-em-janela-na-caverna) |
| V10 | Salvamento do jogo | Salvar com Candy, encerrar normalmente e recuperar em novo processo | Validado em Kongo Jungle e Gorilla Glacier, com reabertura em headless e Win32. Em Monkey Mines, o piloto sem janela reabriu na Candy e entrou na arena de Master Necky. [Teste](32-CAMPANHA-PT-BR-AUDIO-E-PROGRESSO.md#visitas-de-serviço-em-monkey-mines) |
| V11 | Save state, se incluído no marco | Comparar continuação após load com execução contínua | Não implementado; não faz parte da entrega de SRAM |
| V12 | Controle físico | Ações e reconexão no dispositivo disponível | XInput implementado. Mapeamento, zona morta, remoção e reconexão simuladas aprovados. Ensaio físico pendente. [Resultados e procedimento](#controle-xinput-v12) |
| V13 | Repetição determinística | Três replays com mesma entrada e hashes dos estados comparados iguais | Aprovada na rota principal do piloto sem janela. Três replays de 254.444 quadros e três reaberturas de 4.801 quadros coincidiram. [Relatório](32-CAMPANHA-PT-BR-AUDIO-E-PROGRESSO.md#repetição-determinística-da-rota-principal) |

Salvar com Candy e usar save state são funcionalidades diferentes e exigem testes distintos. Um quicksave bem-sucedido não comprova persistência do progresso do cartucho.

## CTest no Windows

Em 2026-11-22, as configurações Release da Rev 1 base e do piloto PT-BR passaram nos dois alvos do CTest com MSVC 19.44, Ninja 1.12.1, CTest 3.31.6 e Python 3.12.10. Os executáveis de teste foram compilados em diretórios novos, incluindo um caminho com espaços e acentos no piloto.

- `rev1_present` verificou a composição GDI em oito dimensões, a apresentação em 4:3 e preenchimento e 20 ciclos de tela cheia por monitor detectado.
- `rev1_python` executou os 59 testes do port em cada configuração, incluindo os sete testes de persistência com o auxiliar do próprio build.

O comando direto `python -m unittest discover -s tests` também passou com 59 testes. A configuração sem Python registrou apenas `rev1_present` e exibiu o aviso esperado. Com `BUILD_TESTING=OFF`, nenhum teste foi registrado. Logs locais em `evidence/2026-11-22/ctest-win32/`. [Comandos de reprodução](04-AMBIENTE-E-REPRODUCAO.md#testes-do-port-usa-rev-1-no-windows)

## Controle XInput (V12)

Em 2026-11-23, os builds Release da Rev 1 base e do piloto PT-BR no Windows passaram nos três alvos do CTest, incluindo os 59 testes Python por configuração. `rev1_gamepad` simulou ausência de controle, os 12 botões, diagonais e limite da zona morta, retomada após perda de foco, desconexão e reconexão no mesmo slot e em outro slot. Os executáveis importaram `XINPUT9_1_0.dll`. O teste de 600 quadros sem janela repetiu a imagem e o relatório de estado e áudio do build anterior em cada configuração.

Todos os quatro slots consultados pela biblioteca do Windows retornaram `ERROR_DEVICE_NOT_CONNECTED`. Em um ensaio de 17 segundos no piloto Win32 com teclado, iniciado com `--caverna` em um diretório isolado, o host completou 1.022 quadros e encerrou normalmente. A mediana entre apresentações ficou em 16,64 ms e houve sinal nas 1.040 leituras de pico da sessão de áudio.

A V12 segue aguardando um controle físico XInput. Os logs locais estão em `evidence/2026-11-23/xinput/`. [Mapeamento e roteiro com controle físico](11-TESTE-INTERATIVO.md#controle-xinput)

## Suíte pública do upstream

Em 2026-11-22, a P05 repetiu `python -B -m unittest discover -s tests -v` no DKC1Recomp v0.0.17. A revisão `559bab62596a97e91f389b39cdeb6cda981ab7c9` e os dois submódulos coincidiram com `config/upstream.lock.json`.

No Windows 10 22H2 com MSVC e Python 3.12.10, a repetição confirmou 303 testes contabilizados, dois erros e dez pulos. Os dois erros ocorreram na chamada ao compilador `cc` ausente, em `test_hd_material_cache` e na preparação de `test_hd_preload`. Os testes nativos de fila de temporização e cadência de apresentação passaram.

Com Clang 23.1.6 do LLVM MinGW UCRT, seis testes antes pulados passaram. A suíte no Windows terminou com 303 testes contabilizados, dois erros de ligação e quatro pulos. O LLD encontrou referências a `WsShadow*` e `Dkc1HdEnabled` que as linhas originais de ligação dos dois testes de HD deixam sem definição no Windows. Os quatro pulos abrangem dois testes de Metal, o adaptador de áudio do iOS e uma comparação que exige evidência local do SuperZSNES. Logs da suíte e do linker em `evidence/2026-11-22/p05-upstream/`. [Pacote portátil usado](https://github.com/mstorsjo/llvm-mingw/releases/tag/20261117)

No Ubuntu 24.04 do GitHub Actions, a mesma revisão foi testada com Clang 18.1.3, Python 3.12.3 e os sanitizers configurados para interromper em caso de erro. O cache de materiais e os nove casos de pré-carregamento HD passaram. A suíte terminou com **312 testes contabilizados, 307 aprovados e cinco pulos**. Os dois testes específicos de MSVC passaram no Windows. Dois testes de Metal dependem de macOS e a comparação de SuperZSNES depende do arquivo local `state5`. A suíte própria do port também passou com 59 testes no Windows. [Execução Ubuntu e log](https://github.com/rya3n/donkey-kong-country-pc/actions/runs/45086760504)

## Quando ampliar a cobertura

Depois da primeira entrega, incluir caverna, chuva e cordas, fase vertical, água, bônus, canhões, chefe e transições. Uma alteração em rotina compartilhada exige cobrir os cenários que ela alcança. Registrar os trechos exatos; não declarar compatibilidade com o jogo inteiro com base em uma fase.

Para widescreen, observar separadamente imagem central, margens, streaming, ativação de objetos e regras de gameplay. As exigências completas de promoção do upstream incluem determinismo, entradas limpas, comparação central e matriz de layouts; seguir o `upstream/AGENTS.md` antes de alterar esse código.

## Campanha e progresso real

Roteiro preparado em 2026-11-05 após o aceite dos modos de tela. A [primeira sessão do piloto PT-BR](31-INICIO-CAMPANHA-PT-BR.md) registra a execução de 2026-11-10. Usar o menu normal e identificar o build em cada sessão.

| Passo | O que registrar | Estado |
| --- | --- | --- |
| Ações e retorno | Movimento, troca de personagem, barris, morte, retorno e continuação | Ações da V06 verificadas em Jungle Hijinxs e escalada em Ropey Rampage. Reentrada pelo checkpoint confirmada nos cenários de V07. Em Tanked Up Trouble, o teste também registrou 23 abastecimentos da plataforma, saltos com pneus e retorno ao trilho pelos canhões |
| Progressão | Nome de cada fase concluída, saída, mapa, bônus e entrada seguinte | Rota principal validada até o encerramento. Foram verificadas as duas salas de Jungle Hijinxs, as duas de Ropey Rampage e as três de Reptile Rumble, com recompensas e retorno à fase. Os dois bônus de Barrel Cannon Canyon passaram desde o menu na versão base e no piloto PT-BR. [Sala do TNT](31-INICIO-CAMPANHA-PT-BR.md#segundo-bônus-de-barrel-cannon-canyon-v14) · [Primeiro bônus de Barrel Cannon Canyon](31-INICIO-CAMPANHA-PT-BR.md#primeiro-bônus-de-barrel-cannon-canyon-v14) · [Terceiro bônus de Reptile Rumble](31-INICIO-CAMPANHA-PT-BR.md#terceiro-bônus-de-reptile-rumble-v14) · [Sala dos canhões](31-INICIO-CAMPANHA-PT-BR.md#sala-dos-canhões-de-reptile-rumble-v14) · [Primeiro bônus de Reptile Rumble](31-INICIO-CAMPANHA-PT-BR.md#primeiro-bônus-de-reptile-rumble-v14) · [Bônus de Ropey Rampage](31-INICIO-CAMPANHA-PT-BR.md#salas-de-bônus-de-ropey-rampage-v14) · [Bônus de Jungle Hijinxs](31-INICIO-CAMPANHA-PT-BR.md#primeira-sala-de-bônus-de-jungle-hijinxs-v14) · [Final da campanha](32-CAMPANHA-PT-BR-AUDIO-E-PROGRESSO.md#gang-plank-galleon-e-final-da-campanha) |
| Variedade e chefes | Água, chuva, cavernas, cordas, canhões, chefes e transições entre mundos | Chuva, cordas, caverna, água, canhões e carrinho exercitados. Very Gnawty e Master Necky derrotados com transição para o próximo mundo |
| Saves com progresso real | Selecionar o slot, salvar na Candy, fechar normalmente, reabrir e conferir o mesmo arquivo | Confirmado em Kongo Jungle e Gorilla Glacier. Em Gorilla Glacier, o slot 1 voltou com 00:28 e 21%. [Roteiro e evidências](32-CAMPANHA-PT-BR-AUDIO-E-PROGRESSO.md#salvamento-da-candy-em-gorilla-glacier) |
| Final da campanha | Chefe final, encerramento/créditos e estado recuperado após reabrir | Dez golpes contra King K. Rool, créditos falsos e reais, retorno automático ao título e carregamento a frio do slot 1 com 00:54 e 34%. Ensaio sem janela. [Relatório e roteiro](32-CAMPANHA-PT-BR-AUDIO-E-PROGRESSO.md#gang-plank-galleon-e-final-da-campanha) |

Para cada sessão, anotar versão, fases percorridas, modo de tela e defeitos observados. Testar a persistência em momentos diferentes da progressão; identificar e proteger a cópia do save antes de qualquer teste de migração ou falha. Não substituir o progresso pessoal por fixtures de QA. Percurso principal, bônus e eventuais caminhos não percorridos devem ter sua cobertura indicada separadamente.

Corrigir e repetir qualquer cenário com defeito crítico antes de aceitar V14. O [piloto PT-BR](30-DIALOGOS-CRANKY-PT-BR.md) está em validação. Suporte a controle físico, save states e pacote final continuam em seus próprios marcos.

## Como registrar defeitos

Título com sintoma observável; ROM/build; cenário; passos; comportamento esperado e observado; primeiro frame conhecido; artefatos; reprodução após entrada limpa; hipótese separada de causa comprovada. Um defeito só pode ser chamado de corrigido após repetir o caso e verificar os cenários relacionados.

## Leitura correta dos resultados

Integridade do ZIP verifica o download. Compilação bem-sucedida verifica a produção do binário. Testes de modelos verificam contratos específicos. Execução headless verifica os estados que ela mede. A inspeção da janela e do áudio verifica a experiência visível. São evidências complementares, com limites diferentes.

## Validação da meta final

Estes critérios propostos dão forma verificável à meta de PT-BR e abertura direta, acordada após a documentação inicial:

| ID | Verificação | Aceitação proposta |
| --- | --- | --- |
| V14 | Campanha e estabilidade da base | Percurso completo registrado, com chefes, bônus, transições, mortes, áudio e saves; sem defeitos críticos conhecidos na cobertura aceita |
| V15 | Cobertura da tradução | Inventário de textos e telas conferido contra a versão PT-BR, com exceções explicitadas |
| V16 | Qualidade linguística e visual | Revisão em contexto, acentos corretos, texto legível e sem cortes ou estouros de caixas |
| V17 | Regressão da tradução | Rotas, progressão, áudio e persistência continuam corretos após a localização |
| V18 | Abertura direta | Após a preparação inicial definida, abrir o executável inicia o jogo sem terminal ou nova seleção de ROM. [Ensaio das compilações atuais](#abertura-direta-no-windows-v18) |
| V19 | Pacote de aplicativo | Testar em ambiente Windows sem ferramentas de desenvolvimento, incluindo caminho com espaços/acentos, saves e preferências entre sessões. [Preferência de imagem validada nos builds locais](#preferência-de-imagem-no-windows-v19) |

A V15 avançou na auditoria dos 346 registros do catálogo parcial. O manifesto do piloto cobre os 217 intervalos de diálogos. As demais telas e falas seguem em revisão em contexto. [Resultado da auditoria V15](15-PT-BR.md#auditoria-de-cobertura-do-piloto-v15)

Na V16, o título **SALVAR COM A CANDY** passou na revisão em tela. O teste confirmou que a alteração visual ficou na faixa do título, que a volta ao mapa e os saves coincidiram e que a reabertura a frio funcionou. A diferença digital de áudio da V17 após confirmar o slot ficou igual à medida no piloto anterior. [Teste e limites](15-PT-BR.md#título-integrado-no-piloto)

Os sete registros dos créditos do navio passaram na revisão em jogo. A rolagem preservou a posição das atribuições, e a luta retomou até o encerramento com o mesmo save final. [Créditos do navio](15-PT-BR.md#créditos-do-navio-em-pt-br)

Os 25 registros dos créditos reais também passaram. O teste encontrou todos os rótulos traduzidos no buffer de sprites, confirmou o desenho do **ã**, a posição das linhas de atribuição, o retorno ao título e o mesmo save final. O teste retomou um estado isolado no fim da luta. [Créditos reais](15-PT-BR.md#créditos-reais-em-pt-br)

A revisão da apresentação do elenco conferiu os 47 registros em jogo. Os sete títulos e quatro falas apareceram completos e os 36 nomes coincidiram em grafia, ordem e posição. O trecho comparado retomou um estado de QA e confirmou a rolagem dos créditos seguintes, o retorno ao título e o mesmo save final. [Apresentação do elenco](15-PT-BR.md#apresentação-do-elenco-em-pt-br)

Na seleção de jogadores, o brilho acompanha os três modos em PT-BR. A revisão também conferiu os três slots, a exclusão em perfil isolado e a entrada em Kongo Jungle em cada modo. [Validação dos menus](16-PILOTO-PT-BR.md#revisão-da-seleção-de-jogo-e-de-jogadores)

As nove revisitas do Funky foram conferidas com seleção normal do jogo. O ensaio cobriu a dupla, Donkey sozinho e Diddy sozinho em Funky's Flights de Monkey Mines, com viagem a Kongo Jungle para cada composição. [Revisitas do Funky](28-FUNKY-FALAS-COMPLETAS.md#revisão-em-contexto-em-funkys-flights)

A revisão das saudações do Cranky separou a seleção normal de 31 variantes na cabana da renderização individual dos 41 textos do catálogo. A saudação comum a Diddy sozinho e à dupla foi ajustada para as duas situações. [Saudações do Cranky](29-SAUDACOES-COMPLETAS-CRANKY-PT-BR.md#revisão-em-contexto-na-cabana)

Nos retornos à cabana, as 11 falas apareceram para Diddy, Donkey e a dupla. A revisão conferiu 33 entradas, a passagem para uma dica e o retorno ao mapa. [Retornos do Cranky](27-RETORNO-RAPIDO-CRANKY-PT-BR.md#revisão-em-contexto-no-retorno-à-cabana)

As 31 dicas gerais da tabela normal apareceram na sequência da cabana. O comparador conferiu os 32 textos catalogados, incluindo a dica de Gnawty, que fica fora da tabela normal. [Dicas gerais do Cranky](30-DIALOGOS-CRANKY-PT-BR.md#dicas-gerais-em-contexto-na-cabana)

As 31 despedidas da tabela normal apareceram após a dica geral. Os 32 textos passaram no comparador, e a saída automática e a saída com Start voltaram ao mapa. [Despedidas do Cranky](30-DIALOGOS-CRANKY-PT-BR.md#despedidas-em-contexto-na-cabana)

As 37 reclamações apareceram em sete visitas de Diddy à cabana, com avanço automático das falas. Duas amostras passaram com Donkey e duas com a dupla em revisita. O ensaio confirmou a passagem para a dica de fase e o retorno ao mapa. As 37 falas também passaram no comparador. [Reclamações do Cranky](30-DIALOGOS-CRANKY-PT-BR.md#reclamações-em-contexto-na-cabana)

A V17 comparou 6.500 quadros de PCM no ensaio da Candy. Na volta ao mapa, o deslocamento ficou entre 0,62 e 1,25 ms nas janelas medidas. Nenhum quadro ficou silencioso em apenas um build. A escuta no dispositivo segue pendente. [Medição](32-CAMPANHA-PT-BR-AUDIO-E-PROGRESSO.md#diferença-digital-após-salvar-na-candy-v17)

A preparação inicial, se necessária, deve ser testada separadamente da abertura habitual. A validação do pacote final precisa acontecer na configuração exata que será usada pelo jogador.

## Abertura direta no Windows (V18)

Em 2026-11-23, os executáveis Windows GUI x64 da Rev 1 base e do piloto PT-BR foram iniciados sem argumentos e com diretório de trabalho diferente da pasta do executável. Cada combinação de build e estrutura foi iniciada duas vezes, totalizando oito execuções. A primeira abriu o áudio, processou entre 65 e 66 quadros e encerrou normalmente. A segunda carregou um save de QA e confirmou que o arquivo de 2.048 bytes e seu backup continuaram idênticos. As pastas de teste usaram espaços e acentos.

| Estrutura testada | ROM encontrada | Perfil de save |
| --- | --- | --- |
| Cópia da árvore de trabalho com executável em `build/` | Raiz da cópia, dois níveis acima do executável | `data/` na raiz da cópia |
| Pasta portátil preparada | Mesmo diretório do executável | `data/` ao lado do executável |

Os builds passaram nos três alvos do CTest, com 65 testes Python por configuração. A inspeção dos executáveis listou apenas bibliotecas do sistema Windows como dependências diretas. A resolução de caminhos usa a API PathCch. [Documentação da Microsoft](https://learn.microsoft.com/en-us/windows/win32/api/pathcch/nf-pathcch-pathcchremovefilespec)

Os perfis e logs do ensaio ficam em `evidence/2026-11-23/v18-abertura/`. A V18 foi verificada nestas compilações locais. A abertura e o progresso precisam ser repetidos no pacote final em um Windows sem ferramentas de desenvolvimento na V19.

## Preferência de imagem no Windows (V19)

Em 2026-11-23, a versão base e o piloto PT-BR recuperaram a escolha entre Preencher e 4:3. O ensaio executou 16 sessões normais, combinando os dois builds com a estrutura do projeto e uma pasta portátil, com espaços e acentos. O arquivo de preferência só foi atualizado nas sessões em que o modo mudou. O save de QA e o backup permaneceram idênticos.

Três ensaios adicionais verificaram a abertura em Preencher com arquivo inválido, a preservação do valor anterior quando a substituição do arquivo foi bloqueada e o isolamento de `--jungle`. Os executáveis de teste foram iniciados com apenas pastas do Windows no `PATH`. O computador de teste tem ferramentas de desenvolvimento instaladas. Os três alvos do CTest passaram nos dois builds, com 65 testes Python por configuração. Evidências em `evidence/2026-11-23/v19-preferencias/`. O ensaio do pacote final em Windows sem ferramentas de desenvolvimento segue na V19.

## Inspeção do executável portátil (V19)

Em 2026-11-23, as cópias portáteis do [ensaio de preferências](#preferência-de-imagem-no-windows-v19) foram comparadas pelo SHA-256 com os executáveis da pasta de build. A Rev 1 base tem 605.184 bytes e o piloto PT-BR tem 667.136 bytes. Ambos são PE x64 com subsistema gráfico e listaram as mesmas sete importações diretas.

Seis bibliotecas estavam presentes no diretório de sistema do Windows desse computador. A sétima, `api-ms-win-core-path-l1-1-0.dll`, é um contrato resolvido pelo carregador do sistema. O relatório encontrou zero DLLs ao lado dos executáveis e zero importações diretas do redistribuível do Visual C++. Essa inspeção registra as dependências do binário no computador de build. [DUMPBIN /DEPENDENTS](https://learn.microsoft.com/en-us/cpp/build/reference/dependents?view=msvc-170) · [Carregamento de API sets](https://learn.microsoft.com/en-us/windows/win32/apiindex/api-set-loader-operation)

No PowerShell de desenvolvedor x64, use o script na raiz do projeto. Passe `-ExpectedSha256` para conferir uma cópia contra o hash de referência. Se o DUMPBIN estiver fora do `PATH`, informe o caminho instalado com `-Dumpbin`.

```powershell
.\scripts\inspect_windows_executable.ps1 -Executable '.\build\ptbr-pilot\DKC-Rev1-PTBR-Piloto.exe'
```

O script foi testado em PowerShell 7. Rejeitou um executável de console, um arquivo truncado e uma divergência de hash. Relatórios locais em `evidence/2026-11-23/v19-pacote/`.

### Ensaio do pacote em Windows sem ferramentas de desenvolvimento

1. Registrar versão, build e arquitetura do Windows. Conferir o SHA-256 do executável entregue com `Get-FileHash -LiteralPath 'CAMINHO_DO_EXECUTAVEL' -Algorithm SHA256` e comparar com o relatório da compilação escolhida para o pacote.
2. Preparar uma pasta de QA gravável com espaços e acentos. Usar a ROM local USA Rev 1 ao lado do executável, conforme o [guia de abertura direta](11-TESTE-INTERATIVO.md#abrir-direto-pelo-executável). A pasta de teste deve ter um perfil novo.
3. Abrir o executável pelo Explorador. Conferir abertura sem terminal ou seletor de ROM, chegada ao menu, áudio durante a partida, comandos de teclado e troca de proporção com F6.
4. Jogar até salvar na Candy e fechar normalmente. Reabrir pelo Explorador, retomar o slot salvo e conferir a proporção escolhida. Conferir o `save.srm` e o backup em `data/<perfil>/saves/`.
5. Registrar o hash testado, o caminho de instalação, o resultado de cada etapa, a localização recuperada e eventuais falhas.

O ensaio final segue pendente. A inspeção local complementa os testes da V18 e da preferência de imagem. A aceitação da V19 exige execução no Windows de destino com o pacote final identificado.
