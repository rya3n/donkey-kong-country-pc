# Log de atualizações

As datas deste histórico usam o fuso America/Sao_Paulo. As entradas mais recentes ficam no início. Este log registra o nosso projeto; as versões do DKC1Recomp são identificadas como versões de terceiros.

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
