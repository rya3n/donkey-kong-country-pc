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

O usuário priorizou M0 e, após a preparação dos documentos, solicitou expressamente a criação do GitHub público. O repositório foi criado para a publicação inicial da documentação; os marcos de compilação e validação permanecem pendentes.

## Pendências acionáveis

| ID | Ação | Estado | Dependência e resultado esperado |
| --- | --- | --- | --- |
| P01 | Revisar a documentação inicial | Em revisão | Concordar com escopo e roteiro, mantendo dúvidas registradas |
| P02 | Disponibilizar ROM USA v1.0 | Bloqueia build | Arquivo local com tamanho e hash suportados |
| P03 | Selecionar revisão de código/engine | Aberta | Escolher clone atual ou revisão do pacote; registrar o par |
| P04 | Confirmar ambiente C/CMake | Aberta | Localizar ambiente existente ou preparar as ferramentas necessárias |
| P05 | Repetir suíte com logs completos | Depende de P04 | Resultados arquivados e erros classificados |
| P06 | Gerar fontes e compilar | Depende de P02–P04 | Binário próprio identificado |
| P07 | Validar a primeira sessão | Depende de P06 | Resultados V04–V09 do plano de validação |
| P08 | Validar persistência | Depende de P07 | Save de jogo e save state avaliados separadamente |
| P09 | Criar repositório público | Concluída a publicação inicial da documentação | Destino: rya3n/donkey-kong-country-pc; visibilidade pública e 12 arquivos conferidos pela API |

Não há responsáveis individuais ou prazos atribuídos além do contexto da conversa. Cada execução deve acrescentar resultados ao diagnóstico e ao log.

## Riscos técnicos atuais

- A ROM disponível não corresponde à revisão exigida: geração e execução suportadas seguem bloqueadas até a entrada correta.
- Código e release divergem: reproduzir o executável baixado exige resolver a identidade da base antes da comparação.
- Falta de compilador no PATH impede alguns testes: o resumo atual não é uma suíte aprovada.
- O upstream mantém recursos experimentais: ativá-los cedo dificulta separar defeitos da base de mudanças do projeto.
- Evidências iniciais sem log integral têm menor rastreabilidade: novas execuções precisam arquivar comandos e saídas.
