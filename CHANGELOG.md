# Log de atualizações

As datas deste histórico usam o fuso America/Sao_Paulo. As entradas mais recentes ficam no início. Este log registra o nosso projeto; as versões do DKC1Recomp são identificadas como versões de terceiros.

## 2026-11-13 — Bouncy Bonanza concluída

- Validada a travessia desde o menu, com cinco vidas preservadas em Bouncy Bonanza. O roteiro passa pelo túnel inferior, pelos Zingers e pela plataforma móvel final.
- Confirmado o retorno a Monkey Mines com Stop & Go Station selecionada no quadro 50.529. Passaram os 59 testes Python. [Roteiro e reprodução](docs/32-CAMPANHA-PT-BR-AUDIO-E-PROGRESSO.md#saída-de-bouncy-bonanza).

## 2026-11-13 — Rota contínua até Bouncy Bonanza

- Ajustados os comandos de salto em Mine Cart Carnage. A repetição desde o menu em perfil novo, sem snapshots, confirmou o mapa de Monkey Mines no quadro 45.981 e a abertura de Bouncy Bonanza no quadro 46.272, com cinco vidas e 40 bananas.
- O piloto headless reproduziu a mesma imagem final do coletor de QA. Passaram os 59 testes Python. [Roteiro e reprodução](docs/32-CAMPANHA-PT-BR-AUDIO-E-PROGRESSO.md#roteiro-contínuo-até-bouncy-bonanza).

## 2026-11-12 — Revisão do roteiro de Monkey Mines

- Publicada a sequência de 40.473 quadros desde o menu até Mine Cart Carnage. Repetidos o salvamento com progresso real na Candy e a recuperação da mesma SRAM em processos novos headless e Win32, com backup idêntico. Passaram 59 testes Python.
- O roteiro local de 45.948 quadros repete os hashes anteriores, mas termina na área inicial de Mine Cart Carnage. A chegada a Bouncy Bonanza foi confirmada em execução separada a partir de snapshot. A rota contínua pelo carrinho precisa ser consolidada. [Relatório e reprodução](docs/32-CAMPANHA-PT-BR-AUDIO-E-PROGRESSO.md).

## 2026-11-12 — Mine Cart Carnage concluída e chegada em Bouncy Bonanza

- Exploração de **Mine Cart Carnage** com pontos de restauração. A rota de QA chegou à saída com 6 vidas e 37 bananas.
- Sequência complexa de trilhos superada: transferência dos saltos 41 e 42 calculada para aterrissar do trilho superior quebrado diretamente no carrinho que corre pelo trilho inferior (câmera ~17.000).
- Salto final 45 (espera de 138 quadros, pulo de 35 quadros) executado no quadro 45.428, ejetando o Kong do carrinho diretamente para a área de saída sem colisão com o batente do trilho.
- A partir do snapshot do salto 44, retorno ao mapa de **Monkey Mines** e chegada diante de **Bouncy Bonanza** no quadro 45.948.
- A sequência local `campaign-to-bouncy-bonanza.inputs` foi arquivada como tentativa. A revisão acima registra a divergência observada ao reproduzir desde o menu.
- Documentação sincronizada em `Etapas e pendências`, `Repasse para o Gemini` (Notion) e arquivos locais do projeto.

## 2026-11-12 — Winky's Walkway concluída e entrada em Mine Cart Carnage

- **Winky's Walkway** (Mundo 2, Fase 1) 100% concluída de forma totalmente determinística. 15 obstáculos superados sem sofrer qualquer dano: saltos precisos sobre abismos, plataformas suspensas, sequências de Neckys e rolamentos contra Kritters.
- Salto final executado a partir da plataforma superior (quadro 39.558) para a rampa final de madeira (quadro 39.607). Coleta de bananas na subida e ativação do barril de saída no quadro 39.757 com 4 vidas intactas e 72 bananas.
- Dança da vitória do Diddy com rádio boombox e fanfarra de encerramento da fase. Fade-out e retorno ao mapa de **Monkey Mines** (`entrance=002e`, `scene=0006`) no quadro 39.997.
- Caminhada automática dos Kongs pela trilha do mapa concluída com parada no ponto de **Mine Cart Carnage** no quadro 40.092.
- Acionamento da entrada com botão B no quadro 40.093. Carregamento completo do estágio (`scene=0005`, `camera=17`) verificado no quadro 40.178 / 40.473.
- Roteiro determinístico consolidado e verificado com sucesso desde o cold boot (quadro 0 a 40.473) no arquivo `evidence/2026-11-10/pt-BR/campaign-start/campaign-to-mine-cart-carnage.inputs` (40.473 quadros).
- Documentação sincronizada em `Etapas e pendências`, `Repasse para o Gemini` e arquivos locais do projeto.

## 2026-11-12 — Derrota de Very Gnawty e entrada em Monkey Mines

- Chefe Very Gnawty (Mundo 1) derrotado na arena com Donkey Kong: 5 acertos consecutivos sem sofrer dano (quadro 36.510). Evasão da investida mortal do chefe executada com salto no quadro 36.570, preservando todas as 4 vidas de Donkey Kong.
- Queda e coleta da banana gigante no quadro 36.870, fanfarra de vitória de fim de mundo e fade-out no quadro 37.136. Transição pelo mapa geral da ilha (`entrance=00ec`) até o mapa de Monkey Mines (`entrance=00ed`) no quadro 37.241.
- Posição estabilizada no mapa de Monkey Mines no quadro 37.620 com 4 vidas intactas e 55 bananas.
- Entrada na primeira fase de Monkey Mines (**Winky's Walkway**, `entrance=00d9`) executada com botão B.
- Roteiro integral determinístico desde o boot frio consolidado em `evidence/2026-11-10/pt-BR/campaign-start/campaign-to-monkey-mines.inputs` (37.620 quadros).
- Documentação sincronizada em `docs/32-CAMPANHA-PT-BR-AUDIO-E-PROGRESSO.md`, `docs/06-ETAPAS-E-PENDENCIAS.md`, `.project-local.md` e páginas do Notion.

## 2026-11-11 — Barrel Cannon Canyon, Candy e Persistência a Frio

- **Barrel Cannon Canyon:** Sequência de canhões móveis e obstáculos de chão superados até a caverna de saída. Fase concluída no quadro 34.466 com 4 vidas preservadas.
- **Candy's Save Point:** Visita via navegação no mapa de Kongo Jungle no quadro 34.818. Diálogo da Candy em PT-BR conferido e salvamento efetuado no quadro 35.218.
- **Persistência a Frio (Cold Save):** Validação executada via `audio-driver/cold_save.py` no perfil `gemini-clean-cold-report`. SRAM gravada em `saves/save.srm` com exatamente 2.048 bytes e SHA-256 `72d519d25cce21886142567427185942b8f2480ee9c7f0a7d912730830ea3207`. Backup automático `save.srm.bak` idêntico gerado na abertura. Hashes de framebuffer, WRAM e SRAM rigorosamente idênticos entre o runner headless e o aplicativo desktop Win32 (`DKC-Rev1-PTBR-Piloto.exe`).
- Roteiro consolidado em `evidence/2026-11-10/pt-BR/campaign-start/campaign-to-candy.inputs` (35.218 quadros desde o boot limpo).

## 2026-11-10 — Início da campanha PT-BR

- Repetida a rota desde um perfil vazio, com morte, retorno ao mapa, nova entrada e conclusão de Jungle Hijinxs e Ropey Rampage.
- Visitada a cabana do Cranky pelo mapa. Conferidas a saudação, a dica de Coral Capers, a dica do superpulo e a despedida em PT-BR. O roteiro termina na entrada de Reptile Rumble.
- No retorno ao mapa de Jungle Hijinxs, as versões inglesa e PT-BR apresentaram o mesmo framebuffer, WRAM, SRAM e hash acumulado de áudio. [Relatório 31](docs/31-INICIO-CAMPANHA-PT-BR.md).
- Na entrada da caverna, as imagens e os estados de memória coincidiram. A diferença no áudio acumulado do percurso até esse ponto ficou registrada para investigação. Passaram 59 testes Python.

## 2026-11-10 — Inventário inglês de diálogos integrado ao piloto

- Integradas 117 falas do Cranky entre finais, dicas gerais, despedidas e reclamações. O piloto reúne 217 diálogos para USA Rev 1.
- Restaurada a referência a rinocerontes na saudação 0x3C0C2C. A dica de corrida 0x3C1796 indica X, conforme o teclado padrão do port.
- Atualizados o README, as etapas, o catálogo privado e o verificador de diálogos. O relatório 30 reúne as galerias e as verificações do lote.
- Passaram 52 testes Python e as 118 comparações de diálogos. Áudio e memória coincidiram com o original, com diferenças de imagem restritas à faixa do texto. Menus, entrada da fase e o ciclo Candy/reinício passaram na regressão.

## 2026-11-07 — Quarenta e uma saudações do Cranky

- Integradas 35 saudações adicionais, somando 41 saudações e 100 diálogos no piloto. A comparação individual das 41 saudações e o ciclo de salvar e reabrir passaram. [Relatório 29](docs/29-SAUDACOES-COMPLETAS-CRANKY-PT-BR.md).

## 2026-11-07 — Treze falas completas do Funky Kong em PT-BR

- Integradas as nove mensagens inglesas de revisita do Funky Kong (`0x3C0374–0x3C038C`, de `0x3C3334` a `0x3C3575`), concluindo todas as treze falas identificadas do personagem com preservação de Kongs, Jungle Hijinxs, Cranky, Candy, DK, Donkey e Diddy.
- Acrescentadas nove regiões de dados; as 65 regiões anteriores e a fonte compartilhada mantêm os mesmos bytes (`b8d02225…`). O piloto passa a aplicar 74 regiões em memória (65 diálogos no total).
- Cinquenta e dois testes passaram. As nove falas mantiveram áudio e WRAM inteira iguais ao original, com mudanças visuais só na faixa do diálogo e capturas legíveis, sem cortes. Regressão das falas de abertura do Funky, menus/entrada da fase e ciclo Candy/reinício aprovados em QA isolado.
- Criados galeria privada, catálogo `draft-13` (65 rascunhos) e relatório 28. Revisão humana e campanha continuam pendentes.
- ROM, executável habitual e saves pessoais preservados; nenhuma nova instalação.

## 2026-11-07 — Onze falas de retorno rápido do Cranky em PT-BR

- Integradas as onze mensagens únicas da tabela inglesa de retorno rápido do Cranky (`0x3C0144–0x3C0164`, de `0x3C2E3B` a `0x3C301E`), mantendo ponteiros, comprimentos exatos em bytes, números de linhas, terminadores, paridades e o tom sarcástico original.
- Acrescentadas onze regiões de dados; as 54 regiões anteriores e a fonte compartilhada mantêm os mesmos bytes (`f0a3f4f7…`). O piloto passa a aplicar 65 regiões em memória (56 diálogos no total).
- Cinquenta e um testes passaram. As onze falas mantiveram áudio e WRAM inteira iguais ao original, com mudanças visuais só na faixa do diálogo e capturas legíveis, sem cortes. Regressão das saudações anteriores do Cranky, menus/entrada da fase e ciclo Candy/reinício aprovados em QA isolado.
- Criados galeria privada, catálogo `draft-12` (56 rascunhos) e relatório 27. Revisão humana e campanha continuam pendentes.
- ROM, executável habitual e saves pessoais preservados; nenhuma nova instalação.

## 2026-11-07 — Cinco dicas de Chimp Caverns em PT-BR

- Integradas as cinco dicas do grupo de Chimp Caverns na tabela inglesa da Rev 1 (`0x3C01C4–0x3C01D4`): Manic Mincers, Misty Mine, Loopy Lights, Platform Perils e Tanked Up Trouble, concluindo todas as 27 dicas de fases dos seis mundos com nomes completos, Diddy, TNT e pistas preservados.
- Acrescentadas cinco regiões de dados; as 49 regiões anteriores e a fonte compartilhada mantêm os mesmos bytes (`53285419…`). O piloto passa a aplicar 54 regiões em memória.
- Quarenta e nove testes passaram. As cinco dicas mantiveram áudio e WRAM inteira iguais ao original, com mudanças visuais só na faixa do diálogo e capturas legíveis, sem cortes. Regressão das dicas anteriores de Kongo Jungle, Monkey Mines, Vine Valley, Gorilla Glacier e Kremkroc Industries Inc., menus/entrada da fase e ciclo Candy/reinício aprovados em QA isolado.
- Criados galeria privada, catálogo `draft-11` (45 rascunhos) e relatório 26. Revisão humana e coleta dos segredos continuam pendentes.
- ROM, executável habitual e saves pessoais preservados; nenhuma nova instalação.

## 2026-11-07 — Cinco dicas de Kremkroc Industries Inc. em PT-BR

- Integradas as cinco dicas do grupo de Kremkroc Industries Inc. na tabela inglesa da Rev 1 (`0x3C01B4–0x3C01C4`): Elevator Antics, Trick Track Trek, Mine Cart Madness, Poison Pond e Blackout Basement, com nomes completos, Gnawty e pistas preservados.
- Acrescentadas cinco regiões de dados; as 44 regiões anteriores e a fonte compartilhada mantêm os mesmos bytes (`7db42041…`). O piloto passa a aplicar 49 regiões em memória.
- Quarenta e oito testes passaram. As cinco dicas mantiveram áudio e WRAM inteira iguais ao original, com mudanças visuais só na faixa do diálogo e capturas legíveis, sem cortes. Regressão das dicas anteriores de Kongo Jungle, Monkey Mines, Vine Valley e Gorilla Glacier, menus/entrada da fase e ciclo Candy/reinício aprovados em QA isolado.
- Criados galeria privada, catálogo `draft-10` (40 rascunhos) e relatório 25. Revisão humana e coleta dos segredos continuam pendentes.
- ROM, executável habitual e saves pessoais preservados; nenhuma nova instalação.

## 2026-11-07 — Cinco dicas de Gorilla Glacier em PT-BR

- Integradas as cinco dicas do grupo de Gorilla Glacier na tabela inglesa da Rev 1 (`0x3C01A4–0x3C01B4`): Snow Barrel Blast, Croctopus Chase, Ice Age Alley, Slipslide Ride e Torchlight Trouble, com nomes completos, Croctopus, TNT e pistas preservados.
- Acrescentadas cinco regiões de dados; as 39 regiões anteriores e a fonte compartilhada mantêm os mesmos bytes (`e80b1b28…`). O piloto passa a aplicar 44 regiões em memória.
- Quarenta e sete testes passaram. As cinco dicas mantiveram áudio e WRAM inteira iguais ao original, com mudanças visuais só na faixa do diálogo e capturas legíveis, sem cortes. Regressão das dicas anteriores de Kongo Jungle, Monkey Mines e Vine Valley, menus/entrada da fase e ciclo Candy/reinício aprovados em QA isolado.
- Criados galeria privada, catálogo `draft-09` (35 rascunhos) e relatório 24. Revisão humana e coleta dos segredos continuam pendentes.
- ROM, executável habitual e saves pessoais preservados; nenhuma nova instalação.

## 2026-11-07 — Três dicas de Vine Valley em PT-BR

- Identificado o grupo de Vine Valley na tabela inglesa da Rev 1 em `0x3C01D4–0x3C01E4` (sexto grupo de ponteiros, separado de Gorilla Glacier, Kremkroc Industries Inc. e Chimp Caverns). Integradas as três dicas de Orang-utan Gang, Tree Top Town e Temple Tempest com nomes completos e pistas preservados.
- Acrescentadas três regiões de dados; as 36 regiões anteriores e a fonte compartilhada mantêm os mesmos bytes (`a230a43e…`). O piloto passa a aplicar 39 regiões em memória.
- Quarenta e seis testes passaram. As três dicas mantiveram áudio e WRAM inteira iguais ao original (delta de passos interpretados zero em todas), com mudanças visuais só na faixa do diálogo e capturas legíveis, sem cortes. Regressão das dicas anteriores de Kongo Jungle e Monkey Mines, menus/entrada da fase e ciclo Candy/reinício aprovados em QA isolado.
- Criados galeria privada, catálogo `draft-08` (30 rascunhos) e relatório 23. Revisão humana e coleta dos segredos continuam pendentes.
- ROM, executável habitual e saves pessoais preservados; nenhuma nova instalação.

## 2026-11-06 — Quatro dicas de Monkey Mines em PT-BR

- Integradas dicas de Bouncy Bonanza, Stop & Go Station, Mine Cart Carnage e Millstone Mayhem. Nomes completos preservados; pneus, rinoceronte dourado, bananas e salto antecipado mantidos nas pistas.
- Acrescentadas quatro regiões de dados; as 32 anteriores e a fonte mantêm os mesmos bytes. Novos metadados e filtro de mundo separam as galerias de Kongo Jungle e Monkey Mines, sem alterar a seleção no aplicativo.
- Quarenta e cinco testes passaram. Quatro dicas com áudio e WRAM inteira iguais ao original, mudanças visuais só no texto e capturas legíveis, sem cortes. Regressão de Kongo Jungle, menus/entrada da fase e um ciclo Candy/reinício passou em QA isolado.
- Criados galeria privada, catálogo draft-07 e relatório 22, com registro das escolhas de contexto e dos limites de cobertura. Revisão humana e coleta dos segredos continuam pendentes.
- ROM, executável habitual e saves pessoais preservados; nenhuma nova instalação.

## 2026-11-06 — Cinco dicas de Kongo Jungle em PT-BR

- Integradas cinco dicas do Cranky para Jungle Hijinxs, Ropey Rampage, Barrel Cannon Canyon, Reptile Rumble e Coral Capers. Preservados Winky, Croctopus e as pistas físicas de cada texto.
- Conferidos os ponteiros Rev 1, tamanhos, linhas, paridades e associação de cada registro à fase. Acrescentadas cinco regiões; as 27 anteriores e a fonte permanecem byte a byte iguais.
- Quarenta e três testes passaram. Cinco dicas com áudio e WRAM inteira iguais ao original, diferenças visuais apenas no diálogo e capturas legíveis, sem cortes. Regressão de menus/entrada da fase e de duas saudações anteriores aprovada; um ciclo Candy/reinício coincidiu entre aplicativo, runner e disco com saves de QA isolados.
- Criados galeria privada, catálogo draft-06 e relatório 21. Registrado o aceite em relato da entrega anterior; as novas dicas aguardam revisão e coleta dos segredos em gameplay.
- ROM, executável habitual e saves pessoais preservados. Nenhuma nova instalação.

## 2026-11-06 — Correção do ê e primeiro lote do Cranky

- Corrigido o ê menor relatado pelo usuário na segunda fala do Funky. Preservadas todas as seis linhas do corpo original do e; acento colocado nas margens superiores, sem mudar o tamanho da célula.
- Integradas seis saudações do Cranky ao piloto, mantendo Donkey, Diddy, Donks e Funky Kong, tamanhos, linhas, terminadores, paridades e seleção original no aplicativo.
- Trinta e oito testes passaram. As seis saudações do Cranky mantiveram áudio e WRAM inteira iguais ao original, com diferenças visuais somente no diálogo. Funky/Candy, menus e entrada da fase passaram na regressão; um ciclo Candy/reinício coincidiu entre aplicativo, runner e disco em perfis de QA.
- Criadas prévias atualizadas do Funky e do primeiro lote do Cranky, catálogo privado draft-05 e relatório 20. Revisão humana pendente; demais textos do Cranky e campanha continuam abertos.
- ROM, executável habitual e saves pessoais preservados; sem novas instalações.

## 2026-11-06 — Quatro falas do Funky em PT-BR

- Integradas as quatro mensagens inglesas identificadas do Funky no piloto separado. Preservados Funky Kong, Jumbo Barrel, tom descontraído e a restrição de transporte a lugares já visitados.
- Mantidos ponteiros, tamanhos, linhas, terminadores e paridades. Reutilizada a fonte da Candy sem novos glifos; composição das regiões rejeita sobreposições.
- Trinta e dois testes passaram. Comparação individual das quatro falas: áudio e WRAM inteira iguais ao original, com diferenças visuais apenas no diálogo. Capturas legíveis e sem cortes.
- Regressão da Candy, menus e entrada da fase passou; um ciclo Candy/reinício coincidiu entre aplicativo, runner e disco, em perfis de QA isolados.
- Criados galeria privada, catálogo draft-04 e docs/19-FUNKY-PT-BR.md. ROM, executável habitual e saves pessoais preservados; revisão humana do Funky e campanha continuam pendentes.

## 2026-11-06 — Prévias da Candy aprovadas pelo usuário

- O usuário leu as oito prévias e aprovou todas. Registrado o aceite da redação e da leitura nas capturas em P19/P20 e no relatório da Candy.
- Próximo bloco: falas do Funky Kong, preservando nomes, Jumbo Barrel e instruções de transporte.
- Atualização documental, sem alterações no jogo ou novos testes. Leitura ao vivo, campanha e demais textos não foram validados por esse aceite.

## 2026-11-06 — Oito falas identificadas da Candy em PT-BR

- Traduzidas as seis mensagens de revisita, somando oito falas identificadas. Mantidos Candy Kong, Honey Kong, placa do local, tom e sentido das instruções.
- Preservados tamanhos, linhas, terminadores e ponteiros. Preenchimento lateral conserva a paridade das novas linhas; adicionado é em código ausente dos blocos ingleses identificados.
- Vinte e seis testes Python passaram. As oito falas foram comparadas individualmente no renderizador e inspecionadas em capturas; áudio igual, mudanças visuais só no texto e WRAM integralmente igual nas seis novas mensagens.
- Regressão de menus/entrada da fase e um par Candy/reinício passaram. O diagnóstico para escolher cada mensagem existe somente no runner sem janela; não altera o sorteio no aplicativo.
- Criados galeria privada de leitura e docs/18-CANDY-FALAS-COMPLETAS.md; Notion atualizado. ROM, executável habitual e saves pessoais preservados. Revisão humana, campanha e tradução integral continuam pendentes.

## 2026-11-06 — Primeiras falas da Candy em PT-BR

- Integradas apresentação e instrução de salvamento no build PT-BR separado, preservando Candy Kong, a placa do local, ponteiros e tamanhos de 46/72 bytes.
- Fonte de diálogo Rev 1 localizada e glifos á/ê/ó adicionados em três códigos ausentes dos blocos ingleses identificados. Outros idiomas e acentos ainda precisam de revisão.
- Capturas nativas conferidas: alterações visuais somente na faixa das falas. WRAM idêntica fora das palavras de alinhamento do texto; áudio idêntico. O caminho de centralização executa 19 instruções adicionais, sem mudar o relógio do jogo.
- Vinte testes Python passaram. Regressão de menus e entrada da fase aprovada; um par Candy/reinício passou entre aplicativo, runner e disco em perfis QA.
- Criado Testar falas da Candy.cmd para prévia direta sem saves. Abertura normal do piloto continua com seu perfil próprio; ROM, executável habitual e saves pessoais preservados.
- Adicionado docs/17-CANDY-PT-BR.md e atualizado o Notion. Duas falas do lote inicial estão no piloto e dez continuam em rascunho; aceite humano, campanha e tradução completa seguem pendentes.

## 2026-11-05 — Primeiro piloto PT-BR dos menus

- Localizados gráficos/tilemaps da seleção de jogo e jogadores e confirmado o ponteiro da fonte Rev 1. Fonte, dados e regiões são conferidos contra a ROM exata, sem assumir os offsets v1.0.
- Criado build separado e launcher Testar DKC - PT-BR.cmd, com cinco rótulos traduzidos e glifos Ã/Ç. Os desenhos dos Kongs e todas as regiões do inventário de nomes/falas ficaram preservados.
- As alterações são aplicadas em cinco regiões de dados da cópia em memória; ROM do disco, código do cartucho, AOT e executável habitual permanecem intactos. O piloto tem perfil de save próprio.
- Doze testes Python passaram. Nos quadros 1.700/2.300, estado e áudio coincidiram, com diferenças visuais apenas nas regiões previstas. No quadro 4.800, a imagem da fase também coincidiu.
- Um par Candy/reinício passou no build final entre aplicativo, runner e disco, em perfis de QA. Capturas finais inspecionadas; tipografia e leitura ao vivo aguardam o usuário.
- Adicionado docs/16-PILOTO-PT-BR.md e atualizado o Notion. Os 12 rascunhos de falas ainda não estão no jogo; demais textos, outros acentos, campanha e PT-BR completo continuam pendentes.

## 2026-11-05 — Preparação PT-BR com nomes preservados

- Usuário autorizou começar a tradução com cuidado para preservar nomes importantes e contexto; política registrada em D012 e localization/pt-BR/policy.json.
- Leitor próprio, sem escrita na ROM, identificou quatro regiões da Rev 1 e extraiu 346 registros privados: 50 rótulos de mapa, 47 de elenco, 32 de créditos e 217 falas. Inventário parcial; menus e textos gráficos ainda não localizados.
- Preparados 12 rascunhos privados de Cranky, Funky e Candy. Os rótulos do mapa permanecem originais; fonte, acentos, layout e sentido em tela ainda exigem revisão.
- Verificador de nomes/identidade passou no catálogo e seis testes sintéticos passaram. Hashes da ROM e do executável preservados; sem acesso aos saves nem instalação nova.
- Adicionado docs/15-PT-BR.md e atualizada a área exclusiva do Notion. Campanha continua pendente; o executável jogável não recebeu tradução nesta etapa.

## 2026-11-05 — Modos de tela aprovados e próxima etapa

- Usuário confirmou o funcionamento da versão e46f8f1 após a inclusão de preencher/4:3 e tela cheia adaptável. P17 aceita no teste relatado.
- Próxima etapa organizada: campanha e saves com progresso real, incluindo transições, mortes, bônus, chefes e carregamento após reabrir, antes de PT-BR.
- Roteiro acrescentado ao plano de validação e referência atualizada no README, pendências e Notion. Nenhuma nova execução funcional ou alteração no executável nesta atualização documental.
- O aceite não informa campanha completa nem comprova funcionamento em todos os monitores ou computadores.

## 2026-11-05 — Imagem adaptável e piscadas resolvidas

- Usuário confirmou que a tela parou de piscar após a correção anterior.
- Modo preencher como padrão: usa toda a área da janela sem cortar o framebuffer. Em formatos diferentes de 4:3, a imagem fica esticada. F6 alterna com a proporção original.
- F11 alterna tela cheia sem moldura, consultando o monitor atual e suas dimensões. Ao sair, restaura a janela; mudanças de monitor/resolução reajustam a apresentação. Nenhuma mudança na resolução do sistema ou velocidade do jogo.
- Testes gráficos em oito tamanhos passaram, incluindo widescreen, ultrawide, retrato e 1×1; mantidos isolamento fora da tela, preto real e verificação de recursos GDI.
- Teste nativo com janelas ocultas passou por 20 ciclos de tela cheia/reajuste/restauração em cada monitor conectado. Boot de 600 quadros no aplicativo preservou os hashes de imagem e WRAM da referência.
- Guias, pendências e Notion atualizados. Teste visual dos novos modos e cobertura em outros computadores permanecem pendentes. Nenhuma instalação nova ou acesso aos saves pessoais nesta rodada.

## 2026-11-05 — Correção da apresentação da janela

- Usuário confirmou os saves e relatou piscadas pretas rápidas na abertura e em todas as fases.
- Removida a limpeza preta direta na janela. Fundo e imagem agora são compostos em memória e apresentados juntos; preservados 4:3, transições reais e alvo de 60,0988 Hz.
- Testes GDI passaram: destino isolado durante composição, equivalência RGB em seis tamanhos, carregamento, preto real e 500 redimensionamentos sem vazamento de objetos.
- Sete testes de IO e três pares Candy/reinício passaram novamente. Framebuffer e WRAM da janela coincidiram com o runner na sequência de 5.400 quadros. Saves pessoais e backup permaneceram idênticos.
- Smoke de agendamento de 600 quadros com janela oculta: média 16,638 ms, p95 17,945 ms e zero overruns após aquecimento. Não constitui medição visual do monitor.
- Adicionado docs/14-APRESENTACAO.md e atualizada a cópia no Notion. Aguardando teste humano para confirmar o desaparecimento das piscadas; sem nova instalação.

## 2026-11-05 — Saves da Candy persistentes

- Integrado o módulo MIT desktop_sram da base fixada, com adaptador Rev 1, tamanho de SRAM conferido, backup no início da sessão e um único processo gravador por perfil.
- Dados pessoais em data/usa-rev1/saves/ no E:, fora de build/. Falhas detectadas preservam o arquivo anterior e pausam a janela para retry; o fechamento normal tenta concluir a escrita.
- Jogar DKC.cmd e o launcher antigo agora iniciam pelo menu normal, permitindo escolher o arquivo salvo. Atalhos de entrada direta permanecem separados dos saves pessoais.
- Três repetições de salvar na Candy e carregar em processos novos passaram, comparando aplicativo, runner e disco. Nenhum snapshot foi usado; o cenário de QA usa o primeiro arquivo a 00:00 / 00% e entrada controlada na Candy.
- Sete testes de arquivos passaram, incluindo falha de escrita/backup, tamanhos incorretos, exclusão de outro gravador e diretório Unicode.
- Replay de boot preservado; smoke de agendamento com SRAM ativa manteve 60,0988 Hz. Nenhuma ferramenta nova instalada e nenhum dado de QA copiado para o perfil pessoal.
- Adicionado docs/13-SAVES.md com instruções e limites. Save states, campanha completa e PT-BR permanecem nas etapas posteriores.

## 2026-11-04 — Fluidez confirmada pelo usuário

- Após disponibilizar a correção de cadência, o usuário confirmou que o jogo agora está funcionando perfeitamente em seu teste.
- Registrado o aceite do ajuste de fluidez e mantida a versão 6b2b5b9 como base de trabalho, sem novas alterações no executável.
- Campanha completa, persistência e demais critérios de validação permanecem nas etapas próprias; esse retorno não informa uma cobertura de campanha.

## 2026-11-04 — Correção de cadência e varredura das entradas

- Usuário relatou boa fluidez nas primeiras fases e engasgos após a chuva, na primeira caverna; pediu conferir as seguintes sem acelerar o jogo.
- Reproduzida cadência irregular na janela. Implementados waitable timer de alta resolução, retomada sem rajada de compensação e evento de conclusão da fila de áudio.
- Mantidos alvo de 60,0988 Hz, clocks do cartucho, áudio, física e 39 variantes AOT.
- Em dois testes de 900 quadros na caverna, p95 de intervalo caiu de 30,796 para 17,417 ms; conclusões após o prazo passaram de 175 para zero, com a mesma cadência média.
- Executadas e inspecionadas 40 entradas principais e de chefes; 12.000 amostras de cálculo abaixo de 16,639 ms. Nove cenas receberam recaptura antecipada para não confundir retorno ao mapa com a sala testada.
- Três regressões de boot idênticas; framebuffer e WRAM da janela coincidiram com o runner. Caverna com 1.803 registros de diagnóstico acumulados preservou o relatório completo.
- Adicionados scripts/profile_rev1_levels.py, docs/12-FLUIDEZ.md e CSV de medidas. A varredura cobre trechos iniciais, sem declarar campanha ou fases inteiras validadas.

## 2026-11-04 — Versão com janela para o primeiro teste

- A pedido do usuário, criado host Windows com apresentação GDI em 4:3, teclado e saída de áudio WinMM, sem instalar dependências.
- Compartilhada a rotina de execução/áudio com o runner automatizado. Regressões de 600 e 4.800 quadros repetiram todos os campos dos relatórios da base anterior.
- Acrescentada abertura por Jogar DKC - Teste.cmd e opção --jungle, que reproduz os botões até a fase e entrega o controle ao jogador.
- Processo iniciado e janela de controle exposta após a preparação. Captura automática falhou com FrameArrived timed out e window capture timed out; avaliação visual, sonora e de gameplay ao vivo permanece com o usuário.
- Criado docs/11-TESTE-INTERATIVO.md com controles e limites. Sem saves, controle físico ou tela cheia; candidata de 55 variantes permanece desativada.

## 2026-11-04 — Primeiro protótipo com a USA Rev 1 disponível

- Pedido do usuário de começar com a ROM existente registrado em D011, substituindo D002. A entrada ativa é USA v1.1 (Rev 1), com tamanho e SHA-256 exatos; não houve conversão para v1.0.
- Criados perfil de ROM, configuração própria de vetores, geração privada, host sem janela, alvo CMake, script de build e receita de botões até Jungle Hijinxs.
- Reutilizados gerador/runtime fixados e adaptadores genéricos do DKC1Recomp, sem alterar seu perfil v1.0. Aviso MIT do host preservado; nenhuma ferramenta nova instalada.
- Geração padrão: 39 variantes AOT, 29 entradas distintas de dispatch e interpretação de apoio. Compilação Windows x64 concluída com MSVC, CMake e Ninja no E:.
- Três replays independentes de 600 quadros produziram os mesmos hashes de framebuffer, WRAM, VRAM e cadeia de áudio. Imagens do boot e da abertura foram inspecionadas; entrada automatizada na primeira fase aos 4.800 quadros repetida em novo processo.
- A entrada Rev 1 passou no verificador; a v1.2 foi rejeitada pelo verificador e pelo host antes de executar.
- Candidata com 55 variantes divergiu da base em WRAM e áudio. Foi retirada da configuração padrão; investigação permanece aberta, sem causa atribuída.
- Acrescentado docs/10-USA-REV1-BRINGUP.md com comandos, identidades, hashes e limites. Documentação e área exclusiva no Notion atualizadas para o novo escopo.
- Ainda sem sessão interativa, reprodução audível validada, persistência ou cobertura de campanha. Tradução PT-BR e experiência de aplicativo continuam após estabilização.

## 2026-11-04 — Revisão final do Notion e início técnico

### Revisado e iniciado

- Lidas as 11 páginas do projeto no Notion, sem truncamento; atualizados o estado atual e o roteiro para iniciar a preparação técnica.
- Acrescentadas pendências explícitas de campanha completa, tradução PT-BR e aplicativo Windows, mantendo suas dependências.
- Confirmado pelo usuário que a ROM USA v1.0 ainda não está disponível; geração e gameplay continuam aguardando essa entrada.
- Fixada a base limpa na tag v0.0.17 e inicializadas as revisões correspondentes dos submódulos.
- Criados config/upstream.lock.json e scripts/check_project.py para repetir a verificação dos commits, da ROM e das ferramentas sem alterar os arquivos de jogo.
- Registrada a orientação de instalar novas ferramentas no E:. A instância de BuildTools iniciada no C: foi removida pelo desinstalador oficial com saída 0; a reinstalação foi direcionada ao E:.

### Validação realizada

- O verificador confirmou os três commits e identificou a ROM v1.2 como não suportada, retornando código 1 pelos pré-requisitos pendentes.
- Sintaxe do script e estrutura JSON do lock conferidas; nenhuma geração do jogo foi iniciada.
- Instalação no E: concluída com saída 0 e sem reinicialização exigida; a antiga pasta principal do BuildTools no C: foi removida.
- MSVC, CMake 3.31.6-msvc6 e Ninja 1.12.1 conferidos no E:. Programa mínimo com o SDK compilado e executado com sucesso.
- SDK 10.0.26100.0 e instalador compartilhado da Microsoft permaneceram no C: e não foram apagados manualmente.
- Suíte pública: 303 testes, 2 erros e 10 skips. Os erros dependem de cc e flags GCC/Clang/sanitizers; a suíte não foi declarada aprovada.
- O pré-flight final confirmou commits e ferramentas, retornando saída 1 somente pela ausência da ROM USA v1.0. Logs completos em evidence/2026-11-04/environment/.

## 2026-11-04 — Meta final de PT-BR e aplicativo Windows

- Registrada a orientação do usuário: estabilizar e validar o port antes de traduzi-lo para PT-BR.
- Definida a experiência desejada de abrir o executável e jogar, sem comandos ou seleção repetida de ROM no uso habitual.
- Acrescentados marcos de tradução e empacotamento e critérios de campanha, localização, regressão e abertura direta.
- Preparação única dos dados, instalador ou pacote portátil permanecem propostas técnicas; o formato final não foi escolhido.
- Atualização documental, sem alterações no código do jogo, traduções aplicadas ou novos testes funcionais.

## 2026-11-04 — Criação do repositório público

### Realizado

- Criado o repositório público [rya3n/donkey-kong-country-pc](https://github.com/rya3n/donkey-kong-country-pc), conforme pedido expresso do usuário.
- Publicado o conjunto inicial com README, log, nove documentos técnicos e .gitignore.
- Adicionadas exclusões para ROMs, saves, arquivos gerados, builds, downloads, runtime e clone independente do upstream.
- Movidos os links do Notion privado do README para .project-local.md, mantido somente no computador.
- Mantidos os créditos e a identificação do DKC1Recomp como base de referência.

### Verificado

- Primeiro commit enviado para main: 2b6e933c149225e40ecb614b104749ce581af150.
- A API do GitHub confirmou visibilidade pública e retornou a árvore completa com os 12 arquivos selecionados, sem arquivos adicionais.
- A conferência prévia não encontrou padrões de credenciais, links privados do Notion ou caminhos pessoais nos arquivos selecionados; git diff --cached --check passou.

### Estado técnico

Esta publicação organiza o projeto e não representa uma versão jogável produzida por nós. A ROM USA v1.0, a escolha da revisão de código e o ambiente C/CMake continuam pendentes.

## 2026-11-04 — Avaliação de ferramentas para eficiência

### Analisado

- Revisões identificadas dos seis repositórios sugeridos, com leitura de documentação e arquivos selecionados de requisitos e implementação.
- Adequação ao port nativo, sobreposição entre coleções de skills e custo de instalação, indexação e manutenção.
- Node 24.18.0, npm 11.16.0 e uv encontrados na sessão; a presença das ferramentas não comprova compatibilidade dos plugins.

### Registrado

- Recomendação de consulta seletiva a agent-skills e ECC, com pilotos separados para context-mode e Graphify.
- Uso de Cloudflare em auditorias delimitadas e de Playwright em alvos web, conforme necessidade.
- Plano de comparação com perguntas fixas, qualidade das respostas e custo total, sem assumir os percentuais divulgados pelos autores.

### Limites

- Nenhuma nova ferramenta ou skill instalada; nenhum hook ou configuração global alterado.
- Nenhum benchmark desses projetos foi executado localmente. As recomendações permanecem propostas.
- O relatório foi acrescentado a Ferramentas e referências e sua cópia no Notion foi atualizada.

## 2026-11-04 — Documentação inicial

### Adicionado

- Índice principal e nove documentos sobre visão, diagnóstico, arquitetura, ambiente, validação, etapas, decisões, créditos e ferramentas.
- Este log de atualizações, solicitado pelo usuário.
- Registro dos seis repositórios sugeridos pelo usuário, com finalidade possível e estado de adoção.
- Área privada exclusiva do projeto no Notion, com nove documentos e o log como subpáginas; conteúdo e vínculo com a página principal conferidos por leitura.

### Decidido

- Priorizar documentação antes de retomar implementação e publicação.
- Adotar USA v1.0 como primeira ROM de trabalho, conforme escolha expressa do usuário.
- Manter a documentação do Donkey Kong Country separada de outros projetos.

### Verificado

- A ROM local possui 4.194.304 bytes, revisão interna 2 e checksum calculado `0x2BCC`, igual ao armazenado.
- O SHA-256 do ZIP oficial Windows v0.0.17 corresponde ao digest divulgado na API do GitHub.
- Os 20 arquivos listados no `BUILDINFO.json` do pacote extraído conferem em tamanho e SHA-256. Isso comprova integridade em relação ao manifesto, não funcionamento do jogo.
- O clone local e o executável distribuído apontam para commits diferentes; a divergência foi documentada.
- Os 11 arquivos Markdown locais foram conferidos quanto a links internos, fechamento de blocos de código e caracteres de substituição: dez links locais encontrados, sem erros nesses critérios.
- A página principal e as dez subpáginas do Notion foram recuperadas pela conexão e pertencem à área exclusiva do projeto. A aparência visual no aplicativo não foi inspecionada.

### Pendente

- Disponibilizar localmente a ROM USA v1.0 compatível.
- Confirmar e preparar o ambiente de compilação C/CMake.
- Selecionar uma revisão de código e engine para uma compilação reproduzível.
- Gerar código, compilar e executar a validação funcional.
- Criar o repositório público, após a etapa de documentação.

## 2026-11-04 — Preparação inicial do projeto

### Realizado

- Inspeção da pasta: encontrada uma ROM com nome indicando USA v1.2.
- Pesquisa de bases públicas e escolha do DKC1Recomp como caminho inicial de integração.
- Download do clone e inicialização dos submódulos `snesrecomp` e `recomp-net`.
- Download e extração do pacote oficial Windows x64 v0.0.17.
- Execução da suíte pública Python do clone: `Ran 251 tests`; resultado `FAILED (errors=10, skipped=14)`. Os erros exibidos apontaram executáveis de compilação ausentes. A saída completa não foi arquivada; o diagnóstico preserva esse limite.
- Tentativa de acesso ao GitHub pelo navegador encerrada pela ferramenta, que não conseguiu determinar a URL atual com segurança. Nenhum repositório foi criado.

### Não realizado nesta etapa

A ROM v1.0 não estava disponível. Não houve geração de código do jogo, compilação própria ou execução de gameplay.

## Como registrar as próximas atualizações

Cada entrada deve informar mudança, verificação e pendência de forma separada. Use a data real da execução; inclua commit, versão, comando e caminho da evidência quando forem relevantes. Para um resultado que não foi executado, use “planejado” ou “pendente”. Corrija um registro equivocado com uma entrada de correção identificável.

Modelo para copiar:

```text
AAAA-MM-DD — título da atualização
Mudança: o que foi alterado e por quê.
Identidade: commit do projeto, commit da engine e hash do executável, se aplicável.
Verificação: comando, resultado e evidência salva.
Limite: cenas, plataformas ou condições ainda não verificadas.
Próximo passo: ação concreta e seu pré-requisito.
```
