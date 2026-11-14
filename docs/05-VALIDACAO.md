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
| V03 | Testes do build e suíte pública | Resultados completos, sem falhas inexplicadas; skips justificados | Suíte Python local: 59 testes passaram. Suíte pública anterior: 303 testes, 2 erros e 10 skips. CTest do jogo pendente |
| V04 | Boot, apresentação e menu | Imagem estável e progressão até seleção de jogo | Executado em janela; usuário confirmou a fluidez após a correção |
| V05 | Entrar em Jungle Hijinxs | Roteiro do boot até controle do personagem | Entrada reproduzida e sessão humana realizada; cobertura ampliada em V14 |
| V06 | Movimento e interação | Mover, pular, rolar, resgatar Diddy, trocar e usar barril | Parcial. Corrida, salto, barris de checkpoint e de parceiro em Jungle Hijinxs, escalada em Ropey Rampage |
| V07 | Morte e retorno | Ciclo completo sem travamento e com estado coerente | Confirmado em Jungle Hijinxs. Perda de vida, retorno ao mapa e nova entrada |
| V08 | Concluir fase e voltar ao mapa | Saída, transição e progressão corretas | Repetido na rota principal de Kongo Jungle, em Monkey Mines, Vulture Culture e Tree Top Town. Forest Frenzy liberada no mapa de Vine Valley |
| V09 | Áudio e apresentação | Trecho identificado sem cortes persistentes ou defeitos visíveis | PCM comparado da despedida do Cranky até a caverna. Escuta em janela pendente |
| V10 | Salvamento do jogo | Salvar com Candy, encerrar normalmente e recuperar em novo processo | Candy de Kongo Jungle aprovada com progresso real em headless e Win32. Ampliar aos demais pontos da campanha |
| V11 | Save state, se incluído no marco | Comparar continuação após load com execução contínua | Não implementado; não faz parte da entrega de SRAM |
| V12 | Controle físico | Ações e reconexão no dispositivo disponível | Não executado |
| V13 | Repetição determinística | Três replays com mesma entrada e hashes dos estados comparados iguais | Três execuções de 600 quadros idênticas; entrada na fase repetida; cobertura restrita |

Salvar com Candy e usar save state são funcionalidades diferentes e exigem testes distintos. Um quicksave bem-sucedido não comprova persistência do progresso do cartucho.

## Quando ampliar a cobertura

Depois da primeira entrega, incluir caverna, chuva e cordas, fase vertical, água, bônus, canhões, chefe e transições. Uma alteração em rotina compartilhada exige cobrir os cenários que ela alcança. Registrar os trechos exatos; não declarar compatibilidade com o jogo inteiro com base em uma fase.

Para widescreen, observar separadamente imagem central, margens, streaming, ativação de objetos e regras de gameplay. As exigências completas de promoção do upstream incluem determinismo, entradas limpas, comparação central e matriz de layouts; seguir o `upstream/AGENTS.md` antes de alterar esse código.

## Campanha e progresso real

Roteiro preparado em 2026-11-05 após o aceite dos modos de tela. A [primeira sessão do piloto PT-BR](31-INICIO-CAMPANHA-PT-BR.md) registra a execução de 2026-11-10. Usar o menu normal e identificar o build em cada sessão.

| Passo | O que registrar | Estado |
| --- | --- | --- |
| Ações e retorno | Movimento, troca de personagem, barris, morte, retorno e continuação | Parcial em Jungle Hijinxs e Ropey Rampage |
| Progressão | Nome de cada fase concluída, saída, mapa, bônus e entrada seguinte | Rota principal de Kongo Jungle e Monkey Mines concluída, com Vulture Culture e Tree Top Town validadas em Vine Valley. Retomar diante de Forest Frenzy pelo [roteiro contínuo](32-CAMPANHA-PT-BR-AUDIO-E-PROGRESSO.md#saída-de-tree-top-town) |
| Variedade e chefes | Água, chuva, cavernas, cordas, canhões, chefes e transições entre mundos | Chuva, cordas, caverna, água, canhões e carrinho exercitados. Very Gnawty e Master Necky derrotados com transição para o próximo mundo |
| Saves com progresso real | Selecionar o slot, salvar na Candy, fechar normalmente, reabrir e conferir o mesmo arquivo | Confirmado na Candy de Kongo Jungle com [roteiro e evidências](32-CAMPANHA-PT-BR-AUDIO-E-PROGRESSO.md) |
| Final da campanha | Chefe final, encerramento/créditos e estado recuperado após reabrir | A registrar |

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
