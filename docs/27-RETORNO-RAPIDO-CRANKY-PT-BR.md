# Falas de retorno rápido do Cranky em PT-BR

Entrega de 2026-11-07 no piloto separado USA v1.1 (Rev 1). Integrada toda a tabela inglesa de retorno rápido do Cranky (`0x3C0144–0x3C0164`, 16 ponteiros cobrindo 11 mensagens únicas de `0x3C2E3B` a `0x3C301E`), usada quando o jogador volta à cabana em curto intervalo ou após falhar numa fase. O Cranky passa a ter seis saudações, onze falas de retorno rápido e todas as vinte e sete dicas de fases dos seis mundos traduzidas (44 mensagens do Cranky). Com Candy e Funky, são 56 mensagens no piloto; demais tabelas gerais do Cranky continuam em etapas próprias.

## Textos traduzidos

| Endereço | Tamanho | Redação em PT-BR |
| --- | --- | --- |
| `0x3C2E3B` | 70 B | Voltou aqui de novo?! / Eu sabia que um pirralho / como você ia falhar... |
| `0x3C2E81` | 85 B | Que rápido! Você nem mesmo / me deu tempo suficiente para / pensar em mais piadas bobas! |
| `0x3C2ED6` | 70 B | Nem sei por que / digo tudo isso pra você, / você nem ouviu da outra vez! |
| `0x3C2F1C` | 32 B | Você tem de / ir melhor que isso! |
| `0x3C2F3C` | 20 B | Você acabou de ir! |
| `0x3C2F50` | 30 B | Já voltou?! Isso foi rápido! |
| `0x3C2F6E` | 47 B | Voltou ao grande mestre / atrás de mais dicas, é? |
| `0x3C2F9D` | 27 B | Ainda apanhando feio, é?! |
| `0x3C2FB8` | 47 B | Pois é! Nem fazem jogadores / como antigamente! |
| `0x3C2FE7` | 55 B | Bom, / eu passo a fase para você!... / Nada, só brincando! |
| `0x3C301E` | 86 B | Como é que você se atreve / a mostrar a cara aqui de novo / após um desempenho lamentável! |

O tom ranzinza e sarcástico original foi preservado em todas as onze mensagens.

## Prévia e piloto

Galeria privada: `evidence/2026-11-07/pt-BR/cranky-revisits/verified-all/preview.html`. As onze capturas nativas mostram a legenda em PT-BR na cabana do Cranky. Elas documentam a seleção técnica no cenário do Cranky; não substituem a condição normal de retorno rápido em gameplay.

Abrir **Testar DKC - PT-BR.cmd** para jogar no perfil próprio do piloto. O aplicativo mantém as condições originais de seleção das falas; **Jogar DKC.cmd** continua abrindo o executável habitual, com seus saves separados.

## Integração

O arquivo `localization/pt-BR/cranky-pilot.json` reúne agora dezessete mensagens gerais do Cranky separadas pelo campo `group`: seis saudações iniciais (`greetings`) e onze falas de retorno rápido (`revisits`). A função `make_cranky_patch` valida a guarda completa da tabela `0x3C0144–0x3C0164` (`2e3b 2e81 2ed6 2f1c 2f3c 2f50 2f6e 2f9d 2fb8 2fe7 301e 2ed6 2f1c 2f3c 2f50 2f6e`) além das guardas de idioma e saudações.

As onze mensagens de `0x3C2E3B` a `0x3C301E` mantêm exatamente seus comprimentos originais em bytes (70, 85, 70, 32, 20, 30, 47, 27, 47, 55 e 86 bytes), preservando ponteiros, quantidades originais de linhas (uma linha em `0x3C2F3C`, `0x3C2F50` e `0x3C2F9D`; duas em `0x3C2F1C`, `0x3C2F6E` e `0x3C2FB8`; três nas demais), terminadores e paridades. Na mensagem `0x3C301E`, cujo original em inglês já usa linha de 31 colunas (`after such a pitiful showing?`), o limite individual `max_line: 31` foi declarado e validado sem corte visual. A fonte compartilhada e seus quatro glifos acentuados (`á`, `ê`, `ó`, `é`) foram reutilizados sem novos slots.

As 54 regiões anteriores mantêm exatamente o hash `f0a3f4f77cdd06619eaae1a3a54445fda2c983f31f19622df60c84bc701e0227` ao serem recompostas sem as onze regiões novas. O piloto aplica agora 65 regiões de dados à cópia da ROM em memória (`patchset_sha256` `b8d0222530870791ff08c470424ce909c3097de8e24cedf38cbdf0c91e3d223e`). O arquivo da ROM, código do cartucho, unidades AOT e relógio de 60,0988 Hz permanecem intactos.

O verificador `scripts/verify_ptbr_candy_pilot.py` aceita `--group greetings` ou `--group revisits` junto de `--character cranky --all-messages`. O diagnóstico `DKC_REV1_QA_CRANKY_MESSAGE` continua exclusivo do runner sem janela.

## Verificações

- Build Release e 51 testes Python passaram, cobrindo os dezessete registros de `cranky-pilot.json`, os vinte e sete registros de `cranky-tips-pilot.json`, grupos e guardas de ponteiros.
- As onze falas de retorno rápido passaram individualmente: áudio completo e 128 KiB de WRAM inteiramente iguais ao original (`interpreted_steps_delta` de 0 nas dez primeiras e +8 em `0x3C301E`); diferenças de imagem apenas na faixa do diálogo (`1.946`, `2.411`, `2.066`, `675`, `568`, `1.006`, `1.158`, `812`, `1.360`, `1.472` e `2.534` pixels). Capturas inspecionadas, legíveis e sem cortes.
- Duas saudações anteriores (`07a4` e `0a14`) foram comparadas novamente com o original: áudio completo e 128 KiB de WRAM inteiramente iguais ao original, com delta zero nos passos interpretados.
- Menus e entrada da fase passaram nos quadros 1.700, 2.300 e 4.800. Na fase, imagem, áudio e WRAM coincidiram com a versão habitual.
- Um ciclo Candy/reinício coincidiu entre aplicativo, runner e disco em perfis de QA separados; SRAM igual ao fixture anterior. Nenhum save pessoal foi usado.
- Catálogo privado `catalog-draft-12.json` passou nas verificações de nomes e integridade: 50 registros preservados, 56 rascunhos históricos e 240 ainda sem tradução.
- ROM e executável habitual conservaram os hashes. Nenhuma nova instalação.

Revisão humana destas prévias, condições normais das falas e campanha completa continuam pendentes.

## Reprodução

Fechar os processos de QA antes de recompilar.

```powershell
./scripts/build_rev1.ps1 -HeadlessOnly
./scripts/build_ptbr_pilot.ps1
python -m unittest discover -s tests -p 'test_ptbr*.py' -v
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/revisits-check --character cranky --group revisits --all-messages
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/greetings-regression --character cranky --group greetings --all-messages --message 07a4 --message 0a14
python scripts/verify_ptbr_menu_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/revisits-menu-check
python scripts/verify_rev1_saves.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/revisits-save-check --build-dir build/ptbr-pilot --desktop-name DKC-Rev1-PTBR-Piloto.exe --repeats 1
```

Evidências privadas em `evidence/2026-11-07/pt-BR/cranky-revisits/`: `verified-all/`, `prior-greetings-regression/`, `menu-gameplay/`, `saves/`, `prior-patches-check.json`, `editorial-review.json`, `unit-tests.log` e logs de build. Os dados extraídos, capturas, dumps, saves e binários permanecem fora do GitHub público.

Próxima etapa: revisar as prévias de retorno rápido do Cranky e avaliar os lotes restantes de saudações, aberturas, dicas gerais e despedidas do Cranky (`P11`).
