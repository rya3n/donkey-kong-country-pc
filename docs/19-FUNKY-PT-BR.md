# Falas do Funky Kong em PT-BR

Entrega de 2026-11-06 no piloto separado para USA v1.1 (Rev 1). Integradas as quatro mensagens inglesas identificadas na tabela do Funky Kong. Mantidos Funky Kong, Jumbo Barrel e os desenhos das placas. O texto conserva o tom descontraído e a limitação de transporte a lugares já visitados.

## Conferir a tradução

Abrir **Testar DKC - PT-BR.cmd** para jogar com o perfil próprio do piloto e visitar Funky's Flights. O executável habitual e seus saves continuam separados. **Testar falas da Candy.cmd** permanece como prévia da Candy.

A galeria privada evidence/2026-11-06/pt-BR/funky/all-messages/preview.html mostra as quatro capturas nativas com legendas. A seleção individual das mensagens acontece somente no comparador sem janela; o aplicativo usa a sequência original.

| Contexto | Redação em PT-BR |
| --- | --- |
| Apresentação | Opa, galera! Sou o Funky Kong! |
| Transporte | Meu irado Jumbo Barrel leva vocês voando a qualquer ponto da ilha! |
| Restrição | Só que, infelizmente, ele só leva vocês a locais que já visitaram... |
| Comentário final | o que é uma baita chatice, pode crer! |

As duas últimas mensagens formam uma frase contínua; a minúscula inicial da última é intencional. A oferta de transporte deve ser lida com a restrição seguinte. A tradução não libera novos destinos.

## Integração e limites

Configuração em localization/pt-BR/funky-pilot.json e gerador em scripts/generate_ptbr_funky_pilot.py. A tabela Rev 1 em 0x3C036C contém os quatro ponteiros 3074, 3096, 30D9 e 3125; ela é conferida e preservada. As mensagens mantêm os tamanhos de 34, 67, 76 e 54 bytes, respectivamente, e suas quantidades de linhas, terminadores e paridades de comprimento. O gerador acrescenta apenas espaços laterais, sem truncar palavras.

A fonte é a mesma dos diálogos da Candy. Reutilizados os quatro glifos á/ê/ó/é já integrados, sem novos códigos ou alterações nos glifos aprovados. A geração compartilhada mantém as verificações de nomes, fonte, limites e uso prévio dos códigos nos blocos ingleses. A composição das 21 regiões de dados também rejeita sobreposições.

As alterações são aplicadas à cópia da ROM em memória do piloto. O arquivo da ROM, o código do cartucho, as unidades AOT, a sequência das mensagens e a lógica de transporte permanecem originais. A velocidade continua em 60,0988 Hz. O suporte de fonte continua restrito aos textos ingleses identificados.

## Verificações

- Build Release e 32 testes Python passaram, incluindo os limites e a preservação dos nomes Funky Kong/Jumbo Barrel.
- As quatro mensagens foram renderizadas individualmente no cenário do Funky. Áudio completo e os 128 KiB de WRAM coincidiram com o original em todos os casos; diferenças de imagem somente na faixa do diálogo. Capturas inspecionadas, legíveis e sem cortes.
- Os passos interpretados variaram de -8 a +24 conforme o texto processado. Esses valores não representam alteração de frames ou velocidade.
- A sequência normal, sem selecionar ou trocar mensagens, passou nos quadros 4.350, 4.650, 4.950 e 5.250: quatro falas em ordem, áudio e WRAM inteira iguais ao original, com diferenças visuais apenas no texto.
- A regressão da Candy passou nos quadros 4.350, 4.500 e 4.650, mantendo somente os ajustes de alinhamento já conhecidos, com áudio igual e nenhuma diferença visual fora do texto.
- Menus e entrada da fase passaram nos quadros 1.700, 2.300 e 4.800; na fase, imagem, WRAM e áudio coincidiram com a versão habitual.
- Um ciclo de salvar na Candy e reabrir passou entre aplicativo, runner e disco, com perfis de QA separados. SRAM idêntica ao fixture anterior; nenhum save pessoal foi usado.
- O catálogo privado draft-04 passou nas verificações de inventário e nomes. Mantém os rascunhos como histórico, registra o aceite anterior da Candy e a revisão humana pendente do Funky. Os dois rascunhos do Cranky continuam fora do runtime.
- ROM e executável habitual mantiveram seus hashes. Nenhuma nova instalação.

A revisão humana destas quatro prévias continua pendente. O teste não comprova campanha completa nem transporte entre todos os mundos com progresso real.

## Reprodução

```powershell
./scripts/build_rev1.ps1 -HeadlessOnly
./scripts/build_ptbr_pilot.ps1
python -m unittest discover -s tests -p 'test_ptbr*.py' -v
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/funky-all-check --character funky --all-messages
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/funky-natural-check --character funky
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/funky-candy-regression
python scripts/verify_ptbr_menu_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/funky-menu-regression
python scripts/verify_rev1_saves.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/funky-save-regression --build-dir build/ptbr-pilot --desktop-name DKC-Rev1-PTBR-Piloto.exe --repeats 1
```

O runner aceita DKC_REV1_QA_FUNKY_MESSAGE somente no build sem janela, para selecionar um dos quatro endereços existentes e compará-lo com o original sob a mesma seleção. O aplicativo com janela ignora esse diagnóstico. O modo sem --all-messages mantém a tabela original e confere a sequência em quatro checkpoints.

Evidências privadas em evidence/2026-11-06/pt-BR/funky/: all-messages/, natural-sequence/, candy-regression/, menu-gameplay/, saves/, unit-tests.log e logs de build. A galeria e os dados derivados permanecem fora do GitHub público.

Próxima etapa: revisão das quatro prévias pelo usuário; depois, preparar um primeiro lote do Cranky Kong, preservando os nomes e o contexto das dicas.
