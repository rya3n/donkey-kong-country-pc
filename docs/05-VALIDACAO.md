# Plano de validação

Estado: plano proposto. Nenhum cenário funcional abaixo foi executado pelo nosso projeto.

## Identidade mínima de uma execução

Registrar sistema operacional e hardware observado; SHA-256 da ROM; commits do projeto e da engine; comando e configuração de build; SHA-256 do executável; proporção de exibição e dimensões do framebuffer; opções gráficas; entrada usada; estado inicial; frames e duração; resultado e caminho dos artefatos.

Um estado inicial pode ser boot limpo ou um snapshot identificado por hash. Não reutilizar um save como evidência sem identificar a versão que o criou. Proteger uma cópia antes de testar persistência ou migração.

## Matriz inicial

| ID | Cenário | Aceitação proposta | Situação |
| --- | --- | --- | --- |
| V01 | Verificar ROM suportada | Tamanho e SHA-256 exatos | Pendente: ROM ausente |
| V02 | Gerar e compilar | Comandos terminam com sucesso e executável é identificado | Pendente: ambiente e base |
| V03 | Testes do build e suíte pública | Resultados completos, sem falhas inexplicadas; skips justificados | Suíte pública: 303 testes, 2 erros, 10 skips; CTest do jogo aguarda ROM/build |
| V04 | Boot, apresentação e menu | Imagem estável e progressão até seleção de jogo | Não executado |
| V05 | Entrar em Jungle Hijinxs | Roteiro do boot até controle do personagem | Não executado |
| V06 | Movimento e interação | Mover, pular, rolar, resgatar Diddy, trocar e usar barril | Não executado |
| V07 | Morte e retorno | Ciclo completo sem travamento e com estado coerente | Não executado |
| V08 | Concluir fase e voltar ao mapa | Saída, transição e progressão corretas | Não executado |
| V09 | Áudio e apresentação | Trecho identificado sem cortes persistentes ou defeitos visíveis | Não executado |
| V10 | Salvamento do jogo | Salvar com Candy, encerrar normalmente e recuperar em novo processo | Não executado |
| V11 | Save state, se incluído no marco | Comparar continuação após load com execução contínua | Não executado |
| V12 | Controle físico | Ações e reconexão no dispositivo disponível | Não executado |
| V13 | Repetição determinística | Três replays com mesma entrada e hashes dos estados comparados iguais | Não executado |

Salvar com Candy e usar save state são funcionalidades diferentes e exigem testes distintos. Um quicksave bem-sucedido não comprova persistência do progresso do cartucho.

## Quando ampliar a cobertura

Depois da primeira entrega, incluir caverna, chuva e cordas, fase vertical, água, bônus, canhões, chefe e transições. Uma alteração em rotina compartilhada exige cobrir os cenários que ela alcança. Registrar os trechos exatos; não declarar compatibilidade com o jogo inteiro com base em uma fase.

Para widescreen, observar separadamente imagem central, margens, streaming, ativação de objetos e regras de gameplay. As exigências completas de promoção do upstream incluem determinismo, entradas limpas, comparação central e matriz de layouts; seguir o `upstream/AGENTS.md` antes de alterar esse código.

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
