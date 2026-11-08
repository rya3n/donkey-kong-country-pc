# Dicas do Cranky para Vine Valley em PT-BR

Entrega de 2026-11-07 no piloto separado USA v1.1 (Rev 1). Identificado o grupo de ponteiros de Vine Valley na tabela inglesa do Cranky e integradas suas três dicas. O Cranky passa a ter seis saudações e doze dicas traduzidas: cinco de Kongo Jungle, quatro de Monkey Mines e três de Vine Valley. Com Candy e Funky, são 30 mensagens no piloto; demais diálogos continuam em etapas próprias.

## Identificação do grupo na Rev 1

A tabela inglesa de dicas começa em `0x3C0184` com grupos de oito ponteiros de 16 bits. A ordem desses grupos na ROM não segue a ordem dos mundos na campanha:

- `0x3C0184–0x3C0194`: Kongo Jungle (5 dicas únicas)
- `0x3C0194–0x3C01A4`: Monkey Mines (4 dicas únicas)
- `0x3C01A4–0x3C01B4`: Gorilla Glacier (5 dicas únicas)
- `0x3C01B4–0x3C01C4`: Kremkroc Industries Inc. (5 dicas únicas)
- `0x3C01C4–0x3C01D4`: Chimp Caverns (5 dicas únicas)
- `0x3C01D4–0x3C01E4`: Vine Valley (`1565 15b3 15ef 1565 15b3 15ef 1565 15b3`, 3 dicas únicas repetidas)

Confirmado o sexto grupo inglês em `0x3C01D4–0x3C01E4` antes da tradução, evitando misturar pistas de Gorilla Glacier com Vine Valley.

## Textos e pistas

| Fase | Redação em PT-BR | Pista mantida |
| --- | --- | --- |
| Orang-utan Gang | Em Orang-utan Gang, siga o barril final abaixo para um barril de risadas! | Seguir o último barril para baixo e o jogo de palavras com o barril de bônus |
| Tree Top Town | Uma só banana basta para abrir o segredo de Tree Top Town. | A banana isolada como pista de entrada para o segredo da fase |
| Temple Tempest | Caia dentro com as bananas e se prepare pra festa em Temple Tempest! | Descer acompanhando as bananas e o tom de festa da recompensa |

Os três nomes completos (`Orang-utan Gang`, `Tree Top Town` e `Temple Tempest`) foram preservados com grafia e hífen originais e adicionados à proteção automática em `localization/pt-BR/policy.json`. Nenhuma dica extra foi inventada para fases de Vine Valley que não possuem entrada própria neste grupo da tabela.

## Prévia e piloto

Galeria privada: `evidence/2026-11-07/pt-BR/vine-valley/verified-all/preview.html`. As três capturas nativas têm títulos com os nomes das fases e legendas em PT-BR. Elas mostram a seleção técnica no cenário do Cranky; não demonstram a coleta dos segredos nas fases.

Abrir **Testar DKC - PT-BR.cmd** para jogar no perfil próprio do piloto. O aplicativo mantém as condições originais de seleção das falas; **Jogar DKC.cmd** continua abrindo o executável habitual, com seus saves separados.

## Integração

O arquivo `localization/pt-BR/cranky-tips-pilot.json` agora reúne doze dicas com metadados de mundo (`kongo-jungle`, `monkey-mines` e `vine-valley`). A função `make_cranky_tips_patch` valida a guarda do grupo `0x3C01D4–0x3C01E4` e a associação entre endereço, tamanho, fase e mundo nos doze registros.

As mensagens em `0x3C1565`, `0x3C15B3` e `0x3C15EF` mantêm 78, 60 e 69 bytes, respectivamente, preservando ponteiros, três linhas por mensagem, terminadores e paridades (incluindo a primeira linha de 30 colunas originais em `0x3C1565`). Somente espaços laterais completam os tamanhos originais; a fonte compartilhada e seus quatro glifos acentuados (`á`, `ê`, `ó`, `é`) foram reutilizados sem novos slots ou alterações na tabela de tiles.

As 36 regiões anteriores mantêm exatamente o hash `a230a43eec1b027c4995358ebf13edfc34381e2d485bef174e2b31b1867e48de` ao serem recompostas sem as três regiões novas. O piloto agora aplica 39 regiões de dados à cópia da ROM em memória (`patchset_sha256` `e80b1b28c2cf1dfeca399eb9043ebb77aea1e777638d5c410580759ac7635d10`). O arquivo da ROM, código do cartucho, unidades AOT e relógio de 60,0988 Hz permanecem intactos.

O verificador `scripts/verify_ptbr_candy_pilot.py` aceita `--world vine-valley` junto de `--character cranky-tips --all-messages`. O diagnóstico `DKC_REV1_QA_CRANKY_MESSAGE` continua exclusivo do runner sem janela.

## Verificações

- Build Release e 46 testes Python passaram, cobrindo os doze registros, nomes completos, associação de mundo e a guarda de ponteiros de Vine Valley.
- As três dicas passaram individualmente: áudio completo e 128 KiB de WRAM inteiramente iguais ao original (`interpreted_steps_delta` de 0, 0 e 0); diferenças de imagem apenas na faixa do diálogo. Capturas inspecionadas, legíveis e sem cortes.
- Três dicas anteriores (`0f35` de Kongo Jungle e `1074`/`1115` de Monkey Mines) foram comparadas novamente com o original e com o build anterior: framebuffer, WRAM e áudio coincidiram byte a byte com a entrega anterior, com variação zero nos passos interpretados em relação ao piloto anterior.
- Menus e entrada da fase passaram nos quadros 1.700, 2.300 e 4.800. Na fase, imagem, áudio e WRAM coincidiram com a versão habitual.
- Um ciclo Candy/reinício coincidiu entre aplicativo, runner e disco em perfis de QA separados; SRAM igual ao fixture anterior. Nenhum save pessoal foi usado.
- Catálogo privado `catalog-draft-08.json` passou nas verificações de nomes e integridade: 50 registros preservados, 30 rascunhos históricos e 266 ainda sem tradução.
- ROM e executável habitual conservaram os hashes. Nenhuma nova instalação.

Revisão humana destas três prévias, condições normais das falas, coleta dos segredos e campanha completa continuam pendentes.

## Reprodução

Fechar os processos de QA antes de recompilar.

```powershell
./scripts/build_rev1.ps1 -HeadlessOnly
./scripts/build_ptbr_pilot.ps1
python -m unittest discover -s tests -p 'test_ptbr*.py' -v
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/vine-hints-check --character cranky-tips --world vine-valley --all-messages
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/vine-prior-regression --character cranky-tips --all-messages --message 0f35 --message 1074 --message 1115
python scripts/verify_ptbr_menu_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/vine-menu-check
python scripts/verify_rev1_saves.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/vine-save-check --build-dir build/ptbr-pilot --desktop-name DKC-Rev1-PTBR-Piloto.exe --repeats 1
```

Evidências privadas em `evidence/2026-11-07/pt-BR/vine-valley/`: `verified-all/`, `prior-hints-regression/`, `menu-gameplay/`, `saves/`, `prior-patches-check.json`, `prior-hints-build-check.json`, `editorial-review.json`, `unit-tests.log` e logs de build. Os dados extraídos, capturas, dumps, saves e binários permanecem fora do GitHub público.

Etapa seguinte implementada: [Dicas de Gorilla Glacier](24-DICAS-GORILLA-GLACIER-PT-BR.md). O filtro `--world vine-valley` permite repetir somente este lote com o verificador atual. As três prévias de Vine Valley continuam com revisão humana pendente; campanha e coleta dos segredos permanecem na matriz de validação.
