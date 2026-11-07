# Dicas do Cranky para Monkey Mines em PT-BR

Entrega de 2026-11-06 no piloto separado USA v1.1 (Rev 1). Integradas quatro dicas identificadas no grupo de Monkey Mines. O Cranky passa a ter seis saudações e nove dicas traduzidas: cinco de Kongo Jungle e quatro de Monkey Mines. Com Candy e Funky, são 27 mensagens no piloto; demais diálogos continuam em etapas próprias.

## Textos e pistas

| Fase | Redação em PT-BR | Pista mantida |
| --- | --- | --- |
| Bouncy Bonanza | Use o pneu: rinoceronte dourado em Bouncy Bonanza. | Pneu e rinoceronte dourado, por extenso |
| Stop & Go Station | As bananas de Stop & Go Station mostram o caminho! | Bananas como orientação |
| Mine Cart Carnage | Evite Mine Cart Carnage e pule cedo para ganhar a vida extra. | A construção enigmática do original e o salto antecipado |
| Millstone Mayhem | Role um pneu para seguir pelo caminho certo em Millstone Mayhem! | Rolar o pneu, sem confundir com o ataque de rolamento do Kong |

Os quatro nomes completos foram preservados e adicionados à proteção automática. A tradução de Bouncy Bonanza mantém a descrição genérica do rinoceronte dourado, sem substituí-la por Rambi ou abreviá-la. Não foi criada uma dica adicional para as outras fases do mundo sem um texto correspondente neste grupo.

Nas duas referências inglesas a borracha, a redação usa pneu. O [guia de Brother Reed](https://gamefaqs.gamespot.com/snes/588282-donkey-kong-country/faqs/8224), nas seções dessas fases, relaciona o pneu ao rinoceronte dourado e às rotas de Millstone Mayhem. Essa consulta apoia a escolha editorial; a fonte principal das falas continua sendo a própria ROM Rev 1. Não foi copiado um passo a passo do guia para os diálogos.

A dica de Stop & Go Station não virou uma ordem de sempre andar à direita. Em Mine Cart Carnage, mantida a formulação do original sem inventar distância, quadro de salto ou instrução nova de atalho.

## Prévia e piloto

Galeria privada: evidence/2026-11-06/pt-BR/monkey-mines/verified-all/preview.html. As quatro capturas nativas têm títulos com os nomes das fases e legendas em PT-BR. Elas mostram a seleção técnica no cenário do Cranky; não demonstram a coleta dos segredos nas fases.

Abrir **Testar DKC - PT-BR.cmd** para jogar no perfil próprio do piloto. O aplicativo mantém as condições originais de seleção das falas; **Jogar DKC.cmd** continua abrindo o executável habitual, com seus saves separados.

## Integração

O arquivo localization/pt-BR/cranky-tips-pilot.json agora reúne nove dicas com metadados de mundo. A função make_cranky_tips_patch valida a associação entre endereço, tamanho, fase e mundo, além dos dois grupos de ponteiros ingleses. O grupo Monkey Mines em 0x3C0194–0x3C01A4 contém os quatro ponteiros repetidos; a ordem dos registros foi conferida na Rev 1.

As mensagens em 0x3C1074, 0x3C10A6, 0x3C10D9 e 0x3C1115 mantêm 50, 51, 60 e 70 bytes, respectivamente. Preservados ponteiros, três linhas por mensagem, terminadores e paridades. Somente espaços laterais completam os registros; nenhum novo glifo ou código de jogo foi necessário.

As 32 regiões anteriores, incluindo a fonte e o ê corrigido, mantêm o hash ce8e00e26a6bdd16bdf8767cd6b8e0970b86aae33ca7e0b91eb20f49ed1fc2e0 ao serem recompostas sem as quatro regiões novas. O piloto agora aplica 36 regiões de dados à cópia da ROM em memória. O arquivo da ROM, código do cartucho, unidades AOT e relógio de 60,0988 Hz permanecem intactos.

O verificador aceita --world monkey-mines ou --world kongo-jungle junto de --character cranky-tips --all-messages. O filtro afeta apenas a galeria e os casos de QA. O diagnóstico DKC_REV1_QA_CRANKY_MESSAGE continua exclusivo do runner sem janela, selecionando o mesmo endereço no original e no piloto para comparar o renderizador.

## Verificações

- Build Release e 45 testes Python passaram, incluindo os nove registros, nomes completos, associação de mundo e o novo grupo de ponteiros.
- As quatro dicas passaram individualmente: áudio completo e 128 KiB de WRAM iguais ao original; diferenças de imagem apenas na faixa do diálogo. Capturas inspecionadas, legíveis e sem cortes.
- Duas dicas de Kongo Jungle foram comparadas novamente com o original e com a entrega anterior. Framebuffer, WRAM e áudio do piloto coincidiram com os resultados anteriores.
- Na regressão de Coral Capers, o contador de passos interpretados ficou 32 abaixo da entrega anterior, com imagem, WRAM e áudio iguais no checkpoint. Essa diferença foi registrada em kongo-previous-build-check.json; não representa mudança de FPS ou alteração da fonte. Nas quatro dicas novas, os deltas em relação ao original foram 0, 0, +8 e 0.
- Menus e entrada da fase passaram nos quadros 1.700, 2.300 e 4.800. Na fase, imagem, áudio e WRAM coincidiram com a versão habitual.
- Um ciclo Candy/reinício coincidiu entre aplicativo, runner e disco em perfis de QA separados; SRAM igual ao fixture anterior. Nenhum save pessoal foi usado.
- Catálogo privado draft-07 passou nas verificações de nomes e integridade: 50 registros preservados, 27 rascunhos históricos e 269 ainda sem tradução. O estado draft não substitui os aceites em relato dos lotes anteriores.
- ROM e executável habitual conservaram os hashes. Nenhuma nova instalação.

Revisão humana destas quatro prévias, condições normais das falas, coleta dos segredos e campanha completa continuam pendentes.

## Reprodução

Fechar os processos de QA antes de recompilar.

```powershell
./scripts/build_rev1.ps1 -HeadlessOnly
./scripts/build_ptbr_pilot.ps1
python -m unittest discover -s tests -p 'test_ptbr*.py' -v
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/monkey-hints-check --character cranky-tips --world monkey-mines --all-messages
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/monkey-kongo-regression --character cranky-tips --world kongo-jungle --all-messages --message 0f35 --message 102e
python scripts/verify_ptbr_menu_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/monkey-menu-check
python scripts/verify_rev1_saves.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/monkey-save-check --build-dir build/ptbr-pilot --desktop-name DKC-Rev1-PTBR-Piloto.exe --repeats 1
```

Evidências privadas em evidence/2026-11-06/pt-BR/monkey-mines/: verified-all/, kongo-regression/, menu-gameplay/, saves/, prior-patches-check.json, kongo-previous-build-check.json, editorial-review.json, unit-tests.log e logs de build. Os dados extraídos, capturas, dumps, saves e binários permanecem fora do GitHub público.

Etapa seguinte implementada: [Dicas de Vine Valley](23-DICAS-VINE-VALLEY-PT-BR.md). O filtro `--world monkey-mines` permite repetir somente este lote com o verificador atual. As quatro prévias de Monkey Mines continuam com revisão humana pendente; campanha e coleta dos segredos permanecem na matriz de validação.
