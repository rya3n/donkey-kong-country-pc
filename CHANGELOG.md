# Log de atualizações

As datas deste histórico usam o fuso America/Sao_Paulo. As entradas mais recentes ficam no início. Este log registra o nosso projeto; as versões do DKC1Recomp são identificadas como versões de terceiros.

## 2026-11-04 — Criação do repositório público

### Realizado

- Criado o repositório público [rya3n/donkey-kong-country-pc](https://github.com/rya3n/donkey-kong-country-pc), conforme pedido expresso do usuário.
- Preparado o conjunto inicial com README, log, nove documentos técnicos e .gitignore.
- Adicionadas exclusões para ROMs, saves, arquivos gerados, builds, downloads, runtime e clone independente do upstream.
- Movidos os links do Notion privado do README para .project-local.md, mantido somente no computador.
- Mantidos os créditos e a identificação do DKC1Recomp como base de referência.

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
