# Treze falas do Funky Kong em PT-BR

Entrega de 2026-11-07 no piloto separado USA v1.1 (Rev 1). Integradas as nove mensagens inglesas de revisita do Funky Kong (`0x3C0374–0x3C038C`, de `0x3C3334` a `0x3C3575`), concluindo todas as treze falas identificadas do personagem: quatro de abertura (`opening`) e nove de revisita (`revisits`, incluindo cinco com a dupla completa e quatro quando apenas Donkey ou Diddy visita o local). Com Candy (8), Funky (13) e Cranky (44), são 65 mensagens traduzidas no piloto.

## Textos de revisita traduzidos

| Endereço | Tamanho | Redação em PT-BR |
| --- | --- | --- |
| `0x3C3334` | 74 B | Boa, Kongs irados! Se / vocês querem velocidade, / pulem dentro e voem! |
| `0x3C337E` | 76 B | Precisam de umas vidas, / galera? Jungle Hijinxs é / o lugar certo pra isso! |
| `0x3C33CA` | 55 B | Opa, gorilas! / Visitem o velho Cranky, / ele pode ajudar! |
| `0x3C3401` | 63 B | Mandando bem, Kongs! / Apertem o cinto e decolem, / vocês já foram! |
| `0x3C3440` | 85 B | Se virem a Candy pelo / caminho, digam que dou aula / de surfe pra ela quando der! |
| `0x3C3495` | 68 B | Topa um voo, amigo DK? / Você sabe como é, / pule logo e mande ver! |
| `0x3C34D9` | 85 B | Opa, cara Donkey! Talvez seu / amiguinho do surfe esteja em / outra fase. Vá conferir lá! |
| `0x3C352E` | 71 B | Fala, Diddy! Perdeu o / parceiro de novo? Decole / de volta e confira tudo! |
| `0x3C3575` | 85 B | Ainda falando sozinho, cara? / Dê uma olhada na selva, logo / você acha o seu parceiro! |

Os nomes próprios (`Kongs`, `Jungle Hijinxs`, `Cranky`, `Candy`, `DK`, `Donkey` e `Diddy`) além de `Funky Kong` e `Jumbo Barrel` das falas de abertura foram preservados e protegidos em `localization/pt-BR/policy.json`.

## Prévia e piloto

Galeria privada: `evidence/2026-11-07/pt-BR/funky-complete/verified-all/preview.html`. As nove capturas nativas mostram a legenda em PT-BR em Funky's Flights. Elas documentam a seleção técnica no cenário do Funky; não reproduzem a ausência de um parceiro em cena.

Abrir **Testar DKC - PT-BR.cmd** para jogar no perfil próprio do piloto. O aplicativo mantém as condições originais de seleção das falas; **Jogar DKC.cmd** continua abrindo o executável habitual, com seus saves separados.

## Integração

O arquivo `localization/pt-BR/funky-pilot.json` reúne todas as treze mensagens do Funky separadas por `group` (`opening` e `revisits`). A função `make_funky_patch` valida a guarda completa `0x3C036C–0x3C038C` (`74 30 96 30 d9 30 25 31 34 33 7e 33 ca 33 01 34 40 34 34 33 7e 33 ca 33 95 34 d9 34 2e 35 75 35`), tamanhos, grupos e nomes protegidos, marcando `complete_funky_translation: true`.

As nove mensagens de `0x3C3334` a `0x3C3575` mantêm seus tamanhos originais (74, 76, 55, 63, 85, 68, 85, 71 e 85 bytes), três linhas cada, terminadores e paridades. A fonte compartilhada e seus quatro glifos acentuados (`á`, `ê`, `ó`, `é`) foram reutilizados sem novos slots.

As 65 regiões anteriores mantêm exatamente o hash `b8d0222530870791ff08c470424ce909c3097de8e24cedf38cbdf0c91e3d223e` ao serem recompostas sem as nove regiões novas. O piloto aplica agora 74 regiões de dados à cópia da ROM em memória (`patchset_sha256` `4501931debd72b9e5a4c58215853ab81df48b20bd04b24219ad02faac370d9d9`). O arquivo da ROM, código do cartucho, unidades AOT e relógio de 60,0988 Hz permanecem intactos.

## Verificações

- Build Release e 52 testes Python passaram, cobrindo os treze registros do Funky, grupos, nomes protegidos e guardas de ponteiros.
- As nove falas de revisita passaram individualmente: áudio completo e 128 KiB de WRAM inteiramente iguais ao original (`interpreted_steps_delta` de `-8, 8, 0, -8, 0, 0, -8, 8, 0`); diferenças de imagem apenas na faixa do diálogo (`2.228`, `2.289`, `1.339`, `1.624`, `2.522`, `2.092`, `2.358`, `2.247` e `2.734` pixels). Capturas inspecionadas, legíveis e sem cortes.
- Duas falas de abertura (`3074` e `3096`) foram comparadas novamente com o original: áudio completo e 128 KiB de WRAM inteiramente iguais ao original.
- Menus e entrada da fase passaram nos quadros 1.700, 2.300 e 4.800. Na fase, imagem, áudio e WRAM coincidiram com a versão habitual.
- Um ciclo Candy/reinício coincidiu entre aplicativo, runner e disco em perfis de QA separados; SRAM igual ao fixture anterior. Nenhum save pessoal foi usado.
- Catálogo privado `catalog-draft-13.json` passou nas verificações de nomes e integridade: 50 registros preservados, 65 rascunhos históricos e 231 ainda sem tradução.
- ROM e executável habitual conservaram os hashes. Nenhuma nova instalação.

## Reprodução

Fechar os processos de QA antes de recompilar.

```powershell
./scripts/build_rev1.ps1 -HeadlessOnly
./scripts/build_ptbr_pilot.ps1
python -m unittest discover -s tests -p 'test_ptbr*.py' -v
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/funky-revisits-check --character funky --group revisits --all-messages
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/funky-opening-regression --character funky --group opening --all-messages --message 3074 --message 3096
python scripts/verify_ptbr_menu_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/funky-menu-check
python scripts/verify_rev1_saves.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/funky-save-check --build-dir build/ptbr-pilot --desktop-name DKC-Rev1-PTBR-Piloto.exe --repeats 1
```

Evidências privadas em `evidence/2026-11-07/pt-BR/funky-complete/`: `verified-all/`, `prior-opening-regression/`, `menu-gameplay/`, `saves/`, `prior-patches-check.json`, `editorial-review.json`, `unit-tests.log` e logs de build. Os dados extraídos, capturas, dumps, saves e binários permanecem fora do GitHub público.

Próxima etapa: completar as saudações do Cranky (`0x3C07A4–0x3C0F0B`) em `P31`.
