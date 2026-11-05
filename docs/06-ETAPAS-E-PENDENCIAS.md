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
| P05 | Repetir suíte com logs completos | Executada; portabilidade pendente | 303 testes, 2 erros por cc/flags de sanitizers e 10 skips; log integral preservado |
| P06 | Gerar fontes e compilar | Concluída para protótipo sem janela | 39 variantes AOT e interpretador de apoio; MSVC/CMake/Ninja, comandos e hashes registrados |
| P07 | Validar a primeira sessão | Em andamento | Boot e entrada automatizada na fase; janela e interação ao vivo pendentes em V04–V09 |
| P08 | Validar persistência | Depende de P07 | Save de jogo e save state avaliados separadamente |
| P09 | Criar repositório público | Concluída a publicação inicial da documentação | Destino: rya3n/donkey-kong-country-pc; visibilidade pública e 12 arquivos conferidos pela API |
| P10 | Validar campanha e estabilidade | Após o build e os testes iniciais | Cobertura V14 aceita antes de iniciar a tradução |
| P11 | Inventariar, traduzir e revisar PT-BR | Depende de P10 | Cobertura de textos, fonte, acentos e regressão V15–V17 |
| P12 | Preparar aplicativo Windows | Após a base estável; validar após a tradução | Abertura direta e pacote verificados por V18–V19 |
| P13 | Investigar divergência ao ampliar AOT | Aberta; candidata retirada | Localizar primeira diferença de WRAM/áudio entre 39 e 55 variantes antes de promover cobertura |
| P14 | Implementar host interativo Rev 1 | Implementado; teste do usuário pendente | Janela 4:3, teclado, saída WinMM e abertura direta na fase; qualidade audiovisual e ações ao vivo ainda não verificadas |

Não há responsáveis individuais ou prazos atribuídos além do contexto da conversa. Cada execução deve acrescentar resultados ao diagnóstico e ao log.

A meta posterior acordada é PT-BR e abertura direta. A publicação inicial de documentação não conclui os marcos de estabilidade do jogo. Antes de M6, executar a campanha e aceitar a cobertura ampliada; depois revisar a tradução e testar o pacote final. A técnica de tradução e o formato de distribuição ainda serão definidos.

## Riscos técnicos atuais

- Rev 1 tem configuração própria ainda incompleta; muitos caminhos continuam no interpretador de apoio.
- A ampliação de AOT mudou WRAM e áudio; imagem final igual não permite aceitar a candidata.
- A base sem janela ainda não foi comparada com hardware ou referência independente; determinismo não comprova exatidão.
- A suíte pública anterior contém dois erros por dependências de cc/sanitizers; não é uma suíte aprovada.
- O upstream mantém recursos experimentais: ativá-los cedo dificulta separar defeitos da base de mudanças do projeto.
- Evidências iniciais sem log integral têm menor rastreabilidade: novas execuções precisam arquivar comandos e saídas.
