# Registro de decisões

Registro iniciado em 2026-11-04. “Aceita” indica orientação expressa do usuário; “proposta” indica recomendação técnica ainda ajustável. Alterações futuras devem preservar o motivo da decisão anterior e apontar o registro que a substituiu.

## D001 — Chegar a um port para PC

**Estado:** aceita. **Origem:** pedido inicial do usuário.

O objetivo é conseguir um port de Donkey Kong Country para PC. Recompilação e engenharia reversa podem ser usadas. A descoberta de uma base pública permite começar pela reprodução e pela validação do DKC1Recomp, dando crédito ao trabalho existente.

**Consequência:** não tratamos o projeto como uma decompilação inédita feita por nós. Reescritas próprias precisam de motivação e evidências.

## D002 — Usar USA v1.0 primeiro

**Estado:** substituída por D011. **Origem:** escolha inicial explícita do usuário na pergunta sobre a revisão da ROM.

Usar a revisão suportada para buscar primeiro uma sessão jogável. A alternativa era investigar e adaptar a v1.2 disponível, com mais incerteza antes do primeiro resultado.

**Consequência:** suporte à v1.2 é uma investigação futura. Não se propõe ignorar hashes ou converter revisão apenas renomeando o arquivo.

## D003 — Manter o projeto separado no Notion

**Estado:** aceita. **Origem:** orientação do usuário para não misturar Donkey Kong Country com outros assuntos.

Uma página própria agrupa os documentos deste projeto. As páginas de outros projetos permanecem fora dessa organização.

**Consequência:** os documentos locais e a cópia no Notion precisam indicar a edição; a sincronização é manual.

## D004 — Preparar um GitHub público

**Estado:** executada quanto à criação; publicação inicial de documentação. **Origem:** usuário autorizou e depois solicitou expressamente um repositório público.

O nome `donkey-kong-country-pc` foi sugerido pelo assistente e usado em [rya3n/donkey-kong-country-pc](https://github.com/rya3n/donkey-kong-country-pc). A tentativa inicial pelo navegador não chegou à criação; posteriormente, o repositório foi criado pela API com a autenticação existente do Git.

**Consequência:** preservar créditos e publicar apenas o material pretendido. Nome, destino e organização dos clones devem ser conferidos quando retomarmos essa etapa.

## D005 — Documentar antes de implementar

**Estado:** aceita e vigente. **Origem:** usuário pediu seguir com calma e fazer primeiro a documentação.

Priorizar clareza de objetivo, evidências, reprodução e critérios de aceite. O pedido posterior de log de atualizações passa a fazer parte dessa entrega.

**Consequência:** a documentação foi preparada antes de retomar a publicação. O pedido posterior de criar o repositório público permite publicar esses documentos; a implementação e a instalação de ferramentas continuam em etapas separadas.

## D006 — Estabelecer a imagem original como referência inicial

**Estado:** proposta técnica.

Validar inicialmente o framebuffer de 256×224 e registrar a proporção de exibição antes de testar widescreen ou efeitos adicionais. A intenção é obter uma referência que ajude a localizar diferenças futuras.

**Consequência:** recursos extras permanecem avaliáveis, com sua própria evidência. Essa proposta não altera defaults do código baixado nesta etapa.

## D007 — Fixar código e engine antes da compilação

**Estado:** decisão técnica implementada na preparação autorizada pelo usuário.

O clone inicial estava em `3eb9a10…`, enquanto o pacote v0.0.17 declara `559bab6…`. Foi escolhida e aplicada a v0.0.17 para alinhar fonte e pacote de referência, com engine `75223f3…` e recomp-net `6d848d6…`. Os hashes completos ficam em `config/upstream.lock.json`.

**Consequência:** o primeiro build deve partir desse conjunto. O verificador scripts/check_project.py detecta divergências das revisões. A mudança de checkout não representa geração de código do jogo nem validação de gameplay.

## D008 — Avaliar ferramentas pela necessidade

**Estado:** permissão de uso recebida; nenhuma adoção nova concluída.

O usuário disponibilizou seis repositórios como possíveis auxiliares. Eles entram no catálogo de referências, com função e aplicação propostas. Instalação ou dependência de build será registrada separadamente quando ocorrer.

## D009 — PT-BR e experiência de aplicativo após estabilização

**Estado:** aceita. **Origem:** usuário definiu a tradução para PT-BR e a abertura pelo executável como meta posterior ao port funcionando corretamente.

Primeiro validar amplamente a base; depois localizar o jogo e preparar a experiência de aplicativo Windows. O uso habitual deve ser abrir o executável e jogar, sem terminal ou escolha repetida de ROM.

**Consequência:** entram no roteiro tradução, revisão de fontes e telas, regressão e empacotamento. O formato de instalação e uma eventual importação única dos dados são propostas técnicas, ainda sem escolha definitiva. Nenhuma tradução ou alteração de runtime foi implementada nesta atualização.

## D010 — Instalar ferramentas no disco E:

**Estado:** aceita. **Origem:** usuário orientou novas instalações no E: e autorizou corrigir a instalação iniciada no C:.

Usar E:\Ferramentas como destino principal. Para BuildTools, remover a instância recém-criada no C: pelo desinstalador oficial e reinstalar no E:, preservando programas preexistentes. Conferir separadamente componentes compartilhados cujo instalador imponha outro destino; não apagar manualmente componentes registrados do Windows.

## D011 — Começar com a USA Rev 1 disponível

**Estado:** aceita quanto à revisão; integração técnica experimental. **Origem:** usuário pediu “vamo fazer com a que temos do 0”, após informar a ausência da USA v1.0.

Usar a USA v1.1 (Rev 1) identificada pelo hash de config/roms/usa-rev1.json. Ela substitui a v1.0 como entrada do nosso alvo. Começar uma configuração própria pelos vetores da ROM e uma integração mínima, reutilizando o gerador/runtime genérico fixado; o projeto não reescreve do zero todo o hardware do SNES.

**Consequência:** não alterar o verificador ou os metadados v1.0 do upstream para fingir compatibilidade. Fontes C derivadas e perfis de execução permanecem locais. O primeiro alvo é sem janela, 256×224 e híbrido, com interpretador de apoio. Ampliar AOT exige comparação de imagem, memória e áudio; a primeira tentativa de 55 variantes divergiu e foi retirada da base padrão de 39 variantes. Janela, controles ao vivo, persistência e campanha seguem pendentes.

## D012 — Iniciar preparação PT-BR preservando nomes e contexto

**Estado:** aceita em 2026-11-05. **Origem:** após aprovar os modos de tela, o usuário autorizou começar e pediu cuidado para não mudar nomes importantes nem o contexto.

Iniciar inventário, glossário e rascunhos editoriais. Preservar nomes próprios, rótulos completos de fases/lugares, referências de gameplay e personalidade dos personagens. Apelidos e termos ambíguos permanecem originais até revisão em contexto.

**Consequência:** a preparação de P11 pode avançar enquanto a cobertura de campanha P10 permanece aberta. Não declarar campanha aceita ou tradução integrada por esse início editorial. Dados extraídos e catálogos traduzidos ficam privados; o jogo só receberá textos após definir fonte, layout, integração e regressão. A meta final de estabilidade, PT-BR e aplicativo de D009 permanece vigente.
