# Dicas do Cranky para Kremkroc Industries Inc. em PT-BR

Entrega de 2026-11-07 no piloto separado USA v1.1 (Rev 1). Integrado o quarto grupo da tabela inglesa do Cranky (`0x3C01B4–0x3C01C4`), correspondente às cinco dicas de Kremkroc Industries Inc. O Cranky passa a ter seis saudações e vinte e duas dicas traduzidas: cinco de Kongo Jungle, quatro de Monkey Mines, três de Vine Valley, cinco de Gorilla Glacier e cinco de Kremkroc Industries Inc. Com Candy e Funky, são 40 mensagens no piloto; demais diálogos continuam em etapas próprias.

## Textos e pistas

| Fase | Redação em PT-BR | Pista mantida |
| --- | --- | --- |
| Elevator Antics | Em Elevator Antics, você deve subir mais alto que um ninho de vespas! | Subir pelas cordas acima do ninho de vespas (Zingers) no topo da caverna |
| Trick Track Trek | Em Trick Track Trek, os gêmeos Gnawty sabem de um segredo! | Referência aos dois castores Gnawty no fim do trilho que guardam o segredo |
| Mine Cart Madness | Em Mine Cart Madness, você está a 3 quiques da terra dos prêmios. | Quicar em três pneus seguidos no ar para alcançar a sala secreta |
| Poison Pond | Ao entrar em Poison Pond, ir pela direita nem sempre é o caminho certo pra ponta. | Duplo sentido entre direita/caminho certo no início da fase e a ponta do peixe-espada Enguarde |
| Blackout Basement | Blackout Basement pode fazer você achar que afunda, mas você termina lá no céu! | Cair no fosso/plataforma que cede e ser lançado para o alto por um barril oculto |

Os cinco nomes completos (Elevator Antics, Trick Track Trek, Mine Cart Madness, Poison Pond e Blackout Basement), além de Gnawty, foram preservados e protegidos pelo verificador em `localization/pt-BR/policy.json`.

## Prévia e piloto

Galeria privada: `evidence/2026-11-07/pt-BR/kremkroc-industries/verified-all/preview.html`. As cinco capturas nativas mostram o título de cada fase e a legenda em PT-BR. Elas documentam a seleção técnica no cenário do Cranky; não demonstram a coleta dos segredos nas fases.

Abrir **Testar DKC - PT-BR.cmd** para jogar no perfil próprio do piloto. O aplicativo mantém as condições originais de seleção das falas; **Jogar DKC.cmd** continua abrindo o executável habitual, com seus saves separados.

## Integração

O arquivo `localization/pt-BR/cranky-tips-pilot.json` reúne agora vinte e duas dicas com metadados de mundo (`kongo-jungle`, `monkey-mines`, `vine-valley`, `gorilla-glacier` e `kremkroc-industries`). A função `make_cranky_tips_patch` valida a guarda do grupo `0x3C01B4–0x3C01C4` (`12d4 1319 1355 1395 13e7 1355 1395 13e7`) e a associação entre endereço, tamanho, fase e mundo nos vinte e dois registros.

As mensagens em `0x3C12D4`, `0x3C1319`, `0x3C1355`, `0x3C1395` e `0x3C13E7` mantêm 69, 60, 64, 82 e 78 bytes, respectivamente, preservando ponteiros, três linhas por mensagem, terminadores e paridades (incluindo a terceira linha de 30 colunas originais em `0x3C1395`). A fonte compartilhada e seus quatro glifos acentuados (`á`, `ê`, `ó`, `é`) foram reutilizados sem novos slots ou alterações na tabela de tiles.

As 44 regiões anteriores mantêm exatamente o hash `7db4204137a0daaa27989d298f7c0ccd9f2f85850ec7a49e2ec554680d1b5849` ao serem recompostas sem as cinco regiões novas. O piloto aplica agora 49 regiões de dados à cópia da ROM em memória (`patchset_sha256` `532854194ec8cce504763c70165bb69bc10e0c9805a32843d092d08c54ed38e1`). O arquivo da ROM, código do cartucho, unidades AOT e relógio de 60,0988 Hz permanecem intactos.

O verificador `scripts/verify_ptbr_candy_pilot.py` aceita `--world kremkroc-industries` junto de `--character cranky-tips --all-messages`. O diagnóstico `DKC_REV1_QA_CRANKY_MESSAGE` continua exclusivo do runner sem janela.

## Verificações

- Build Release e 48 testes Python passaram, cobrindo os vinte e dois registros, nomes completos, Gnawty, associação de mundo e a guarda de ponteiros de Kremkroc Industries Inc.
- As cinco dicas passaram individualmente: áudio completo e 128 KiB de WRAM inteiramente iguais ao original (`interpreted_steps_delta` de -16, 0, 8, 0 e 0); diferenças de imagem apenas na faixa do diálogo (`1.460`, `2.059`, `1.065`, `2.268` e `1.603` pixels). Capturas inspecionadas, legíveis e sem cortes.
- Quatro dicas anteriores (`0f35` de Kongo Jungle, `1074` de Monkey Mines, `1565` de Vine Valley e `115b` de Gorilla Glacier) foram comparadas novamente com o original e com o build anterior: framebuffer, WRAM e áudio coincidiram byte a byte com a entrega anterior, com variação zero nos passos interpretados em relação ao piloto anterior.
- Menus e entrada da fase passaram nos quadros 1.700, 2.300 e 4.800. Na fase, imagem, áudio e WRAM coincidiram com a versão habitual.
- Um ciclo Candy/reinício coincidiu entre aplicativo, runner e disco em perfis de QA separados; SRAM igual ao fixture anterior. Nenhum save pessoal foi usado.
- Catálogo privado `catalog-draft-10.json` passou nas verificações de nomes e integridade: 50 registros preservados, 40 rascunhos históricos e 256 ainda sem tradução.
- ROM e executável habitual conservaram os hashes. Nenhuma nova instalação.

Revisão humana destas prévias, condições normais das falas, coleta dos segredos e campanha completa continuam pendentes.

## Reprodução

Fechar os processos de QA antes de recompilar.

```powershell
./scripts/build_rev1.ps1 -HeadlessOnly
./scripts/build_ptbr_pilot.ps1
python -m unittest discover -s tests -p 'test_ptbr*.py' -v
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/kremkroc-hints-check --character cranky-tips --world kremkroc-industries --all-messages
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/kremkroc-prior-regression --character cranky-tips --all-messages --message 0f35 --message 1074 --message 1565 --message 115b
python scripts/verify_ptbr_menu_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/kremkroc-menu-check
python scripts/verify_rev1_saves.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/kremkroc-save-check --build-dir build/ptbr-pilot --desktop-name DKC-Rev1-PTBR-Piloto.exe --repeats 1
```

Evidências privadas em `evidence/2026-11-07/pt-BR/kremkroc-industries/`: `verified-all/`, `prior-hints-regression/`, `menu-gameplay/`, `saves/`, `prior-patches-check.json`, `prior-hints-build-check.json`, `editorial-review.json`, `unit-tests.log` e logs de build. Os dados extraídos, capturas, dumps, saves e binários permanecem fora do GitHub público.

Próxima etapa: revisar as prévias de Kremkroc Industries Inc. e traduzir o último grupo de dicas de fases em Chimp Caverns (`0x3C01C4–0x3C01D4`) na Rev 1.
