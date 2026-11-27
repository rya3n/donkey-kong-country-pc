# Etapas e pendências

Plano inicial de 2026-11-04, sem datas de entrega assumidas. Os marcos abaixo organizam o trabalho; não representam versões já lançadas.

## Sequência proposta

| Marco | Entrega | Condição para concluir |
| --- | --- | --- |
| M0 — Documentação | Visão, diagnóstico, decisões e log organizados | Documentos coerentes, links conferidos e leitura do usuário |
| M1 — Base reproduzível | ROM, código, engine e compilador identificados | Hash compatível e ferramentas confirmadas |
| M2 — Compilação local | Binário produzido e testes registrados | Logs completos, hashes e bloqueios resolvidos ou delimitados |
| M3 — Primeira sessão jogável | Boot até fase, interação e saída | Cenários iniciais aceitos com evidências |
| M4 — Persistência e cobertura | Saves e variedade de cenas | Matriz executada com limites explícitos |
| M5 — Publicação | Repositório e instruções utilizáveis | Arquivos de publicação conferidos, créditos e reprodução claros |
| M6 — Tradução PT-BR | Jogo localizado após a aceitação da base estável | Inventário, revisão em contexto e regressão da tradução concluídos |
| M7 — Aplicativo Windows | Abrir o executável e jogar | Pacote testado sem ferramentas de desenvolvimento, com saves persistentes e sem configuração repetida |

O usuário priorizou M0 e a criação do GitHub público. Depois, pediu começar com a USA Rev 1 disponível. M1 foi estabelecido para esse perfil experimental e M2 tem um primeiro executável sem janela; M3 e os marcos de validação continuam abertos. Resultados em [Protótipo USA Rev 1](10-USA-REV1-BRINGUP.md).

## Pendências acionáveis

| ID | Ação | Estado | Dependência e resultado esperado |
| --- | --- | --- | --- |
| P01 | Revisar a documentação inicial | Concluída para início técnico | Onze páginas do Notion revisadas; estado atual, bloqueio e roteiro atualizados |
| P02 | Identificar a ROM de trabalho | Concluída para Rev 1; escopo alterado em D011 | USA v1.1 local validada por tamanho/hash; v1.0 deixou de ser pré-requisito do alvo próprio |
| P03 | Selecionar revisão de código/engine | Concluída | v0.0.17 e os três commits conferidos contra config/upstream.lock.json |
| P04 | Confirmar ambiente C/CMake | Concluída a verificação básica | MSVC/CMake/Ninja no E:, SDK funcional e programa mínimo compilado e executado |
| P05 | Repetir suíte com logs completos | Concluída com resultados por ambiente | Ubuntu: 307 aprovados e cinco pulos justificados. Windows: os testes de temporização e cadência passaram, e os dois erros de ligação HD foram reproduzidos. [Resultados e logs](05-VALIDACAO.md#suíte-pública-do-upstream) |
| P06 | Gerar fontes e compilar | Concluída para protótipo sem janela | 39 variantes AOT e interpretador de apoio; MSVC/CMake/Ninja, comandos e hashes registrados |
| P07 | Validar a primeira sessão | Sessão humana realizada e ações da V06 verificadas | Boot, entrada na fase e fluidez confirmados. A versão base e o piloto repetiram as ações de Jungle Hijinxs. A escuta em janela foi verificada em Reptile Rumble na V09. [Áudio em janela](32-CAMPANHA-PT-BR-AUDIO-E-PROGRESSO.md#áudio-em-janela-na-caverna) [Roteiro de ações](31-INICIO-CAMPANHA-PT-BR.md#rolamento-barril-dk-e-troca-de-personagem-v06) |
| P08 | Validar persistência | Aprovada na Candy de Kongo Jungle, Monkey Mines e Gorilla Glacier | O progresso foi carregado em novos processos, com backup idêntico. Em Monkey Mines, o slot 1 reabriu na Candy e permitiu seguir até a arena de Master Necky. Em Gorilla Glacier, o slot 1 recuperou 00:28 e 21%. [Relatório da campanha](32-CAMPANHA-PT-BR-AUDIO-E-PROGRESSO.md#visitas-de-serviço-em-monkey-mines) |
| P09 | Criar repositório público | Concluída a publicação inicial da documentação | Destino: rya3n/donkey-kong-country-pc; visibilidade pública e 12 arquivos conferidos pela API |
| P10 | Validar campanha e estabilidade | Rota principal repetida em três processos sem janela | V13 aprovada. Luta final, créditos, retorno ao título e recuperação a frio do slot 1 foram reproduzidos. As visitas a Candy, Funky e Cranky em Monkey Mines foram verificadas. Os sete bônus de Jungle Hijinxs, Ropey Rampage e Reptile Rumble foram confirmados com recompensas e retorno à fase. Os dois bônus de Barrel Cannon Canyon passaram desde o menu na versão base e no piloto PT-BR. Na segunda sala, o disparo central rendeu dez bananas e uma vida com retorno ao controle. Os disparos laterais foram ensaiados a partir do canhão. Em Reptile Rumble, a base e o piloto passaram na medição em janela e a escuta confirmou som sem cortes durante o movimento. DKC-BUG-5 segue em investigação. [Sala do TNT](31-INICIO-CAMPANHA-PT-BR.md#segundo-bônus-de-barrel-cannon-canyon-v14) · [Primeiro bônus de Barrel Cannon Canyon](31-INICIO-CAMPANHA-PT-BR.md#primeiro-bônus-de-barrel-cannon-canyon-v14) · [Terceiro bônus de Reptile Rumble](31-INICIO-CAMPANHA-PT-BR.md#terceiro-bônus-de-reptile-rumble-v14) · [Sala dos canhões](31-INICIO-CAMPANHA-PT-BR.md#sala-dos-canhões-de-reptile-rumble-v14) · [Primeiro bônus de Reptile Rumble](31-INICIO-CAMPANHA-PT-BR.md#primeiro-bônus-de-reptile-rumble-v14) · [Bônus de Ropey Rampage](31-INICIO-CAMPANHA-PT-BR.md#salas-de-bônus-de-ropey-rampage-v14) · [Bônus de Jungle Hijinxs](31-INICIO-CAMPANHA-PT-BR.md#primeira-sala-de-bônus-de-jungle-hijinxs-v14) · [Visitas em Monkey Mines](32-CAMPANHA-PT-BR-AUDIO-E-PROGRESSO.md#visitas-de-serviço-em-monkey-mines) · [Áudio em janela](32-CAMPANHA-PT-BR-AUDIO-E-PROGRESSO.md#áudio-em-janela-na-caverna) |
| P11 | Inventariar, traduzir e revisar PT-BR | 217 intervalos de diálogos conferidos, título da Candy e 79 registros de elenco e créditos verificados | Candy 8, Funky 13 e Cranky 196. Os 50 nomes do mapa e 36 do elenco foram preservados. As demais telas e falas seguem na revisão em contexto da V15–V16. [Auditoria de cobertura](15-PT-BR.md#auditoria-de-cobertura-do-piloto-v15) · [Apresentação do elenco](15-PT-BR.md#apresentação-do-elenco-em-pt-br) · [Créditos finais](15-PT-BR.md#créditos-reais-em-pt-br) |
| P12 | Preparar aplicativo Windows | Abertura, saves, preferência do F6 e dependências diretas conferidos nos builds locais | A V19 tem um relatório reproduzível de arquitetura, hash e DLLs. Falta executar o pacote final em Windows sem ferramentas de desenvolvimento. [Inspeção e roteiro](05-VALIDACAO.md#inspeção-do-executável-portátil-v19) |
| P13 | Investigar divergência ao ampliar AOT | Aberta; candidata retirada | Localizar primeira diferença de WRAM/áudio entre 39 e 55 variantes antes de promover cobertura |
| P14 | Implementar host interativo Rev 1 | Implementado; primeiro teste realizado | Usuário testou as primeiras fases e relatou perda de fluidez na caverna; bateria completa de ações ainda pendente |
| P15 | Corrigir fluidez sem acelerar a simulação | Correção medida e confirmada pelo usuário | Ajuste aceito no teste humano; 40 entradas amostradas, sem validação de campanha completa |
| P16 | Corrigir piscadas pretas em todas as cenas | Correção confirmada pelo usuário | Usuário informou que a tela parou de piscar após 7043b6d |
| P17 | Adaptar imagem e tela cheia ao monitor | Funcionamento confirmado pelo usuário | Aceite após e46f8f1; não estende a cobertura a todos os monitores ou computadores |
| P18 | Localizar menus/fontes e criar piloto PT-BR | Correção do destaque verificada em captura. Aceite ao vivo pendente | A matriz confirmou os três slots, o fluxo de exclusão em QA e a seleção e entrada nos três modos. [Validação dos menus](16-PILOTO-PT-BR.md#revisão-da-seleção-de-jogo-e-de-jogadores) |
| P19 | Integrar primeiras falas da Candy | Implementado; prévias aprovadas pelo usuário | Apresentação e instrução incluídas no aceite das oito capturas em 2026-11-06 |
| P20 | Completar falas identificadas da Candy | Concluído no escopo das oito falas e prévias | Redação e leitura aprovadas pelo usuário em 2026-11-06; QA anterior preservado; campanha continua em P10 |
| P21 | Integrar falas identificadas do Funky | Implementado; correção de fonte aceita em relato | Quatro mensagens e restrição do Jumbo Barrel preservadas; correção do ê incluída no aceite da entrega seguinte |
| P22 | Integrar primeiro lote do Cranky e corrigir ê | Aceite em relato do usuário | Usuário confirmou satisfação com a entrega e autorizou as dicas em 2026-11-06; demais condições de gameplay continuam pendentes |
| P23 | Integrar dicas de Kongo Jungle | Implementado; revisão humana pendente | Cinco fases, pistas e nomes preservados; fonte e regiões anteriores idênticas; conferir relatório 21 |
| P24 | Integrar dicas de Monkey Mines | Implementado; revisão humana pendente | Quatro dicas, nomes completos e pistas mantidos; 32 regiões anteriores idênticas; conferir relatório 22 |
| P25 | Integrar dicas de Vine Valley | Implementado; revisão humana pendente | Grupo identificado em 0x3C01D4–0x3C01E4; três dicas, nomes completos e pistas mantidos; 36 regiões anteriores idênticas; conferir relatório 23 |
| P26 | Integrar dicas de Gorilla Glacier | Implementado; revisão humana pendente | Cinco dicas em 0x3C01A4–0x3C01B4, nomes completos e pistas mantidos; 39 regiões anteriores idênticas; conferir relatório 24 |
| P27 | Integrar dicas de Kremkroc Industries Inc. | Implementado; revisão humana pendente | Cinco dicas em 0x3C01B4–0x3C01C4, nomes completos, Gnawty e pistas mantidos; 44 regiões anteriores idênticas; conferir relatório 25 |
| P28 | Integrar dicas de Chimp Caverns | Implementado; revisão humana pendente | Cinco dicas em 0x3C01C4–0x3C01D4, fechando as 27 dicas dos seis mundos; 49 regiões anteriores idênticas; conferir relatório 26 |
| P29 | Integrar falas de retorno rápido do Cranky | 11 falas conferidas em contexto | Cinco redações ajustadas. As três composições passaram pelas 11 variantes, pela dica seguinte e pela volta ao mapa. [Resultados](27-RETORNO-RAPIDO-CRANKY-PT-BR.md#revisão-em-contexto-no-retorno-à-cabana) |
| P30 | Completar falas identificadas do Funky | Nove revisitas verificadas em contexto | Cinco falas da dupla, duas de Donkey sozinho e duas de Diddy sozinho. Quatro redações ajustadas, treze falas renderizadas no comparador e acesso a Kongo Jungle testado. [Resultados](28-FUNKY-FALAS-COMPLETAS.md#revisão-em-contexto-em-funkys-flights) |
| P31 | Completar saudações do Cranky | 31 variantes conferidas em contexto e 41 textos renderizados | Cinco redações ajustadas. Dez textos ficam fora da tabela normal de saudação da Rev 1 e passaram no comparador individual. [Resultados](29-SAUDACOES-COMPLETAS-CRANKY-PT-BR.md#revisão-em-contexto-na-cabana) |
| P32 | Integrar as 117 falas restantes do Cranky | Implementado, com revisão humana pendente | Finais, dicas gerais, despedidas e reclamações. Conferir relatório 30 |

Não há responsáveis individuais ou prazos atribuídos além do contexto da conversa. Cada execução deve acrescentar resultados ao diagnóstico e ao log.

A meta posterior acordada é PT-BR e abertura direta. A publicação inicial de documentação não conclui os marcos de estabilidade do jogo. Antes de M6, executar a campanha e aceitar a cobertura ampliada; depois revisar a tradução e testar o pacote final. A técnica de tradução e o formato de distribuição ainda serão definidos.

## Riscos técnicos atuais

- Rev 1 tem configuração própria ainda incompleta; muitos caminhos continuam no interpretador de apoio.
- A ampliação de AOT mudou WRAM e áudio; imagem final igual não permite aceitar a candidata.
- A base sem janela ainda não foi comparada com hardware ou referência independente; determinismo não comprova exatidão.
- A v0.0.17 do upstream ainda tem dois erros de ligação nos testes HD em Windows com LLVM MinGW. Esses casos passaram no Ubuntu. [Relatório da P05](05-VALIDACAO.md#suíte-pública-do-upstream)
- O upstream mantém recursos experimentais: ativá-los cedo dificulta separar defeitos da base de mudanças do projeto.
- Evidências iniciais sem log integral têm menor rastreabilidade: novas execuções precisam arquivar comandos e saídas.
