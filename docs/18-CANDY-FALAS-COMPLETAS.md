# Oito falas identificadas da Candy em PT-BR

Atualização de 2026-11-06 do piloto separado. As seis mensagens de revisita foram traduzidas, somando oito falas da Candy em inglês identificadas nas tabelas da Rev 1. Os nomes Candy Kong e Honey Kong e a placa Candy's Save Point permanecem originais. Falas de outros personagens e tradução integral do jogo continuam em etapas próprias.

## Onde conferir

Abrir **Testar DKC - PT-BR.cmd** para jogar no piloto e observar as mensagens nas visitas à Candy. O atalho mantém seu perfil próprio de saves. **Testar falas da Candy.cmd** continua oferecendo a apresentação e a instrução inicial numa prévia sem persistência; ele não força todas as mensagens de revisita.

A revisão automatizada produz uma galeria privada em evidence/2026-11-06/pt-BR/candy-complete/verified-all/preview.html, com as oito capturas nativas e os textos correspondentes. Nessa galeria, as mensagens foram selecionadas individualmente pelo comparador sem janela, para verificar cada texto sem depender do sorteio do jogo. Não representa uma campanha completa.

## Redação das seis mensagens adicionais

| Contexto | Redação em PT-BR |
| --- | --- |
| Boas-vindas ao voltar | Oi, gente! Tem algo bom para salvar? |
| Oferta de ajuda | Ajudo vocês, macacos, a salvar o jogo? |
| Convite ao barril | Que tal uma voltinha no meu barril de salvamento? |
| Apelido carinhoso | Ei, Honey Kong! Boa hora para salvar seu progresso até aqui! |
| Reconhecer o esforço | Deve ter dado trabalho chegar até aqui! Que tal salvar seu jogo? |
| Incentivar a aproveitar a chance | Uau! Vocês chegaram longe! Salvem seu jogo agora, enquanto podem! |

Mantidos o tom amistoso, a brincadeira com os macacos, o convite para girar no barril e a referência ao progresso. Honey Kong foi preservado como apelido, conforme a política de nomes e contexto. Não foi acrescentada regra de salvamento automático nem alterada a instrução de pular no barril.

## Integração

Os oito registros ocupam 0x3C315B–0x3C3334, com tamanhos individuais de 46, 72, 38, 38, 49, 69, 80 e 81 bytes. Conservados os ponteiros de apresentação e revisita, o tamanho de cada registro, o número de linhas e os terminadores. As novas frases recebem somente preenchimento lateral com espaços, sem truncar ou substituir palavras.

O preenchimento também preserva a paridade do comprimento das novas linhas. Isso mantém o comportamento do alinhamento e evita que a leitura do terminador altere o campo seguinte da tabela de cor. A verificação não foi ampliada para aceitar essa diferença: o gerador foi ajustado e o caso foi repetido.

Adicionado o glifo **é**, além de **á**, **ê** e **ó**, na fonte de diálogo. O código 0x5E estava ausente nos quatro blocos ingleses identificados e usa um glifo de 16 bytes em 0x29DABC. A integração agora tem 17 regiões de dados em memória: cinco dos menus, oito falas e quatro glifos. O arquivo da ROM, seu código de jogo e as unidades AOT não são alterados.

## Verificações concluídas

- Build Release e 26 testes Python passaram, incluindo preservação de Candy Kong/Honey Kong, limites, preenchimento, paridade e ponteiros de revisita.
- As oito mensagens foram comparadas individualmente com o original, usando o renderizador real. Capturas inspecionadas: sem cortes e com acentos legíveis.
- O áudio completo coincidiu em todos os casos. Nas seis mensagens novas, os 128 KiB de WRAM coincidiram integralmente. Nas duas anteriores, ficaram apenas as diferenças de alinhamento já identificadas. Nenhuma diferença visual fora da faixa do diálogo.
- Os passos interpretados variaram de -40 a +19 conforme o texto processado; esses valores são registrados, não confundidos com frames ou velocidade. O relógio continua em 60,0988 Hz.
- A regressão dos menus e da entrada da fase passou; no quadro 4.800, imagem, WRAM e áudio coincidiram com a versão habitual.
- Um par Candy/reinício passou entre aplicativo, runner e disco, em perfis de QA, com a mesma SRAM do fixture anterior. Nenhum save pessoal foi usado nessa verificação.
- ROM e executável habitual conservaram seus hashes. Não houve nova instalação.

Para selecionar cada caso, o runner sem janela aceita DKC_REV1_QA_CANDY_MESSAGE com um dos oito endereços conhecidos. O diagnóstico muda somente a tabela da cópia de teste antes de inicializar a execução; a mesma seleção é feita no original e no piloto. Essa opção não existe no executável com janela e não altera o sorteio ou a escolha das falas do jogador. No build normal do piloto, todos os ponteiros originais permanecem intactos.

O aceite humano da redação e da leitura ao vivo continua pendente. Outros idiomas, acentos não utilizados aqui, cobertura de campanha e tradução completa não foram aprovados por estes testes.

## Reprodução

```powershell
./scripts/build_rev1.ps1 -HeadlessOnly
./scripts/build_ptbr_pilot.ps1
python -m unittest discover -s tests -p 'test_ptbr*.py' -v
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/candy-all-check --all-messages
python scripts/verify_ptbr_menu_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/candy-regression
python scripts/verify_rev1_saves.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/candy-save-regression --build-dir build/ptbr-pilot --desktop-name DKC-Rev1-PTBR-Piloto.exe --repeats 1
```

Para repetir somente um caso, acrescentar --message 321d a --all-messages. Usar uma pasta de saída nova e fechar o piloto antes de recompilar ou executar o teste de saves.

Evidências finais privadas: evidence/2026-11-06/pt-BR/candy-complete/verified-all/, verified-menu-gameplay/, verified-saves/, unit-tests.log e build.log. O catálogo privado draft-03 reúne oito falas da Candy no piloto e seis rascunhos de Funky/Cranky ainda fora do runtime. Status editorial continua em rascunho até o aceite humano.

Próxima etapa: revisar as falas com o usuário e preparar as falas do Funky Kong, mantendo os nomes e verificando instruções de transporte, tom e contexto.
