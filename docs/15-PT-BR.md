# Preparação da tradução PT-BR

Iniciada em 2026-11-05 por autorização do usuário, com a orientação de preservar nomes importantes e o contexto do jogo. Esta etapa produz inventário, glossário e rascunhos. A campanha completa permanece pendente; o executável jogável não recebeu alterações de texto.

Atualização posterior: os menus foram localizados e um build experimental separado recebeu cinco rótulos gráficos em PT-BR. O executável habitual e os 12 rascunhos de falas permanecem como antes. Ver [Piloto dos menus](16-PILOTO-PT-BR.md). O relatório abaixo registra a extração inicial.

Em 2026-11-06, duas falas da Candy receberam redação revista e foram integradas ao piloto, sem aceite humano ainda. As outras dez permanecem fora do runtime. Ver [Falas da Candy](17-CANDY-PT-BR.md).

## Regra editorial

- Manter nomes próprios de personagens, inimigos, animais, lugares, fases, marcas e pessoas dos créditos. Preservar grafia, identidade e pontuação; não substituir por uma tradução literal.
- Preservar os nomes completos do mapa, incluindo os locais de serviço. O termo genérico “ponto de salvamento” pode aparecer numa instrução sem renomear Candy's Save Point.
- Traduzir menus, mensagens, instruções e falas com português brasileiro natural, mantendo a informação de gameplay e a personalidade de quem fala.
- Manter apelidos e termos ambíguos enquanto o contexto não estiver revisto. Não expandir uma abreviação, inventar parentesco ou trocar uma referência para facilitar o encaixe.
- Rever mensagens consecutivas em conjunto. Uma frase pode continuar no próximo registro; revisar uma entrada isolada pode mudar o sentido.
- Usar acentos corretos nos rascunhos. A fonte e o espaço disponível precisam ser verificados antes de integrar a tradução; remover acentos não é a solução padrão.

Exemplos protegidos: Donkey Kong, Diddy Kong, Cranky Kong, Candy Kong, Funky Kong, K. Rool, Rambi, Enguarde, Expresso, Winky, Squawks, Kremlings, DK, KONG e TNT. Nomes como Jungle Hijinxs permanecem originais. A política inicial está em localization/pt-BR/policy.json; os rótulos completos do mapa também são protegidos pelo verificador do catálogo.

Termos genéricos iniciais: save → salvar; lives → vidas; level → fase; bonus room → sala de bônus; jump → pular. Essa lista nunca se sobrepõe a um nome próprio completo.

## Inventário inicial da Rev 1

O leitor próprio confere tamanho e SHA-256 exatos antes de ler a ROM. Os limites abaixo foram conferidos nos dados da Rev 1. A referência de disassembly é da v1.0: não foram importados seus offsets como se fossem equivalentes. Por exemplo, o bloco de créditos da nossa entrada começa em 0x01EFFC, enquanto a referência identifica o início em 0x01EFDE.

| Região | Intervalo de arquivo, fim exclusivo | Registros | Conteúdo observado |
| --- | --- | --- | --- |
| map_names_en | 0x38A50B–0x38A7EA | 50 | Rótulos em inglês do mapa, incluindo o marcador ERROR; preservar nesta etapa |
| cast_en | 0x01DFD5–0x01E1BC | 47 | Nomes, títulos e falas curtas da apresentação do elenco |
| credits_en | 0x01EFFC–0x01F405 | 32 | Créditos, nomes e brincadeiras do encerramento |
| dialogue_en | 0x3C03C8–0x3C35CA | 217 | Bloco de falas em inglês |
| **Total inicial** | **Quatro regiões** | **346** | **Cobertura parcial do texto do jogo** |

Nessas regiões, o bit alto marca o último caractere de uma linha; parte dos blocos separa mensagens com zero. O leitor mantém linhas, offsets e comprimentos originais. Um caractere/controle desconhecido ou um limite incompleto interrompe a leitura; não é descartado silenciosamente.

Seleção de arquivo, modos de jogadores, texto desenhado como gráfico, instruções fora desses blocos e eventuais duplicatas continuam por localizar. Os 346 registros não constituem um inventário completo do jogo.

## Trabalho realizado

- Extraído catálogo privado de 346 registros, com identidade da ROM e campos de revisão.
- Criados 12 rascunhos editoriais: duas saudações de Cranky, quatro falas de Funky e seis falas de Candy. São propostas de texto, ainda sem revisão em tela, quebras de linha ou codificação de acentos aprovadas.
- Os 50 rótulos do mapa ficaram preservados; 284 registros permanecem sem tradução e 12 estão em rascunho.
- Verificador passou no catálogo real: IDs, fonte, offsets e nomes protegidos preservados. Os seis testes com textos sintéticos passaram, incluindo rejeição de nome alterado, fonte modificada e aprovação indevida do rascunho.
- Hashes da ROM e do executável permaneceram iguais. O leitor não escreve na ROM; nenhum save foi aberto e nenhuma dependência foi instalada.

O verificador estrutural não julga fidelidade semântica, humor ou naturalidade. Cada fala exige revisão no contexto, e nomes novos devem ser incorporados ao glossário conforme forem identificados.

## Reprodução local

```powershell
python scripts/inventory_rev1_text.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out experimental/usa-rev1/pt-BR/catalog-initial.json
python scripts/check_ptbr_catalog.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --original experimental/usa-rev1/pt-BR/catalog-initial.json --draft experimental/usa-rev1/pt-BR/catalog-draft-01.json
python -m unittest discover -s tests -p test_ptbr_review.py -v
```

O inventário recusa sobrescrever um arquivo existente. Para nova extração, escolher outro nome dentro de experimental/ ou evidence/, sem substituir o catálogo já editado. A ferramenta de inventário cria a fonte inicial; os rascunhos são trabalho editorial separado. Catálogos com textos originais e traduções ficam somente nas pastas privadas ignoradas; o repositório publica leitor, verificações, política e relatório.

Evidências desta execução: evidence/2026-11-05/pt-BR/. Catálogos locais: experimental/usa-rev1/pt-BR/. Não há patch de tradução ou alteração no runtime nesta entrega.

## Próxima etapa técnica

Localizar menus e suas tabelas/fontes na Rev 1, verificar os glifos de PT-BR e o espaço por linha, e definir como integrar dados traduzidos sem alterar endereços de código ou a identidade da ROM original. Depois, realizar um piloto visual separado, comparar execução, áudio e saves, e revisar as falas em tela. A cobertura de campanha continua registrada no plano de validação; a preparação editorial não a aprova automaticamente.

Referência estrutural consultada localmente: [disassembly de Yoshifanatic1, revisão c2080f4](https://github.com/Yoshifanatic1/Donkey-Kong-Country-1-Disassembly/tree/c2080f40469c716923f550706509a0d354229841). A referência declara suporte a USA v1.0 e licença GPLv3; nenhum trecho de sua implementação foi copiado para o leitor próprio. A extração desta etapa usa exclusivamente a ROM Rev 1 conferida.

## Revisão em jogo dos créditos

Em 2026-11-22, a revisão no piloto Windows PT-BR confirmou que os 32 registros do inventário `credits_en` cobrem os dois blocos exibidos no jogo. O leitor de inventário mantém os IDs atuais. Os intervalos abaixo usam offsets do arquivo USA v1.1 (Rev 1), com fim exclusivo.

| Trecho | Intervalo | Registros | O que revisar |
| --- | --- | ---: | --- |
| Créditos falsos no navio | `0x01EFFC–0x01F08F` | 7 | Título, cinco atribuições e a pergunta final. Preservar o efeito da grafia proposital com K, os nomes, o alinhamento pontilhado e o ponto de interrogação |
| Créditos reais após o elenco | `0x01F08F–0x01F405` | 25 | Cabeçalho e 24 grupos de crédito. Localizar títulos e funções e preservar grafia, ordem e associação de nomes e marcas |
| Apresentação do elenco | `0x01DFD5–0x01E1BC` | 47 | Conferir títulos e frases em revisão própria. Preservar nomes de personagens |

O inventário registra linhas de até 24 caracteres no trecho falso e até 28 no real. Use essas medidas para priorizar os casos de encaixe. A aprovação em PT-BR exige verificar a largura e o alinhamento na rolagem, os glifos das funções localizadas e a associação de cada nome ao seu grupo. Termos editoriais como “Programação”, “Testes” e “Agradecimentos” servem de referência para os rótulos de função.

Em dois perfis de QA, a revisão conferiu 17 capturas da sequência falsa e 41 da real. No navio, o quadro 229.272 mostra a pergunta final, e o quadro 229.811 marca o retorno do controle. No encerramento real, o quadro 245.894 mostra a abertura dos créditos, o quadro 250.889 mostra a última atribuição e o quadro 251.294 já mostra a sequência de abertura do jogo. As funções amostradas continuam em inglês. O manifesto do piloto contém 226 regiões de patch e nenhuma se sobrepõe aos intervalos de créditos ou de elenco. Os 59 testes Python passaram.

Os dois blocos podem ser alcançados pelo [roteiro do final da campanha](../recipes/usa-rev1/campaign-to-ending-title.inputs). As capturas de revisão ficam em `credits-review-fake/` e `credits-review-real/`, dentro de `evidence/2026-11-10/pt-BR/campaign-start/`. A tradução em jogo, a revisão dos glifos localizados e a escuta em janela permanecem pendentes.

### Prévia da rolagem com texto próprio

O [gerador de prévia](../scripts/preview_credit_text.py) lê um arquivo JSON UTF-8 com uma lista de linhas e cria um HTML local. Ele preserva as linhas em branco, normaliza acentos para NFC e destaca os trechos que excedem a largura de referência. A prévia tem pausa e controle de posição.

```powershell
python scripts/preview_credit_text.py --input evidence/texto-proprio.json --columns 24 --out evidence/previa-24.html
python scripts/preview_credit_text.py --input evidence/texto-proprio.json --columns 28 --out evidence/previa-28.html
```

Em 2026-11-22, o teste com 11 linhas sintéticas confirmou duas linhas acima da referência de 24 caracteres e uma acima da referência de 28. No Edge, a rolagem, a pausa, o controle de posição e os acentos passaram em larguras de 390 e 1.100 pixels. Os 59 testes Python passaram. Os resultados se referem à fonte do navegador. A fonte do jogo e a integração de um catálogo próprio ficam na etapa V15–V16.

## Auditoria de cobertura do piloto (V15)

Em 2026-11-23, o verificador comparou os 346 registros do catálogo privado com os 226 intervalos do manifesto PT-BR. Para cada registro, o relatório contou coincidências exatas de início e fim, outras sobreposições e ausência de sobreposição. O executável sem janela confirmou a identidade do conjunto de alterações do manifesto ao rodar 600 quadros com a Rev 1.

| Grupo inventariado | Registros | Com rascunho | Intervalo exato no manifesto | Situação |
| --- | ---: | ---: | ---: | --- |
| Diálogos | 217 | 217 | 217 | O piloto cobre os intervalos das falas da Candy, do Funky e do Cranky. A revisão em contexto segue na V16. |
| Nomes do mapa | 50 | 0 | 0 | Preservados pela política editorial. |
| Apresentação do elenco | 47 | 0 | 0 | Cobertura de títulos e frases a revisar. |
| Créditos falsos e reais | 32 | 0 | 0 | A revisão da referência e a prévia no navegador estão registradas acima. A integração em jogo segue pendente. |

Nenhum registro teve sobreposição parcial ou com intervalo de tamanho diferente. Nove regiões do manifesto ficam fora desses registros. Os rótulos gráficos e a revisão de telas têm evidências próprias. O título interno do menu de salvamento da Candy apareceu em inglês na validação de Monkey Mines. A revisão desse título deve preservar o nome completo do local no mapa. [Piloto dos menus](16-PILOTO-PT-BR.md) · [Visita à Candy](32-CAMPANHA-PT-BR-AUDIO-E-PROGRESSO.md#visitas-de-serviço-em-monkey-mines)

O escopo do resultado são os intervalos da Rev 1 contidos no catálogo. A presença no manifesto confirma a cobertura estrutural, e a aceitação da localização exige leitura em contexto, revisão de acentos e verificação do encaixe na tela.

```powershell
$catalogo = 'experimental/usa-rev1/pt-BR'
python -B scripts/check_ptbr_catalog.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' `
    --original "$catalogo/catalog-initial.json" --draft "$catalogo/catalog-draft-16.json" `
    --pilot-manifest "$catalogo/menu-pilot/manifest.json"
```

O campo `pilot_coverage` contém contagens por grupo e por tipo de correspondência. O verificador rejeita um manifesto de outra ROM e intervalos inválidos ou sobrepostos. A suíte Python passou com 62 testes. Evidências locais em `evidence/2026-11-23/v15-cobertura/`.

## Título do menu de salvamento da Candy (V16)

A inspeção da visita em Monkey Mines confirmou três elementos distintos. A saudação da Candy aparece em PT-BR, o título dentro do menu de slots aparece em inglês e o mapa exibe **Candy's Save Point**. A proposta de rótulo para o menu é **Salvar com a Candy**. A revisão deve manter o nome completo do ponto no mapa e conferir o encaixe do título acima dos slots. [Visita em Monkey Mines](32-CAMPANHA-PT-BR-AUDIO-E-PROGRESSO.md#visitas-de-serviço-em-monkey-mines)

O verificador usa a receita curta de QA da Candy nas duas compilações existentes. Cada captura começa em um perfil vazio. Ele compara os quadros da fala, do menu e da volta ao mapa e conta os pixels alterados na faixa reservada ao título. O mapa desse ensaio rápido é o do primeiro mundo. A inspeção de Monkey Mines segue como referência da visita pela rota da campanha.

```powershell
python -B scripts/verify_ptbr_candy_ui.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' `
    --out evidence/revisao-menu-candy
```

O diretório de saída deve ser novo. As capturas do framebuffer, o manifesto da execução e os saves criados pelo ensaio ficam em `evidence/`.

Em 2026-11-23, duas rodadas produziram os mesmos resultados por build:

| Quadro | Cena | Comparação entre a versão base e o piloto |
| ---: | --- | --- |
| 4.440 | Fala da Candy | 1.498 pixels diferentes, todos dentro da faixa de diálogo. |
| 4.800 | Menu de salvamento | Zero pixels diferentes, inclusive na faixa do título. |
| 4.936 | Volta ao mapa | Zero pixels diferentes. Os arquivos de save de 2.048 bytes coincidiram entre si e com o relatório da SRAM. |

A cadeia digital de áudio coincidiu até o quadro 4.800 e divergiu até 4.936 após a confirmação do slot. O número de quadros com áudio ativo foi igual. A causa e o efeito audível ficam para a regressão V17. A revisão confirmou o título em inglês no build atual. A troca do rótulo em jogo e a conferência do novo desenho continuam na V16. Os 62 testes Python passaram. Evidências locais em `evidence/2026-11-23/v16-candy-ui/`.

A V17 localizou a primeira diferença entre os quadros 4.832 e 4.835 e mediu o deslocamento na volta ao mapa. [Comparação quadro a quadro](32-CAMPANHA-PT-BR-AUDIO-E-PROGRESSO.md#diferença-digital-após-salvar-na-candy-v17).

### Título integrado no piloto

Em 2026-11-26, o piloto passou a exibir **SALVAR COM A CANDY** acima dos slots. O gerador usa a fonte do piloto e os tiles exclusivos do título. O mapa da Candy recebe sua própria faixa de tiles em `0x31C887–0x31C987`. Os glifos ficam nos gráficos compartilhados com a seleção de arquivo, fora dos tiles usados pelos retratos dos slots e pelo menu de seleção. **Candy's Save Point** permanece com o nome original no mapa.

No quadro 4.800, os 1.594 pixels diferentes ficaram na faixa do título. A leitura da captura confirmou o texto inteiro acima dos slots. A WRAM, a SRAM e a cadeia de áudio coincidiram com as do piloto anterior na fala, no menu e na volta ao mapa. As capturas da seleção de arquivo e dos modos de jogo foram idênticas às do piloto anterior. A versão base e o novo piloto gravaram o mesmo save de 2.048 bytes.

O teste de persistência confirmou o save e a reabertura a frio em processos novos no executável Windows e no runner sem janela. Os 65 testes Python e os três alvos do CTest de cada compilação passaram. As evidências ficam em `evidence/2026-11-26/v16-candy-title/`. A revisão de elenco e créditos continua em V15–V16.
