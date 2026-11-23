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
| V06 | Movimento e interação | Mover, pular, rolar, resgatar Diddy, trocar e usar barril | Parcial. Corrida, salto, barris de checkpoint e de parceiro em Jungle Hijinxs, escalada em Ropey Rampage e movimento durante as alternâncias de iluminação em Blackout Basement |
| V07 | Morte e retorno | Ciclo completo sem travamento e com estado coerente | Retorno ao mapa e nova entrada confirmados em Jungle Hijinxs. Reentrada pelo checkpoint confirmada em Croctopus Chase, Torchlight Trouble, Rope Bridge Rumble, Oil Drum Alley, Trick Track Trek, Elevator Antics, Poison Pond, Mine Cart Madness, Blackout Basement, Tanked Up Trouble, Manic Mincers, Misty Mine, Loopy Lights e Platform Perils |
| V08 | Concluir fase e voltar ao mapa | Saída, transição e progressão corretas | Rota principal validada até Gang-Plank Galleon. O chefe final foi derrotado e o jogo voltou à tela de título após os créditos |
| V09 | Áudio e apresentação | Trecho identificado sem cortes persistentes ou defeitos visíveis | Seis rodadas do piloto na caverna tiveram sinal em todas as 6.239 leituras. A interrupção longa permaneceu restrita ao ensaio anterior. DKC-BUG-5 em investigação e escuta no dispositivo pendente. [Diagnóstico](32-CAMPANHA-PT-BR-AUDIO-E-PROGRESSO.md#repetição-no-piloto-e-diagnóstico-da-espera) |
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
| Ações e retorno | Movimento, troca de personagem, barris, morte, retorno e continuação | Cobertura parcial em Jungle Hijinxs e Ropey Rampage. Reentrada pelo checkpoint confirmada nos cenários de V07. Em Tanked Up Trouble, o teste também registrou 23 abastecimentos da plataforma, saltos com pneus e retorno ao trilho pelos canhões |
| Progressão | Nome de cada fase concluída, saída, mapa, bônus e entrada seguinte | Rota principal validada até o encerramento. A cobertura dos bônus permanece parcial. [Relatório e roteiro](32-CAMPANHA-PT-BR-AUDIO-E-PROGRESSO.md#gang-plank-galleon-e-final-da-campanha) |
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
| V18 | Abertura direta | Após a preparação inicial definida, abrir o executável inicia o jogo sem terminal ou nova seleção de ROM |
| V19 | Pacote de aplicativo | Testar em ambiente Windows sem ferramentas de desenvolvimento, incluindo caminho com espaços/acentos, saves e preferências entre sessões |

Todos estão pendentes. A preparação inicial, se necessária, deve ser testada separadamente da abertura habitual. A validação do pacote final precisa acontecer na configuração exata que será usada pelo jogador.
