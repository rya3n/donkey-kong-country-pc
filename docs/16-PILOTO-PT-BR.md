# Primeiro piloto PT-BR dos menus

Entrega experimental de 2026-11-05, separada da versão habitual. Traduz cinco rótulos gráficos das telas de seleção de jogo e de jogadores. A tradução completa, as falas e a campanha continuam pendentes.

## Abrir o piloto

Executar **Testar DKC - PT-BR.cmd** na raiz do projeto. O atalho abre build/ptbr-pilot/DKC-Rev1-PTBR-Piloto.exe pelo boot normal. Se precisar compilar, usar scripts/build_ptbr_pilot.ps1; o script gera os gráficos privados a partir da ROM Rev 1 conferida e usa outra pasta de build.

O piloto usa data/usa-rev1-ptbr-pilot/saves/ para progresso próprio. Não carrega automaticamente o save pessoal da versão habitual. Jogar DKC.cmd continua usando o executável e o perfil anteriores. Controles, F6, F11 e velocidade permanecem iguais.

| Local | Texto do piloto |
| --- | --- |
| Seleção de arquivo | SELEÇÃO DE JOGO |
| Ação de apagar | APAGAR JOGO |
| Um jogador | 1 JOGADOR |
| Competição | 2 JOGADORES / COMPETIÇÃO |
| Equipe | 2 JOGADORES / EQUIPE |

As opções mantêm suas ações originais. O piloto não acrescenta um seletor de idioma: a arte contém um rótulo de idioma não exposto nessa tela da USA Rev 1, e desenhá-lo como opção nova seria enganoso. Apagar continua sendo uma ação destrutiva do jogo; não é necessário apagar um arquivo para avaliar o texto.

## Como foi integrado

Os textos desses menus são gráficos em tiles de 4 bits por pixel. A fonte reaproveitada foi localizada na Rev 1 em 0x3887B2, com ponteiro DMA conferido em 0x39AA62. O endereço da referência v1.0, 0x3887AF, não corresponde ao início correto na nossa ROM. Foram reconstruídos glifos de Ã e Ç dentro da célula; outros acentos ainda não são suportados por este piloto.

A fonte original é de 8×8 pixels; o piloto usa células de 8×16, com ajuste de altura para os acentos. Isso é uma primeira solução legível, não a tipografia final. A camada de brilho que continha as palavras em inglês foi removida da tela de jogadores; a seleção continua indicada pelas cores e pelo comportamento do jogo. Os desenhos dos Kongs são preservados.

O gerador produz um cabeçalho privado com cinco regiões de gráficos/tilemaps. A compilação experimental verifica a ROM original, valida o hash de cada região e aplica os dados somente à cópia em memória antes de inicializar o runtime. Não escreve na ROM do disco, não muda o cabeçalho de identificação e não altera código executável do cartucho ou unidades AOT geradas. Nomes, textos de mapa, elenco, créditos e falas ficam intactos.

| Dados em memória | Intervalo de arquivo, fim exclusivo |
| --- | --- |
| Seleção de arquivo: mapa | 0x31C2C7–0x31C887 |
| Seleção de arquivo: gráficos | 0x31C987–0x31EA67 |
| Seleção de jogadores: mapa | 0x2F86BE–0x2F8DBE |
| Seleção de jogadores: gráficos | 0x2F8DBE–0x2FB29E |
| Seleção de jogadores: camada com inglês/brilho | 0x2FB29E–0x2FB89E |

CMake mantém DKC_BUILD_PTBR_PILOT desligado por padrão. O build separado liga a opção e declara a dependência explícita do cabeçalho gerado, para recompilar quando os gráficos mudarem. Dados derivados, capturas e binários permanecem privados.

## Verificação

- Build Release do piloto concluído; 12 testes Python passaram, incluindo proteção de nomes, limites do layout, encoding planar e rejeição de ponteiro incompatível.
- Nas capturas nativas de 1.700 e 2.300 quadros, os novos textos e acentos foram inspecionados. WRAM, cadeia de áudio, passos interpretados e contagens coincidiram com a versão habitual; diferenças visuais ficaram restritas às regiões previstas de texto.
- Após a mesma receita de 4.800 quadros, na entrada da fase, imagem, WRAM e áudio coincidiram com a referência. Nenhum pixel diferente nessa captura de gameplay.
- Conferidas as quatro regiões do inventário anterior e os tiles usados pelos Kongs: bytes originais preservados.
- Na versão final do piloto, um par de salvar na Candy e reabrir em novos processos passou, comparando aplicativo, runner e disco. Os perfis eram exclusivos de QA; não foi usado save pessoal nem snapshot. Três pares também passaram em versões preliminares, mas não substituem a conferência final identificada.
- ROM e executável habitual permaneceram com os mesmos hashes. Nenhuma nova ferramenta instalada.

As capturas vêm do framebuffer nativo, e os testes de janela de QA são ocultos. Falta o aceite humano da apresentação ao vivo e da leitura no tamanho usado pelo jogador. A tipografia ainda pode receber ajuste. O suporte a controles físicos e uma campanha completa em dois jogadores não foram validados nesta entrega.

Evidências finais privadas: evidence/2026-11-05/pt-BR/menu-pilot/verified-comparison/, verified-saves/, unit-tests.log e build.log. Resultados de protótipos anteriores ficam separados e não devem ser usados como capturas da versão final.

## Reproduzir os testes

```powershell
./scripts/build_ptbr_pilot.ps1
python -m unittest discover -s tests -p 'test_ptbr*.py' -v
python scripts/verify_ptbr_menu_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/ptbr-menu-check
python scripts/verify_rev1_saves.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/ptbr-save-check --build-dir build/ptbr-pilot --desktop-name DKC-Rev1-PTBR-Piloto.exe --repeats 1
```

Os verificadores recusam reutilizar diretórios de saída. Fechar o piloto antes de recompilar ou iniciar o verificador de saves, pois o log e o executável pertencem à mesma pasta de build. A versão habitual pode continuar instalada.

Próximo trabalho: obter o retorno visual e preparar uma primeira fala da Candy, verificando a fonte e as quebras de linha do diálogo sem alterar seu nome ou a instrução de salvamento. Os 12 rascunhos anteriores continuam fora do runtime.
