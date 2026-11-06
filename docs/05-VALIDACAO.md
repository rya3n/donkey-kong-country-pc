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
| V03 | Testes do build e suíte pública | Resultados completos, sem falhas inexplicadas; skips justificados | Suíte pública: 303 testes, 2 erros, 10 skips; CTest do jogo aguarda ROM/build |
| V04 | Boot, apresentação e menu | Imagem estável e progressão até seleção de jogo | Executado em janela; usuário confirmou a fluidez após a correção |
| V05 | Entrar em Jungle Hijinxs | Roteiro do boot até controle do personagem | Entrada reproduzida e sessão humana realizada; cobertura ampliada em V14 |
| V06 | Movimento e interação | Mover, pular, rolar, resgatar Diddy, trocar e usar barril | Não executado |
| V07 | Morte e retorno | Ciclo completo sem travamento e com estado coerente | Não executado |
| V08 | Concluir fase e voltar ao mapa | Saída, transição e progressão corretas | Não executado |
| V09 | Áudio e apresentação | Trecho identificado sem cortes persistentes ou defeitos visíveis | Não executado |
| V10 | Salvamento do jogo | Salvar com Candy, encerrar normalmente e recuperar em novo processo | Três repetições passaram no cenário Candy 00:00 / 00%; ampliar cobertura de progresso real |
| V11 | Save state, se incluído no marco | Comparar continuação após load com execução contínua | Não implementado; não faz parte da entrega de SRAM |
| V12 | Controle físico | Ações e reconexão no dispositivo disponível | Não executado |
| V13 | Repetição determinística | Três replays com mesma entrada e hashes dos estados comparados iguais | Três execuções de 600 quadros idênticas; entrada na fase repetida; cobertura restrita |

Salvar com Candy e usar save state são funcionalidades diferentes e exigem testes distintos. Um quicksave bem-sucedido não comprova persistência do progresso do cartucho.

## Quando ampliar a cobertura

Depois da primeira entrega, incluir caverna, chuva e cordas, fase vertical, água, bônus, canhões, chefe e transições. Uma alteração em rotina compartilhada exige cobrir os cenários que ela alcança. Registrar os trechos exatos; não declarar compatibilidade com o jogo inteiro com base em uma fase.

Para widescreen, observar separadamente imagem central, margens, streaming, ativação de objetos e regras de gameplay. As exigências completas de promoção do upstream incluem determinismo, entradas limpas, comparação central e matriz de layouts; seguir o `upstream/AGENTS.md` antes de alterar esse código.

## Próxima execução: campanha e progresso real

Roteiro preparado em 2026-11-05 após o aceite dos modos de tela. Esta lista organiza o próximo teste; não registra resultados já obtidos. Usar a versão e46f8f1 como referência inicial e identificar qualquer correção posterior. Jogar pelo menu normal, sem os atalhos de entrada diagnóstica.

| Passo | O que registrar | Estado |
| --- | --- | --- |
| Ações e retorno | Movimento, troca de personagem, barris, morte, retorno e continuação | A registrar |
| Progressão | Nome de cada fase concluída, saída, mapa, bônus e entrada seguinte | A registrar |
| Variedade e chefes | Água, chuva, cavernas, cordas, canhões, chefes e transições entre mundos | A registrar |
| Saves com progresso real | Progresso mostrado no menu, salvar na Candy, fechar normalmente, reabrir e conferir o mesmo arquivo | A registrar |
| Final da campanha | Chefe final, encerramento/créditos e estado recuperado após reabrir | A registrar |

Para cada sessão, anotar versão, fases percorridas, modo de tela e defeitos observados. Testar a persistência em momentos diferentes da progressão; identificar e proteger a cópia do save antes de qualquer teste de migração ou falha. Não substituir o progresso pessoal por fixtures de QA. Percurso principal, bônus e eventuais caminhos não percorridos devem ter sua cobertura indicada separadamente.

Corrigir e repetir qualquer cenário com defeito crítico antes de aceitar V14. Por autorização posterior, o inventário e os rascunhos PT-BR já começaram em paralelo; ver [Preparação PT-BR](15-PT-BR.md). Isso não aceita V14 nem promove a tradução ao executável. Suporte a controle físico, save states e pacote final continuam em seus próprios marcos.

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
