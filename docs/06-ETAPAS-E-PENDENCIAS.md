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

O usuário priorizou M0 e, após a preparação dos documentos, solicitou expressamente a criação do GitHub público. O repositório foi criado para a publicação inicial da documentação; os marcos de compilação e validação permanecem pendentes.

## Pendências acionáveis

| ID | Ação | Estado | Dependência e resultado esperado |
| --- | --- | --- | --- |
| P01 | Revisar a documentação inicial | Concluída para início técnico | Onze páginas do Notion revisadas; estado atual, bloqueio e roteiro atualizados |
| P02 | Disponibilizar ROM USA v1.0 | Bloqueada: arquivo indisponível | Usuário confirmou a ausência; validar tamanho e hash quando o arquivo estiver disponível |
| P03 | Selecionar revisão de código/engine | Concluída | v0.0.17 e os três commits conferidos contra config/upstream.lock.json |
| P04 | Confirmar ambiente C/CMake | Concluída a verificação básica | MSVC/CMake/Ninja no E:, SDK funcional e programa mínimo compilado e executado |
| P05 | Repetir suíte com logs completos | Executada; portabilidade pendente | 303 testes, 2 erros por cc/flags de sanitizers e 10 skips; log integral preservado |
| P06 | Gerar fontes e compilar | Depende de P02–P04 | Binário próprio identificado |
| P07 | Validar a primeira sessão | Depende de P06 | Resultados V04–V09 do plano de validação |
| P08 | Validar persistência | Depende de P07 | Save de jogo e save state avaliados separadamente |
| P09 | Criar repositório público | Concluída a publicação inicial da documentação | Destino: rya3n/donkey-kong-country-pc; visibilidade pública e 12 arquivos conferidos pela API |
| P10 | Validar campanha e estabilidade | Após o build e os testes iniciais | Cobertura V14 aceita antes de iniciar a tradução |
| P11 | Inventariar, traduzir e revisar PT-BR | Depende de P10 | Cobertura de textos, fonte, acentos e regressão V15–V17 |
| P12 | Preparar aplicativo Windows | Após a base estável; validar após a tradução | Abertura direta e pacote verificados por V18–V19 |

Não há responsáveis individuais ou prazos atribuídos além do contexto da conversa. Cada execução deve acrescentar resultados ao diagnóstico e ao log.

A meta posterior acordada é PT-BR e abertura direta. A publicação inicial de documentação não conclui os marcos de estabilidade do jogo. Antes de M6, executar a campanha e aceitar a cobertura ampliada; depois revisar a tradução e testar o pacote final. A técnica de tradução e o formato de distribuição ainda serão definidos.

## Riscos técnicos atuais

- A ROM disponível não corresponde à revisão exigida: geração e execução suportadas seguem bloqueadas até a entrada correta.
- Código e release divergem: reproduzir o executável baixado exige resolver a identidade da base antes da comparação.
- Falta de compilador no PATH impede alguns testes: o resumo atual não é uma suíte aprovada.
- O upstream mantém recursos experimentais: ativá-los cedo dificulta separar defeitos da base de mudanças do projeto.
- Evidências iniciais sem log integral têm menor rastreabilidade: novas execuções precisam arquivar comandos e saídas.
