# Registro de decisões

Registro iniciado em 2026-11-04. “Aceita” indica orientação expressa do usuário; “proposta” indica recomendação técnica ainda ajustável. Alterações futuras devem preservar o motivo da decisão anterior e apontar o registro que a substituiu.

## D001 — Chegar a um port para PC

**Estado:** aceita. **Origem:** pedido inicial do usuário.

O objetivo é conseguir um port de Donkey Kong Country para PC. Recompilação e engenharia reversa podem ser usadas. A descoberta de uma base pública permite começar pela reprodução e pela validação do DKC1Recomp, dando crédito ao trabalho existente.

**Consequência:** não tratamos o projeto como uma decompilação inédita feita por nós. Reescritas próprias precisam de motivação e evidências.

## D002 — Usar USA v1.0 primeiro

**Estado:** aceita. **Origem:** escolha explícita do usuário na pergunta sobre a revisão da ROM.

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

**Estado:** proposta técnica; revisão específica ainda em aberto.

O clone está em `3eb9a10…`, enquanto o pacote v0.0.17 declara `559bab6…`. Fixar um conjunto antes de compilar e comparar.

**Consequência:** não atribuir à base local um resultado obtido em outra revisão. O clone não foi atualizado ou modificado durante a documentação.

## D008 — Avaliar ferramentas pela necessidade

**Estado:** permissão de uso recebida; nenhuma adoção nova concluída.

O usuário disponibilizou seis repositórios como possíveis auxiliares. Eles entram no catálogo de referências, com função e aplicação propostas. Instalação ou dependência de build será registrada separadamente quando ocorrer.
