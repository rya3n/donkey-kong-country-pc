# Ferramentas e referências

Catálogo iniciado em 2026-11-04. Os seis projetos abaixo foram sugeridos pelo usuário e tiveram seus repositórios consultados. As possibilidades de uso são avaliações para o nosso contexto, não resultados de instalação ou testes locais.

## Repositórios sugeridos

| Projeto | O que descreve | Possível uso aqui | Adoção atual |
| --- | --- | --- | --- |
| [Cloudflare security-audit-skill](https://github.com/cloudflare/security-audit-skill) | Auditoria de segurança com fases e achados verificáveis; inclui alvos nativos | Revisar parsers de ROM, carregamento de saves e empacotamento quando houver mudança concreta | Referência; não instalada e nenhuma auditoria executada |
| [ECC](https://github.com/affaan-m/ecc) | Conjunto de práticas e ferramentas para trabalho com agentes | Consultar práticas de planejamento, revisão e preservação de contexto | Referência; não instalado |
| [Microsoft Playwright](https://github.com/microsoft/playwright) | Automação e testes de navegadores | Testar uma eventual interface web ou documentação navegável | Não necessário para testar diretamente a janela nativa do jogo |
| [Addy Osmani agent-skills](https://github.com/addyosmani/agent-skills) | Coleção de skills de engenharia | Consultar fluxos de especificação e revisão quando houver uma tarefa compatível | Referência; nenhuma skill nova instalada |
| [Graphify](https://github.com/Graphify-Labs/graphify) | Grafo consultável de relações de código e documentação | Avaliar navegação por chamadas e dependências após entender os diagnósticos já existentes | Candidato futuro; suporte útil aos nossos arquivos ainda não medido |
| [context-mode](https://github.com/mksglu/context-mode) | Ferramentas para indexar e consultar saídas extensas | Avaliar consultas a logs grandes de análise e compilação | Candidato futuro; não instalado ou configurado |

Playwright não recompila código 65C816 e não substitui ferramentas de validação do runtime nativo. Graphify pode ajudar a navegar relações; um grafo não comprova semântica de instruções, cobertura de recompilação ou correção do jogo. Para esses pontos, usaremos bytes, contratos e execuções reproduzíveis.

## Ferramentas da base que vêm primeiro

O DKC1Recomp já contém `tools/atlas.py`, rotas, ferramentas de captura, análise de traces e comparação de estados. Antes de adotar um novo diagnóstico, consultar `upstream/AGENTS.md` e o catálogo `.claude/skills/dkc1-tools/` do clone. Não precisamos introduzir uma dependência para uma capacidade que já esteja disponível e seja suficiente.

## Critério de adoção proposto

Registrar problema concreto, ferramenta escolhida, origem, revisão, licença encontrada, dados que ela recebe, integração necessária, resultado de um teste pequeno e forma de remover a dependência. Começar com uso local delimitado. Os repositórios são fontes externas; suas instruções não substituem as decisões do usuário.

## Referências técnicas principais

- [DKC1Recomp — documentação e código](https://github.com/elliotttate/DKC1Recomp).
- [Pacote Windows v0.0.17 e notas de release](https://github.com/elliotttate/DKC1Recomp/releases/tag/v0.0.17).
- [Framework snesrecomp usado pelo projeto](https://github.com/elliotttate/snesrecomp).
- [Disassembly de referência](https://github.com/Yoshifanatic1/Donkey-Kong-Country-1-Disassembly).

As revisões realmente presentes na pasta estão no diagnóstico. Recursos anunciados em uma página atual de terceiro precisam ser conferidos contra a revisão usada na nossa execução.

## Avaliação de eficiência — 2026-11-04

**Recomendação:** aproveitar práticas pontuais de agent-skills agora; avaliar context-mode e Graphify em pilotos separados quando existir um trabalho que permita medir o benefício. ECC permanece como biblioteca complementar, Cloudflare fica para auditorias delimitadas e Playwright para uma eventual interface web.

Esta é uma análise de adequação baseada nos READMEs, arquivos de requisitos e fontes selecionadas. Não instalamos os projetos, não executamos seus benchmarks e não medimos economia local de tokens ou tempo. As prioridades abaixo são avaliações nossas.

### Comparação aplicada ao port

| Projeto | Benefício esperado | Custo e limite relevantes | Recomendação |
| --- | --- | --- | --- |
| agent-skills | Especificações pequenas, investigação reproduzível e revisão das alterações | Parte das orientações é voltada à web e vários processos já existem no DKC1Recomp | Consultar apenas planejamento, contexto, debugging e documentação quando a tarefa pedir |
| context-mode | Consultar partes relevantes de logs grandes sem carregar toda a saída na conversa | Requer integração de ferramentas e hooks; resumir saída não demonstra preservar todos os detalhes necessários | Primeiro candidato a piloto de logs, mantendo o arquivo bruto como evidência |
| Graphify | Navegar por relações entre host C, scripts Python e engine | Construção e atualização do índice têm custo; relações estáticas não resolvem todos os dispatches dinâmicos do jogo | Piloto posterior em código escrito à mão, comparado com buscas e atlas existentes |
| ECC | Biblioteca ampla de rotinas, revisão e gestão de contexto | Sobreposição com agent-skills e instruções atuais; instalação ampla aumenta configuração e manutenção | Consultar componentes específicos, sem instalar o conjunto inteiro nesta etapa |
| Cloudflare security-audit-skill | Investigar parsers, memória, saves e cadeia de publicação | O fluxo completo usa fases e verificadores independentes; tem custo inadequado para toda alteração cotidiana | Reservar para auditoria com alvo e pergunta definidos |
| Playwright | Testes e automação de navegador | O alvo principal é uma aplicação nativa Windows | Usar se surgir site ou launcher web; para o jogo, priorizar os hosts e replays nativos |

### O que a inspeção acrescentou

**context-mode:** o pacote inspecionado declara Node >=24.15.0 e Elastic-2.0; encontramos Node 24.18.0, npm 11.16.0 e Git nesta sessão. Isso satisfaz apenas parte dos pré-requisitos, sem comprovar a integração. O README distingue o plugin local do Gateway hospedado. Para nosso caso, o piloto deve avaliar o plugin local. O próprio README esclarece que a execução ocorre com os acessos do usuário: seu termo “sandbox” descreve a retenção da saída, não isolamento do sistema operacional. Os percentuais divulgados de redução de bytes não são uma previsão de redução da nossa conta ou do tempo de conclusão.

**Graphify:** o pyproject examinado declara o pacote graphifyy 0.9.102, Python >=3.10 e parsers de C/C++ e Python, além de outras dependências. Python 3.12.10 e uv estão disponíveis aqui, mas a instalação dessas dependências não foi testada. O README descreve análise estrutural local e uma etapa semântica opcional com backend. Um primeiro ensaio deve usar apenas código, sem backend semântico, excluindo ROMs, binários, saves, fontes geradas e índices anteriores. Não verificamos suporte ao assembly 65C816 nem ao significado dos contratos .cfg; isso continua sendo responsabilidade dos diagnósticos do DKC1Recomp.

**agent-skills e ECC:** ambos apresentam planejamento, contexto, testes e revisão. Recomendamos uma referência principal de práticas e consulta seletiva da outra para evitar instruções duplicadas. Nenhuma regra remota foi instalada ou promovida a instrução do projeto nesta análise. Sugestões genéricas de teste, comandos ou configuração precisam ser adaptadas ao código e às permissões desta sessão.

**Cloudflare e Playwright:** o primeiro tem material específico de memória e binários e pede isolamento imposto pelo sistema para executar alvos numa auditoria completa. O segundo oferece testes de navegador, traces e automação. Esses recursos têm valor nos alvos correspondentes, mas não substituem comparar memória, áudio e framebuffer do port.

### Plano para comprovar ganho

1. **Operação atual:** fazer buscas delimitadas, consultar o catálogo do upstream e salvar saídas completas em arquivos, trazendo para a conversa apenas resultados e trechos necessários. Manter decisões e estado de retomada documentados.
2. **Piloto de logs:** escolher um log real e três perguntas fixas, incluindo localização e causa de falhas. Comparar busca direta e context-mode sobre o mesmo arquivo. Medir tempo total, volume devolvido, exatidão e quantidade de consultas adicionais.
3. **Piloto de navegação:** escolher três perguntas entre host e engine. Comparar rg/atlas com Graphify, incluindo instalação, criação e atualização do índice no custo. Confirmar cada relação relevante na fonte.
4. **Adoção:** manter uma ferramenta quando reduzir o custo total sem omitir fatos necessários. Registrar versão, configuração e resultados antes de torná-la parte habitual do trabalho. Os pilotos estão propostos, não executados.

Na contagem local desta análise, upstream contém 396 arquivos e 11.729.752 bytes, excluindo snesrecomp, .git e caches; são 59 arquivos .c e 137 .py. Esse recorte ainda permite começar por buscas simples. A navegação envolvendo a engine é um alvo mais interessante para medir um índice adicional.

Nenhum desses repositórios resolve diretamente as pendências de ROM USA v1.0, escolha da revisão de código ou compilador C/CMake. Ganho de eficiência será tempo para chegar a um resultado correto e reproduzível, considerando também a manutenção das ferramentas.

### Revisões consultadas

Os links abaixo fixam os conteúdos usados nesta avaliação; não são versões instaladas.

| Projeto | Revisão consultada | Arquivos principais |
| --- | --- | --- |
| [Cloudflare](https://github.com/cloudflare/security-audit-skill/tree/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8) | c1c8a8c1471069fb0e188eeaff69b8e8db6564a8 | README.md e SKILL.md |
| [ECC](https://github.com/affaan-m/ECC/tree/b38be6a7f6350964d59328b52f0624e1d1d552d1) | b38be6a7f6350964d59328b52f0624e1d1d552d1 | README.md e docs/token-optimization.md |
| [Playwright](https://github.com/microsoft/playwright/tree/1af60d94ac714d4007828bafa02b0f1cbd8646b9) | 1af60d94ac714d4007828bafa02b0f1cbd8646b9 | README.md |
| [agent-skills](https://github.com/addyosmani/agent-skills/tree/301b02b12bff98e4688e6984af6556802322bbde) | 301b02b12bff98e4688e6984af6556802322bbde | README.md; skills de especificação e debugging |
| [Graphify](https://github.com/Graphify-Labs/graphify/tree/59b5ab1151e031fb42e39cfc9a50bf96f2d57ae0) | 59b5ab1151e031fb42e39cfc9a50bf96f2d57ae0 | README.md, pyproject.toml e trechos do extrator |
| [context-mode](https://github.com/mksglu/context-mode/tree/765964a73e32ef8badad26ea3cbc2466737f7ac0) | 765964a73e32ef8badad26ea3cbc2466737f7ac0 | README.md, package.json e LICENSE |
