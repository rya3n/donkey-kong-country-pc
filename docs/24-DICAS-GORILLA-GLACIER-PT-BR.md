# Dicas do Cranky para Gorilla Glacier em PT-BR

Entrega de 2026-11-07 no piloto separado USA v1.1 (Rev 1). Integrado o terceiro grupo da tabela inglesa do Cranky (`0x3C01A4–0x3C01B4`), correspondente às cinco dicas de Gorilla Glacier. O Cranky passa a ter seis saudações e dezessete dicas traduzidas: cinco de Kongo Jungle, quatro de Monkey Mines, três de Vine Valley e cinco de Gorilla Glacier. Com Candy e Funky, são 35 mensagens no piloto; demais diálogos continuam em etapas próprias.

## Textos e pistas

| Fase | Redação em PT-BR | Pista mantida |
| --- | --- | --- |
| Snow Barrel Blast | Em Snow Barrel Blast, descer nem sempre tira você do jogo; pode fazer você ir adiante. | Descer/cair no trecho de barris como atalho para avançar na fase |
| Croctopus Chase | Em Croctopus Chase, há um jeito certo e um jeito errado pra passar pelos barris. | Contraste entre o caminho certo e o errado ao cruzar os barris |
| Ice Age Alley | Em Ice Age Alley, aves do mesmo bando voam juntas pra dar asas a você. | Usar o bando de aves alinhadas para alcançar as asas (Expresso) |
| Slipslide Ride | Pular bem no saltador vai deslizar você ao sucesso em Slipslide Ride! | Quicar no inimigo saltador para alcançar a corda e deslizar até o segredo |
| Torchlight Trouble | O TNT rende um bom par de estouros de parede em parede em Torchlight Trouble. | Usar dois barris de TNT para abrir paredes com segredos na fase |

Os cinco nomes completos (Snow Barrel Blast, Croctopus Chase, Ice Age Alley, Slipslide Ride e Torchlight Trouble), além de Croctopus e TNT, foram preservados e protegidos pelo verificador em `localization/pt-BR/policy.json`.

## Prévia e piloto

Galeria privada: `evidence/2026-11-07/pt-BR/gorilla-glacier/verified-all/preview.html`. As cinco capturas nativas mostram o título de cada fase e a legenda em PT-BR. Elas documentam a seleção técnica no cenário do Cranky; não demonstram a coleta dos segredos nas fases.

Abrir **Testar DKC - PT-BR.cmd** para jogar no perfil próprio do piloto. O aplicativo mantém as condições originais de seleção das falas; **Jogar DKC.cmd** continua abrindo o executável habitual, com seus saves separados.

## Integração

O arquivo `localization/pt-BR/cranky-tips-pilot.json` reúne agora dezessete dicas com metadados de mundo (`kongo-jungle`, `monkey-mines`, `vine-valley` e `gorilla-glacier`). A função `make_cranky_tips_patch` valida a guarda do grupo `0x3C01A4–0x3C01B4` (`115b 11b0 11ff 1244 1288 115b 11b0 11ff`) e a associação entre endereço, tamanho, fase e mundo nos dezessete registros.

As mensagens em `0x3C115B`, `0x3C11B0`, `0x3C11FF`, `0x3C1244` e `0x3C1288` mantêm 85, 79, 69, 68 e 76 bytes, respectivamente, preservando ponteiros, três linhas por mensagem, terminadores e paridades (incluindo a primeira linha de 30 colunas originais em `0x3C115B`). A fonte compartilhada e seus quatro glifos acentuados (`á`, `ê`, `ó`, `é`) foram reutilizados sem novos slots ou alterações na tabela de tiles.

As 39 regiões anteriores mantêm exatamente o hash `e80b1b28c2cf1dfeca399eb9043ebb77aea1e777638d5c410580759ac7635d10` ao serem recompostas sem as cinco regiões novas. O piloto aplica agora 44 regiões de dados à cópia da ROM em memória (`patchset_sha256` `7db4204137a0daaa27989d298f7c0ccd9f2f85850ec7a49e2ec554680d1b5849`). O arquivo da ROM, código do cartucho, unidades AOT e relógio de 60,0988 Hz permanecem intactos.

O verificador `scripts/verify_ptbr_candy_pilot.py` aceita `--world gorilla-glacier` junto de `--character cranky-tips --all-messages`. O diagnóstico `DKC_REV1_QA_CRANKY_MESSAGE` continua exclusivo do runner sem janela.

## Verificações

- Build Release e 47 testes Python passaram, cobrindo os dezessete registros, nomes completos, associação de mundo e a guarda de ponteiros de Gorilla Glacier.
- As cinco dicas passaram individualmente: áudio completo e 128 KiB de WRAM inteiramente iguais ao original (`interpreted_steps_delta` de -16, 0, 0, -16 e 0); diferenças de imagem apenas na faixa do diálogo (`2.583`, `2.578`, `1.564`, `1.404` e `1.606` pixels). Capturas inspecionadas, legíveis e sem cortes.
- Três dicas anteriores (`0f35` de Kongo Jungle, `1074` de Monkey Mines e `1565` de Vine Valley) foram comparadas novamente com o original e com o build anterior: framebuffer, WRAM e áudio coincidiram byte a byte com a entrega anterior, com variação zero nos passos interpretados em relação ao piloto anterior.
- Menus e entrada da fase passaram nos quadros 1.700, 2.300 e 4.800. Na fase, imagem, áudio e WRAM coincidiram com a versão habitual.
- Um ciclo Candy/reinício coincidiu entre aplicativo, runner e disco em perfis de QA separados; SRAM igual ao fixture anterior. Nenhum save pessoal foi usado.
- Catálogo privado `catalog-draft-09.json` passou nas verificações de nomes e integridade: 50 registros preservados, 35 rascunhos históricos e 261 ainda sem tradução.
- ROM e executável habitual conservaram os hashes. Nenhuma nova instalação.

Revisão humana destas prévias, condições normais das falas, coleta dos segredos e campanha completa continuam pendentes.

## Reprodução

Fechar os processos de QA antes de recompilar.

```powershell
./scripts/build_rev1.ps1 -HeadlessOnly
./scripts/build_ptbr_pilot.ps1
python -m unittest discover -s tests -p 'test_ptbr*.py' -v
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/gorilla-hints-check --character cranky-tips --world gorilla-glacier --all-messages
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/gorilla-prior-regression --character cranky-tips --all-messages --message 0f35 --message 1074 --message 1565
python scripts/verify_ptbr_menu_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/gorilla-menu-check
python scripts/verify_rev1_saves.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/gorilla-save-check --build-dir build/ptbr-pilot --desktop-name DKC-Rev1-PTBR-Piloto.exe --repeats 1
```

Evidências privadas em `evidence/2026-11-07/pt-BR/gorilla-glacier/`: `verified-all/`, `prior-hints-regression/`, `menu-gameplay/`, `saves/`, `prior-patches-check.json`, `prior-hints-build-check.json`, `editorial-review.json`, `unit-tests.log` e logs de build. Os dados extraídos, capturas, dumps, saves e binários permanecem fora do GitHub público.

Próxima etapa: revisar as prévias de Gorilla Glacier e traduzir o grupo de Kremkroc Industries Inc. (`0x3C01B4–0x3C01C4`) na Rev 1.
