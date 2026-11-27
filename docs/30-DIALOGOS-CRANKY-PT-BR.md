# Inventário de diálogos do Cranky em PT-BR

Em 2026-11-10, o piloto passou a incluir as 117 falas restantes do Cranky preparadas no lote anterior. A configuração reúne 196 mensagens do personagem e 217 diálogos no total para USA Rev 1. Esse total corresponde ao bloco inglês de diálogos identificado no inventário.

| Grupo integrado | Falas |
| --- | ---: |
| Finais | 16 |
| Dicas gerais | 32 |
| Despedidas | 32 |
| Reclamações | 37 |

O lote anterior já tinha oito falas da Candy, treze do Funky e 79 do Cranky. As 79 do Cranky incluem 41 saudações, onze retornos rápidos e 27 dicas de fases. A entrada 0x3C0C2C voltou a mencionar rinocerontes com “Terra de rinocerontes!”. A dica de corrida em 0x3C1796 indica X, a tecla padrão do port para correr e rolar.

## Como abrir e revisar

Abra **Testar DKC - PT-BR.cmd**. O índice privado evidence/2026-11-10/pt-BR/cranky-complete/preview.html abre as galerias de finais, dicas gerais, despedidas, reclamações e da saudação corrigida da entrega de 2026-11-10. A seleção técnica ocorre na cabana do Cranky no quadro 4.350. As revisões em jogo desses quatro grupos estão registradas abaixo.

## Verificações

- O build Release e os 52 testes Python passaram.
- Nas 118 comparações, o áudio completo e os 128 KiB de WRAM coincidiram com o original. As diferenças de imagem ficaram na faixa de diálogo. As duas correções e amostras das linhas mais longas foram inspecionadas nas capturas.
- Os menus e a entrada de Jungle Hijinxs passaram nos quadros 1.700, 2.300 e 4.800. O ciclo de salvar na Candy e reabrir passou com perfis de teste separados.
- O catálogo privado draft-16 passou na verificação de nomes e do inventário. O conjunto de IDs da configuração coincide com os 217 registros ingleses de diálogo.
- A comparação das 109 regiões do piloto anterior identificou uma alteração, a saudação dos rinocerontes. As 117 falas integradas elevam o total para 226 regiões de dados em memória.
- O executável do piloto tem SHA-256 `537f4be9984d154d546819cbde14b69b939e994c156e0bf7ce7e611cc3042c83`. O conjunto de dados aplicado tem SHA-256 `1032422cde60b0e6e7bed624c5a2b35068e8fbbab65e51546f7572b4e338369e`.

## Reprodução

```powershell
./scripts/build_rev1.ps1 -HeadlessOnly
./scripts/build_ptbr_pilot.ps1
python -m unittest discover -s tests -p 'test_ptbr*.py' -v
foreach ($group in @('endings', 'general_tips', 'farewells', 'rants')) {
    python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out "evidence/cranky-check-$group" --character cranky --group $group --all-messages
    if ($LASTEXITCODE -ne 0) { throw "Falha na comparação de $group" }
}
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/cranky-rhino-check --character cranky --group greetings --all-messages --message 0c2c
python scripts/verify_ptbr_menu_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/cranky-menu-check
python scripts/verify_rev1_saves.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/cranky-save-check --build-dir build/ptbr-pilot --desktop-name DKC-Rev1-PTBR-Piloto.exe --repeats 1
```

O gerador verifica os ponteiros, os limites dos registros e os nomes protegidos antes de montar a tradução em memória. O verificador seleciona os endereços autorizados no comparador sem janela e usa o mesmo endereço nas execuções em inglês e PT-BR.

## Dicas gerais em contexto na cabana

Em 2026-11-27, foram ajustadas dez redações. A dica do superpulo especifica rolar para fora da plataforma e apertar o botão de pulo no ar. A do tonel de metal explica como subir nele quando volta da parede. As dicas sobre correr para saltar mais longe, ganhar impulso ao pular em inimigos e usar pneus fixos também ficaram mais claras. A instrução existente para correr com X continua de acordo com o [mapeamento padrão do teclado](11-TESTE-INTERATIVO.md#abrir-e-jogar).

A tabela inglesa de dicas gerais em `0x3C0244–0x3C0284` tem 32 ponteiros para 31 registros distintos, com `0x3C1ED0` repetido. A dica de Gnawty em `0x3C1F0F` fica fora dessa tabela e foi conferida no comparador individual.

A partir dos [estados isolados no mapa de Monkey Mines](29-SAUDACOES-COMPLETAS-CRANKY-PT-BR.md#revisão-em-contexto-na-cabana), o jogo escolheu as 31 dicas com Diddy sozinho. Três amostras também passaram com Donkey e três com a dupla em uma revisita. Após a saudação ou a fala de retorno, B abriu uma dica de fase. O segundo B mostrou a dica geral. A leitura das linhas renderizadas confirmou o catálogo em todas as 37 entradas. Os três perfis passaram pela despedida e voltaram ao mapa com Cranky's Cabin selecionada.

Os 32 registros passaram individualmente com áudio digital e WRAM idênticos à versão base. As diferenças visuais ficaram na faixa do diálogo. A comparação dos manifestos confirmou dez alterações no texto e outras 232 regiões idênticas. Passaram os 68 testes Python e os três alvos do CTest de cada compilação. A validação conferiu o texto e a sequência da cabana. As evidências ficam em `evidence/2026-11-27/v16-cranky-tips/`.

## Despedidas em contexto na cabana

Em 2026-11-27, foram ajustadas 11 redações. Frases como “Foi bom bater um papo!” servem para a dupla e para um Kong sozinho, pois a Rev 1 sorteia a despedida na mesma tabela. A piada da gravata preserva o nome Donkey. A despedida do jacaré ficou mais curta e manteve a brincadeira.

A tabela de despedidas em `0x3C02C4–0x3C0304` tem 32 ponteiros para 31 textos, com `0x3C255C` repetido. A fala sobre tirar uma soneca na cabana, no endereço `0x3C23A2`, fica fora dessa tabela e foi conferida individualmente.

O teste começou nos [estados isolados no mapa de Monkey Mines](29-SAUDACOES-COMPLETAS-CRANKY-PT-BR.md#revisão-em-contexto-na-cabana). Depois da saudação ou da fala de retorno, três toques em B passaram pela dica de fase, pela dica geral e pela despedida. O jogo selecionou as 31 variantes com Diddy sozinho. A revisão também conferiu três despedidas com Donkey e quatro com a dupla, num total de 38 entradas. A saída automática ao fim da fala passou com Diddy e com a dupla. A saída com Start passou com Donkey. Nos três perfis, Cranky's Cabin voltou a ficar selecionada no mapa.

O comparador individual conferiu os 32 textos com áudio digital e WRAM idênticos à versão base. As diferenças visuais ficaram na faixa do diálogo. O manifesto mostrou 11 regiões de texto alteradas e outras 231 idênticas. Passaram os 68 testes Python e os três alvos do CTest em cada compilação. As evidências ficam em `evidence/2026-11-27/v16-cranky-farewells/`.

## Reclamações em contexto na cabana

Em 2026-11-27, foram ajustadas 15 redações. As falas recuperam o contraste entre tons de cinza e cores, a brincadeira com os quadros de animação da barba e a queixa sobre a dificuldade dos jogos antigos. O nome Game & Watch foi preservado.

A tabela em `0x3C0030–0x3C007A` tem 37 ponteiros distintos. A entrada na cabana sorteia a primeira de seis reclamações consecutivas. Elas aparecem depois da saudação ou da fala de retorno, com avanço automático a cada 384 quadros. B durante esse trecho passa para a dica de fase.

O ensaio parte de [estados isolados no mapa de Monkey Mines](29-SAUDACOES-COMPLETAS-CRANKY-PT-BR.md#revisão-em-contexto-na-cabana), com Cranky's Cabin selecionada. Para repetir a seleção com Diddy sozinho, restaure o estado do quadro 60.258 antes de cada visita, espere 71, 40, 61, 22, 0, 36 ou 29 quadros, conforme a visita, e entre com B. Esses tempos correspondem aos índices iniciais 0, 6, 12, 18, 24, 30 e 31. Aguarde as seis reclamações em cada visita.

As sete visitas de Diddy exibiram as 37 reclamações distintas em 42 exibições. A última passou automaticamente para a dica de fase no quadro 63.124. Donkey sozinho e a dupla em revisita exibiram duas falas cada, com avanço automático entre as falas e B para abrir a dica de fase. Start levou os três perfis de volta ao mapa com Cranky's Cabin selecionada (`0x00EF`).

O comparador individual conferiu as 37 falas no quadro 4.350, com áudio digital e WRAM idênticos à versão base. As diferenças visuais ficaram na faixa do diálogo. O manifesto confirmou 15 regiões de texto alteradas e outras 227 idênticas. Passaram os 68 testes Python e os três alvos do CTest em cada compilação. As capturas e os resultados em JSON ficam em `evidence/2026-11-27/v16-cranky-rants/`.

## Falas do encerramento em contexto

Em 2026-11-27, foram ajustadas 15 das 16 falas finais. A fala sobre a surpresa cita o depósito de bananas, e a provocação sobre os segredos distingue o final comum do final de 101%. Os nomes Donkey, Kremlings, Red Team e Yellow Team foram preservados.

A tabela em `0x3C03A8–0x3C03C7` tem 16 ponteiros distintos. O trecho inicial depende do modo de jogo. No competitivo, o Cranky usa a equipe ativa e se a outra equipe já terminou. Em seguida vem a fala sobre o depósito e o comentário sobre o progresso. A 101%, o jogo escolhe as duas falas que reconhecem a descoberta de todos os segredos.

O teste em Windows sem janela partiu de estados isolados do [roteiro de Gang-Plank Galleon](32-CAMPANHA-PT-BR-AUDIO-E-PROGRESSO.md#gang-plank-galleon-e-final-da-campanha), entre o décimo golpe e a cena da banana gigante. A rota de um jogador preservou o estado de 34% da campanha. Os outros seis cenários partiram de cópias preparadas para QA com o modo, o progresso de 101% ou o resultado da outra equipe ajustados antes da cena. A seleção das falas e o avanço automático de 384 quadros foram executados pelo jogo.

| Cenário | Falas exibidas |
| --- | ---: |
| Um jogador, 34% | 5 |
| Dupla cooperativa, 34% | 5 |
| Um jogador, 101% | 5 |
| Red Team em primeiro | 6 |
| Yellow Team em primeiro | 6 |
| Red Team em segundo | 5 |
| Yellow Team em segundo | 5 |

As 37 exibições cobriram as 16 falas distintas. Todos os cenários avançaram ao depósito recuperado (`0x004C`). No trecho de campanha sem ajustes no estado, o roteiro passou pelo depósito no quadro 234.194, pelo elenco no 235.094 e pelos créditos reais no 245.894. O jogo voltou à tela de título no quadro 254.444, com `entrance=0x0000` e `scene=0x0001`.

Os 16 textos distintos passaram na comparação individual com a versão base. O áudio digital e a WRAM coincidiram. As diferenças de imagem ficaram na faixa do diálogo. O manifesto confirmou 15 regiões de texto alteradas e outras 227 idênticas. Passaram os 68 testes Python e os três alvos do CTest em cada compilação. As capturas e os resultados ficam em `evidence/2026-11-27/v16-cranky-endings/`.
