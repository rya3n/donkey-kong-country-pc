# Inventário de diálogos do Cranky em PT-BR

Em 2026-11-10, o piloto passou a incluir as 117 falas restantes do Cranky preparadas no lote anterior. A configuração reúne 196 mensagens do personagem e 217 diálogos no total para USA Rev 1. Esse total corresponde ao bloco inglês de diálogos identificado no inventário. A revisão editorial em campanha e a localização dos créditos e das demais telas continuam abertas.

| Grupo integrado | Falas |
| --- | ---: |
| Finais | 16 |
| Dicas gerais | 32 |
| Despedidas | 32 |
| Reclamações | 37 |

O lote anterior já tinha oito falas da Candy, treze do Funky e 79 do Cranky. As 79 do Cranky incluem 41 saudações, onze retornos rápidos e 27 dicas de fases. A entrada 0x3C0C2C voltou a mencionar rinocerontes com “Terra de rinocerontes!”. A dica de corrida em 0x3C1796 indica X, a tecla padrão do port para correr e rolar.

## Como abrir e revisar

Abra **Testar DKC - PT-BR.cmd**. O índice privado evidence/2026-11-10/pt-BR/cranky-complete/preview.html abre as galerias de finais, dicas gerais, despedidas, reclamações e da saudação corrigida da entrega de 2026-11-10. A seleção técnica ocorre na cabana do Cranky no quadro 4.350. A revisão em jogo das dicas gerais está registrada abaixo.

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
