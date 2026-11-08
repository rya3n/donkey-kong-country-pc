# Dicas do Cranky para Chimp Caverns em PT-BR

Entrega de 2026-11-07 no piloto separado USA v1.1 (Rev 1). Integrado o quinto grupo da tabela inglesa do Cranky (`0x3C01C4–0x3C01D4`), correspondente às cinco dicas de Chimp Caverns, concluindo todas as 27 dicas únicas de fases nos seis mundos da tabela `0x3C0184–0x3C01E4`. O Cranky passa a ter seis saudações e vinte e sete dicas traduzidas: cinco de Kongo Jungle, quatro de Monkey Mines, três de Vine Valley, cinco de Gorilla Glacier, cinco de Kremkroc Industries Inc. e cinco de Chimp Caverns. Com Candy e Funky, são 45 mensagens no piloto; demais tabelas do Cranky continuam em etapas próprias.

## Textos e pistas

| Fase | Redação em PT-BR | Pista mantida |
| --- | --- | --- |
| Manic Mincers | Deixe Diddy segurar o TNT em Manic Mincers. | Diddy segura o barril de TNT à frente do corpo para abrir a parede do bônus |
| Misty Mine | Use bastante corda e você se surpreenderá lá em Misty Mine. | Descer até o fim da longa corda no fosso para encontrar a entrada secreta |
| Loopy Lights | Em Loopy Lights, o barril do abutre joga você longe. | Saltar no abutre (Necky) próximo ao barril para alcançar a sala de bônus |
| Platform Perils | O abutre de Platform Perils sabe que por vezes é melhor descer para a terra. | Quicar no abutre ou descer com a plataforma para achar o barril oculto abaixo |
| Tanked Up Trouble | Você terá Tanked Up Trouble se tiver o tanque cheio e sem ter aonde ir! | Trocadilho com o combustível da plataforma sobre trilhos e o fim do percurso |

Os cinco nomes completos (Manic Mincers, Misty Mine, Loopy Lights, Platform Perils e Tanked Up Trouble), além de Diddy e TNT, foram preservados e protegidos pelo verificador em `localization/pt-BR/policy.json`.

## Prévia e piloto

Galeria privada: `evidence/2026-11-07/pt-BR/chimp-caverns/verified-all/preview.html`. As cinco capturas nativas mostram o título de cada fase e a legenda em PT-BR. Elas documentam a seleção técnica no cenário do Cranky; não demonstram a coleta dos segredos nas fases.

Abrir **Testar DKC - PT-BR.cmd** para jogar no perfil próprio do piloto. O aplicativo mantém as condições originais de seleção das falas; **Jogar DKC.cmd** continua abrindo o executável habitual, com seus saves separados.

## Integração

O arquivo `localization/pt-BR/cranky-tips-pilot.json` reúne agora todas as vinte e sete dicas de fases com metadados dos seis mundos (`kongo-jungle`, `monkey-mines`, `vine-valley`, `gorilla-glacier`, `kremkroc-industries` e `chimp-caverns`). A função `make_cranky_tips_patch` valida a guarda do grupo `0x3C01C4–0x3C01D4` (`1435 1461 149d 14d2 151f 1461 149d 14d2`) e a associação entre endereço, tamanho, fase e mundo nos vinte e sete registros.

As mensagens em `0x3C1435`, `0x3C1461`, `0x3C149D`, `0x3C14D2` e `0x3C151F` mantêm 44, 60, 53, 77 e 70 bytes, respectivamente, preservando ponteiros, quantidades originais de linhas (duas linhas em `0x3C1435` e `0x3C149D`; três nas demais), terminadores e paridades. A fonte compartilhada e seus quatro glifos acentuados (`á`, `ê`, `ó`, `é`) foram reutilizados sem novos slots ou alterações na tabela de tiles.

As 49 regiões anteriores mantêm exatamente o hash `532854194ec8cce504763c70165bb69bc10e0c9805a32843d092d08c54ed38e1` ao serem recompostas sem as cinco regiões novas. O piloto aplica agora 54 regiões de dados à cópia da ROM em memória (`patchset_sha256` `f0a3f4f77cdd06619eaae1a3a54445fda2c983f31f19622df60c84bc701e0227`). O arquivo da ROM, código do cartucho, unidades AOT e relógio de 60,0988 Hz permanecem intactos.

O verificador `scripts/verify_ptbr_candy_pilot.py` aceita `--world chimp-caverns` junto de `--character cranky-tips --all-messages`. O diagnóstico `DKC_REV1_QA_CRANKY_MESSAGE` continua exclusivo do runner sem janela.

## Verificações

- Build Release e 49 testes Python passaram, cobrindo os vinte e sete registros, nomes completos, Diddy, TNT, associação de mundo e as seis guardas de ponteiros da tabela de dicas de fases.
- As cinco dicas passaram individualmente: áudio completo e 128 KiB de WRAM inteiramente iguais ao original (`interpreted_steps_delta` de 0, 0, 8, 0 e -8); diferenças de imagem apenas na faixa do diálogo (`895`, `1.716`, `1.525`, `2.071` e `1.438` pixels). Capturas inspecionadas, legíveis e sem cortes.
- Cinco dicas anteriores (`0f35` de Kongo Jungle, `1074` de Monkey Mines, `1565` de Vine Valley, `115b` de Gorilla Glacier e `12d4` de Kremkroc Industries Inc.) foram comparadas novamente com o original e com o build anterior: framebuffer, WRAM e áudio coincidiram byte a byte com a entrega anterior, com variação zero nos passos interpretados em relação ao piloto anterior.
- Menus e entrada da fase passaram nos quadros 1.700, 2.300 e 4.800. Na fase, imagem, áudio e WRAM coincidiram com a versão habitual.
- Um ciclo Candy/reinício coincidiu entre aplicativo, runner e disco em perfis de QA separados; SRAM igual ao fixture anterior. Nenhum save pessoal foi usado.
- Catálogo privado `catalog-draft-11.json` passou nas verificações de nomes e integridade: 50 registros preservados, 45 rascunhos históricos e 251 ainda sem tradução.
- ROM e executável habitual conservaram os hashes. Nenhuma nova instalação.

Revisão humana destas prévias, condições normais das falas, coleta dos segredos e campanha completa continuam pendentes.

## Reprodução

Fechar os processos de QA antes de recompilar.

```powershell
./scripts/build_rev1.ps1 -HeadlessOnly
./scripts/build_ptbr_pilot.ps1
python -m unittest discover -s tests -p 'test_ptbr*.py' -v
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/chimp-hints-check --character cranky-tips --world chimp-caverns --all-messages
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/chimp-prior-regression --character cranky-tips --all-messages --message 0f35 --message 1074 --message 1565 --message 115b --message 12d4
python scripts/verify_ptbr_menu_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/chimp-menu-check
python scripts/verify_rev1_saves.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/chimp-save-check --build-dir build/ptbr-pilot --desktop-name DKC-Rev1-PTBR-Piloto.exe --repeats 1
```

Evidências privadas em `evidence/2026-11-07/pt-BR/chimp-caverns/`: `verified-all/`, `prior-hints-regression/`, `menu-gameplay/`, `saves/`, `prior-patches-check.json`, `prior-hints-build-check.json`, `editorial-review.json`, `unit-tests.log` e logs de build. Os dados extraídos, capturas, dumps, saves e binários permanecem fora do GitHub público.

Próxima etapa: revisar as prévias dos seis mundos de dicas do Cranky e avaliar os lotes restantes de diálogos gerais do Cranky (`P11`) ou a validação de campanha (`P10`).
