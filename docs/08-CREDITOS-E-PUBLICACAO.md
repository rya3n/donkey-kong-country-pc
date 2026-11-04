# Créditos, procedência e publicação

Este inventário registra os avisos encontrados nos projetos consultados. Não altera as licenças originais nem atribui uma única licença a todo o conjunto.

## Bases utilizadas

| Componente | Procedência | Aviso encontrado |
| --- | --- | --- |
| DKC1Recomp | [elliotttate/DKC1Recomp](https://github.com/elliotttate/DKC1Recomp) | Código de host e ferramentas identificado como MIT |
| snesrecomp | [elliotttate/snesrecomp](https://github.com/elliotttate/snesrecomp) | PolyForm Noncommercial 1.0.0 e avisos próprios |
| Metadados estruturais | [Yoshifanatic1/Donkey-Kong-Country-1-Disassembly](https://github.com/Yoshifanatic1/Donkey-Kong-Country-1-Disassembly) | Procedência GPL-3 descrita nos avisos do DKC1Recomp |
| SDL2 e miniz | Dependências descritas em `upstream/third_party/windows/README.md` | zlib e MIT, respectivamente |
| Integrações adicionais | `upstream/THIRD_PARTY_NOTICES.md` e avisos do pacote | Preservar os textos de cada componente usado |

Donkey Kong Country e seus elementos pertencem aos respectivos titulares. Este é um projeto de fãs e estudo, sem vínculo oficial com Nintendo ou Rare. A ROM local não faz parte do código público do projeto.

## Política proposta para o repositório

Publicar nossa documentação e, quando existirem, scripts e alterações próprias com sua procedência. Para a preparação inicial foi adotado um clone independente documentado, controlado por URL e revisões em config/upstream.lock.json. O diretório upstream/ contém um repositório Git próprio e permanece ignorado, preservando a procedência dos autores.

Manter fora da publicação ROMs, gráficos e áudio extraídos, fontes geradas da ROM, saves privados, estados, capturas do jogo, arquivos de download e binários baixados. Para uma futura distribuição de binários, realizar uma revisão específica de conteúdo e avisos; a autorização para um repositório público não significa que um pacote já tenha sido preparado.

Nenhuma licença foi escolhida para o nosso material novo nesta etapa. Não substituir ou remover licenças de terceiros.

## Conferência antes da publicação

1. Escolher e verificar o destino público correto.
2. Conferir a lista exata de arquivos e o histórico que serão enviados.
3. Confirmar que conteúdo local do jogo e credenciais não aparecem nesse conjunto.
4. Preservar créditos, revisões e avisos dos componentes efetivamente incluídos.
5. Fazer o README descrever o estado real: documentação, build ou versão testada.
6. Abrir o repositório publicado e verificar arquivos e visibilidade.

## Publicação inicial

Em 2026-11-04 foi criado o repositório público [rya3n/donkey-kong-country-pc](https://github.com/rya3n/donkey-kong-country-pc). O conjunto inicial publicado contém README, CHANGELOG, os nove documentos em docs/ e .gitignore; sua visibilidade e os 12 arquivos foram conferidos pela API. O clone de referência permanece independente e não integra essa publicação.

Os links do Notion privado foram preservados apenas em .project-local.md, ignorado pelo Git. Os documentos técnicos públicos não dependem do acesso a essas páginas para serem compreendidos. Nenhuma versão jogável própria é anunciada nesta publicação.
