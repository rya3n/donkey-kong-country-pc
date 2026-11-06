# Dicas do Cranky para Kongo Jungle em PT-BR

Entrega de 2026-11-06 no piloto separado USA v1.1 (Rev 1). Integradas as cinco dicas inglesas identificadas para as fases de Kongo Jungle. O Cranky passa a ter seis saudações e cinco dicas traduzidas, além das oito falas da Candy e quatro do Funky já integradas. Demais dicas e falas do Cranky continuam em inglês.

O usuário confirmou satisfação com a entrega anterior e autorizou avançar. O aceite em relato da correção do ê e das seis saudações está registrado no relatório 20; as cinco dicas desta entrega aguardam sua própria revisão.

## Redação e contexto

| Fase | Dica em PT-BR | Pista preservada |
| --- | --- | --- |
| Jungle Hijinxs | Em Jungle Hijinxs, fique nas copas para ganhar vidas extras. | Rota pelo alto das árvores e vidas extras |
| Ropey Rampage | A farra de Ropey Rampage fica entre uma pedra e algo bem duro! | A referência física à pedra e a algo duro |
| Barrel Cannon Canyon | Um salto de fé basta para achar Winky em Barrel Cannon Canyon. | Salto de fé, Winky e a fase correta |
| Reptile Rumble | Há bananas no fosso de cobras de Reptile Rumble! | Bananas, fosso e cobras |
| Coral Capers | O astuto Croctopus guarda seu tesouro num canto de Coral Capers. | Croctopus, itens guardados e um canto da fase |

A revisão editorial compara cada dica com o texto inglês da própria Rev 1 e com sua associação à fase. Os nomes completos das cinco fases, Winky e Croctopus foram preservados e protegidos pelo verificador.

Os jogos de palavras foram adaptados dando prioridade à pista: a referência à pedra de Ropey Rampage não virou um ditado sobre outros objetos; a expressão com bananas de Reptile Rumble explicita bananas e o fosso; a aliteração de Coral Capers não introduziu um baú ou pote literal. A dica de Winky mantém a referência do original sem acrescentar instruções de montar num animal ou pegar um objeto específico.

Essa revisão não comprova a coleta dos cinco segredos numa sessão jogável. As prévias mostram o texto selecionado no cenário do Cranky; a execução das rotas e suas condições normais continuam como cobertura de gameplay pendente.

## Conferir no piloto

Galeria privada: evidence/2026-11-06/pt-BR/cranky-tips/verified-all/preview.html. As cinco capturas nativas estão identificadas por fase e acompanhadas do texto em PT-BR. A seleção de QA serve apenas à revisão da leitura e não muda o sorteio das dicas no aplicativo.

Para jogar, abrir **Testar DKC - PT-BR.cmd**, com o perfil próprio do piloto, e visitar o Cranky. O executável habitual e seus saves permanecem separados.

## Integração

Configuração em localization/pt-BR/cranky-tips-pilot.json; função make_cranky_tips_patch em scripts/generate_ptbr_cranky_pilot.py. A tabela inglesa Rev 1 em 0x3C0184 é conferida, incluindo as repetições das primeiras cinco dicas. Os registros em 0x3C0F35, 0x3C0F72, 0x3C0FB8, 0x3C0FFC e 0x3C102E mantêm 61, 70, 68, 50 e 70 bytes, respectivamente.

Conservados os ponteiros, terminadores, linhas e paridades dos comprimentos; somente espaços laterais completam os tamanhos originais. Cada faixa também é ligada ao nome correto da fase para evitar trocas de contexto no catálogo e na galeria.

As 27 regiões anteriores permanecem byte a byte iguais, incluindo a fonte e o ê corrigido. A verificação recompôs o hash anterior 2ea40cbd2d25d9c27581c879c2881bcdc0932256fa7074a0217f35ed42a7a522 sem as cinco novas regiões. O piloto agora aplica 32 regiões de dados à cópia da ROM em memória; arquivo da ROM, código do cartucho e unidades AOT permanecem intactos. Nenhum novo glifo foi necessário; velocidade mantida em 60,0988 Hz.

O diagnóstico sem janela DKC_REV1_QA_CRANKY_MESSAGE aceita também os cinco endereços novos. Original e piloto recebem a mesma seleção técnica na tabela inglesa de despedidas, alcançada no quadro 4.350 da entrada EE de QA. O aplicativo não incorpora essa seleção e conserva as tabelas e condições originais.

## Verificações

- Build Release e 43 testes Python passaram. Os novos testes cobrem nomes completos, Winky/Croctopus, correspondência entre fase e registro, ponteiros, tamanhos e paridades.
- As cinco dicas foram comparadas individualmente: áudio completo e os 128 KiB de WRAM iguais ao original, com diferenças de imagem somente na faixa do diálogo. Capturas inspecionadas, legíveis e sem cortes. Os passos interpretados variaram de 0 a +16 conforme o texto; esse contador não altera o relógio do jogo.
- As 27 regiões anteriores foram conferidas contra o hash da entrega anterior; fonte e traduções anteriores preservadas.
- Menus e entrada da fase passaram nos quadros 1.700, 2.300 e 4.800. Na fase, imagem, áudio e WRAM coincidiram com a versão habitual.
- Duas saudações anteriores do Cranky, com uma e três linhas, foram comparadas novamente: áudio e WRAM inteira iguais ao original, com mudanças visuais somente no diálogo.
- Um ciclo Candy/reinício coincidiu entre aplicativo, runner e disco, usando saves de QA separados. SRAM igual ao fixture anterior; nenhum save pessoal usado.
- Catálogo privado draft-06 passou nas verificações de integridade e nomes: 50 registros preservados, 23 rascunhos históricos e 273 ainda sem tradução. Esses estados do inventário não substituem os aceites humanos registrados nos relatórios.
- ROM e executável habitual conservaram seus hashes. Nenhuma nova instalação.

## Reprodução

Fechar os processos de QA antes de recompilar.

```powershell
./scripts/build_rev1.ps1 -HeadlessOnly
./scripts/build_ptbr_pilot.ps1
python -m unittest discover -s tests -p 'test_ptbr*.py' -v
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/cranky-hints-check --character cranky-tips --world kongo-jungle --all-messages
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/cranky-greeting-check --character cranky --all-messages --message 07a4 --message 0a14
python scripts/verify_ptbr_menu_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/cranky-hints-gameplay
python scripts/verify_rev1_saves.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/cranky-hints-save --build-dir build/ptbr-pilot --desktop-name DKC-Rev1-PTBR-Piloto.exe --repeats 1
```

Evidências privadas em evidence/2026-11-06/pt-BR/cranky-tips/: verified-all/, greeting-regression/, menu-gameplay/, saves/, prior-patches-check.json, editorial-review.json, unit-tests.log e logs de build. Nenhuma captura, catálogo extraído, ROM, dump, save ou binário é publicado no GitHub.

Etapa seguinte implementada: [Dicas de Monkey Mines](22-DICAS-MONKEY-MINES-PT-BR.md). O filtro --world kongo-jungle permite repetir somente este lote com o verificador atual. As cinco prévias de Kongo Jungle continuam com revisão humana pendente; campanha e coleta dos segredos permanecem na matriz de validação.
