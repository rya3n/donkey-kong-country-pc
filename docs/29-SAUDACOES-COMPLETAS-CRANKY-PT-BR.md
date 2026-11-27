# Quarenta e uma saudações completas do Cranky em PT-BR

Entrega de 2026-11-07 no piloto separado USA v1.1 (Rev 1). Integradas as trinta e cinco saudações restantes do inventário do Cranky Kong (`0x3C07C0–0x3C0950` e `0x3C0A4D–0x3C0F0B`), totalizando 41 textos. São 31 saudações da tabela geral e dez textos que incluem referências individuais. A verificação posterior da seleção em jogo está registrada abaixo.

## Novas saudações traduzidas (35 registros)

Este quadro registra a redação de 2026-11-07. Em 2026-11-10, a fala de 0x3C0C2C passou a dizer “Terra de rinocerontes!”. Os ajustes de 2026-11-27 estão na seção de revisão em contexto. [Lote seguinte e correções](30-DIALOGOS-CRANKY-PT-BR.md)

| Endereço | Tamanho | Redação em PT-BR |
| --- | --- | --- |
| `0x3C07C0` | 50 B | Donkey, seu jovem / moleque travesso! / Quanto tempo! |
| `0x3C07F2` | 51 B | Meu rapaz Donkey! Faz / anos desde que nos falamos! |
| `0x3C0825` | 52 B | Já era hora de você visitar / seu frágil avozinho! |
| `0x3C0859` | 43 B | Ei! Pode arrumar / uma banana ao velhote? |
| `0x3C0884` | 47 B | E o que foi que você veio / trazer pro vovozinho? |
| `0x3C08B3` | 56 B | Olha, você espantou / seu velho avozinho / chegando até aqui! |
| `0x3C08EB` | 74 B | Enfim você resolveu vir / buscar conselhos de jogo / com o seu vovozinho! |
| `0x3C0950` | 64 B | Diddy, meu garotinho! / Olha, nem acredito / como você cresceu! |
| `0x3C0A4D` | 41 B | Ora, vejam! / Olhem só quem resolveu vir! |
| `0x3C0A76` | 58 B | Faz muito tempo que eu nem / vejo você por estas bandas! |
| `0x3C0AB0` | 43 B | Que é que você quer?! / Ando muito ocupado! |
| `0x3C0ADB` | 37 B | Ah! Até enfim! / Alguém pra conversar! |
| `0x3C0B00` | 51 B | Teve sorte de me encontrar, / eu já ia indo embora! |
| `0x3C0B33` | 49 B | Você trouxe de volta / as bananas que emprestei? |
| `0x3C0B64` | 46 B | Quando vi você antes / você ainda usava fraldas! |
| `0x3C0B92` | 45 B | Chegue mais perto, / deixe-me dar uma olhada! |
| `0x3C0BBF` | 30 B | Olhem só o que temos aqui! |
| `0x3C0BDD` | 34 B | Que bela surpresa, / ver você agora! |
| `0x3C0BFF` | 45 B | Um bando de Kremlings / acabou de passar! |
| `0x3C0C2C` | 27 B | Aqui é terra de chifrudos! |
| `0x3C0C47` | 54 B | Ei, garoto! Acredita no / barraco em que me meteram?! |
| `0x3C0C7D` | 36 B | Moleque! / Você já trouxe meu jornal?! |
| `0x3C0CA1` | 52 B | Eita gorila! / Deu para ouvir você vir / lá de bem longe! |
| `0x3C0CD5` | 59 B | Custa muito achar / paz e sossego hoje em dia / com você por cá! |
| `0x3C0D10` | 46 B | Claro, chegue mais! / Melhor que falar com o ar! |
| `0x3C0D3E` | 46 B | Ah! Faz eu lembrar do passado / ver você aqui! |
| `0x3C0D6C` | 78 B | Rapaz, tudo aqui andou cheio! / Com todo esse bando / de Kremlings, e agora você! |
| `0x3C0DBA` | 49 B | Bem parece que hoje / sou o Sr. Popular por aqui! |
| `0x3C0DEB` | 53 B | Melhor que visita / da Sra. Kong! / Como posso ajudar? |
| `0x3C0E20` | 40 B | Quem diria topar / com vocês por aqui! |
| `0x3C0E48` | 44 B | Hoje estou sem mais nada, / nem venha pedir! |
| `0x3C0E74` | 60 B | Dei meu barril final para o / seu belo amigo orangotango. |
| `0x3C0EB0` | 31 B | O que diabos você quer aqui? |
| `0x3C0ECF` | 60 B | Mais aproveitador? / Eu já fiquei sem nada, / vá logo embora! |
| `0x3C0F0B` | 42 B | Aposto que você / nem passa daqui mesmo... |

Os nomes próprios (`Donkey`, `Diddy`, `Donks`, `Funky Kong`, `Kremlings` e `Kong`) foram preservados e validados conforme `localization/pt-BR/policy.json`.

## Prévia e piloto

Galeria privada: `evidence/2026-11-07/pt-BR/cranky-greetings-complete/verified-all/preview.html`. As quarenta e uma capturas nativas mostram cada saudação em PT-BR na cabana do Cranky.

Abrir **Testar DKC - PT-BR.cmd** para jogar no perfil próprio do piloto. **Jogar DKC.cmd** continua abrindo o executável habitual, com seus saves separados.

## Integração

O arquivo `localization/pt-BR/cranky-pilot.json` reúne agora as 41 saudações (`group: "greetings"`) e as 11 falas de retorno rápido (`group: "revisits"`), totalizando 52 registros. A função `make_cranky_patch` valida a guarda completa da tabela de 32 ponteiros de saudação (`0x3C00C4–0x3C0104`), a tabela de retorno rápido (`0x3C0144–0x3C0164`), os 52 pares `(offset, bytes)`, grupos e nomes protegidos.

A fonte compartilhada e seus quatro glifos acentuados (`á`, `ê`, `ó`, `é`) foram reutilizados sem novos slots. O piloto aplica agora 109 regiões de dados à cópia da ROM em memória (`patchset_sha256` `d0953a1a3ec084e5c896a073daf19bb2c25d0a07f13f6952683530fd72a8caec`, binário `DKC-Rev1-PTBR-Piloto.exe` SHA-256 `d5fc3586429476520c42e337dff9ed26580bb65517cf085c4543df85aed99ee8`).

## Verificações

- Build Release e 52 testes Python passaram.
- As 41 saudações do Cranky passaram individualmente em `evidence/2026-11-07/pt-BR/cranky-greetings-complete/verified-all`: áudio completo e 128 KiB de WRAM inteiramente iguais ao original (`wram_changed_offsets: []`), com diferenças visuais restritas à faixa do diálogo (`y = 170..211`).
- Menus e entrada da fase passaram nos quadros 1.700, 2.300 e 4.800.
- Um ciclo Candy/reinício coincidiu entre aplicativo, runner e disco em perfis de QA separados (`evidence/2026-11-07/pt-BR/cranky-greetings-complete/saves`).
- Catálogo privado `catalog-draft-14.json` passou nas verificações de nomes e integridade: 50 registros preservados, 100 rascunhos históricos e 196 ainda sem tradução.

## Reprodução

```powershell
python -m unittest discover -s tests -p 'test_ptbr*.py' -v
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/cranky-greetings-check --character cranky --group greetings --all-messages
python scripts/verify_ptbr_menu_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/cranky-menu-check
python scripts/verify_rev1_saves.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/cranky-save-check --build-dir build/ptbr-pilot --desktop-name DKC-Rev1-PTBR-Piloto.exe --repeats 1
```

## Revisão em contexto na cabana

Em 2026-11-27, uma visita de Diddy sozinho reproduziu a saudação “Quem diria topar com vocês por aqui!”. A seleção normal da USA Rev 1 usa a mesma tabela geral para um Kong e para a dupla. A versão revisada diz “Quem diria receber visita por aqui!”. Outros quatro ajustes melhoraram a quebra da fala sobre Funky Kong, a lembrança das fraldas, a piada de falar sozinho e a referência ao barril que Cranky deu ao amigo orangotango. Os cinco registros mantiveram tamanhos, terminações e paridades.

A tabela inglesa de saudação em `0x3C00C4–0x3C0104` contém 32 ponteiros para 31 textos distintos, com `0x3C0D10` repetido. Os dez registros de `0x3C07A4` a `0x3C0950` ficam fora dessa tabela. O ensaio conferiu esses dez no comparador individual. O fluxo normal testado de entrada na cabana de Monkey Mines usou os outros 31, com seleção pelo próprio jogo e perfis de QA isolados.

Cada ensaio em contexto partiu de um estado no mapa com a cabana selecionada. A espera antes de pressionar B variou para percorrer as 31 variantes em cada uma das três composições. A leitura do mapa de tiles conferiu o texto e a distribuição das linhas nas 93 entradas. Depois da última fala amostrada em cada perfil, Start voltou ao mapa com Cranky's Cabin selecionada.

| Composição | Quadro de partida | Saudações distintas | Quadro de retorno ao mapa |
| --- | ---: | ---: | ---: |
| Diddy sozinho | 60.258 | 31 | 60.702 |
| Dupla | 61.487 | 31 | 62.012 |
| Donkey sozinho | 61.659 | 31 | 62.184 |

O estado com Diddy veio do [roteiro até Necky's Nuts](../recipes/usa-rev1/campaign-to-neckys-nuts-map.inputs), interrompido no quadro 60.258. Os estados da dupla e de Donkey vieram da recuperação natural do parceiro em Millstone Mayhem, conforme o [desvio das revisitas do Funky](28-FUNKY-FALAS-COMPLETAS.md#revisão-em-contexto-em-funkys-flights). Na dupla, a partir do quadro 61.114, o teste saiu da fase e seguiu à direita de Millstone Mayhem para a cabana. Após 172 quadros sem entrada no outro ensaio, Donkey ficou sozinho e seguiu pelo mesmo caminho.

O comparador individual registrou áudio digital e WRAM idênticos à base nos 41 pontos. As diferenças visuais ficaram na faixa do diálogo. A comparação dos manifestos confirmou que somente os cinco registros ajustados mudaram, com 237 regiões idênticas. Passaram os 68 testes Python e os três alvos do CTest de cada build. As evidências ficam em `evidence/2026-11-27/v16-cranky-greetings/`.
