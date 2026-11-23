# Primeira sessão de campanha PT-BR

Sessão de 2026-11-10 em Windows com a ROM USA Rev 1 e o piloto de 217 diálogos do commit `2a2bee76707f66f695dc277db0b84bd1c7e52cc5`.

## Percurso

| Trecho | Resultado observado |
| --- | --- |
| Menu e primeira entrada em Jungle Hijinxs | Novo jogo iniciado pelo menu normal. O primeiro encontro com um Kritter consumiu uma vida, e o jogo voltou ao mapa. Foi possível entrar na fase de novo. |
| Jungle Hijinxs | Corrida, saltos e barris de checkpoint e de parceiro. A saída devolveu o jogador ao mapa com Ropey Rampage disponível. |
| Ropey Rampage | Entrada pelo mapa, chuva, escalada e travessia das cordas oscilantes. A saída abriu Cranky's Cabin e o caminho para Reptile Rumble. |
| Cranky's Cabin | Saudação, dica de Coral Capers com o nome Croctopus, dica de superpulo e despedida em português. Quatro caixas legíveis na sequência escolhida pelo jogo. Retorno ao mapa. |
| Reptile Rumble | Seleção pelo mapa e entrada na primeira caverna. |

Os comandos foram explorados quadro a quadro em um programa auxiliar local. A rota escolhida foi repetida desde o menu pelo executável headless do piloto, com um perfil vazio. A repetição usa apenas comandos do controle. O resultado cobre a lógica do jogo e o framebuffer de 256 × 224. A experiência na janela e a continuidade do áudio audível ainda precisam de uma sessão interativa.

## Identidade dos arquivos

| Arquivo ou conjunto | SHA-256 |
| --- | --- |
| ROM USA Rev 1 | `df2644d435330192a13768cc1f79c5aa3084a64217a5250c6dd4ffdbe2175be4` |
| `build/ptbr-pilot/dkc_rev1_headless.exe` | `074211c15fecf9a425c670b8c4312683f99825930ac50d3c15666e82be3433ca` |
| Conjunto de patches PT-BR | `1032422cde60b0e6e7bed624c5a2b35068e8fbbab65e51546f7572b4e338369e` |

No retorno ao mapa de Jungle Hijinxs (quadro 8659) e diante da cabana do Cranky (13452), o framebuffer, a WRAM, a SRAM e o hash acumulado de áudio coincidiram nas versões inglesa e PT-BR. A VRAM total diferiu nesses dois pontos. Na entrada de Reptile Rumble (15354), o framebuffer, a WRAM, a VRAM e a SRAM coincidiram. Nesse último ponto, o hash acumulado de áudio diferiu, com 14.353 quadros com amostras não nulas no piloto e 14.354 na versão inglesa. A primeira divergência fica no intervalo entre o início da visita ao Cranky e a entrada da caverna. A comparação audível e a localização do quadro exato continuam pendentes.

Os relatórios, logs, capturas e perfis ficam em `evidence/2026-11-10/pt-BR/campaign-start/`. Cada execução usa um diretório próprio de SRAM.

## Repetir o percurso

A sequência de 15.354 quadros está em [campaign-to-reptile-rumble.inputs](../recipes/usa-rev1/campaign-to-reptile-rumble.inputs). Em um PowerShell sem variáveis de diagnóstico do jogo, execute na raiz do projeto com o piloto já compilado e a ROM local.

```powershell
$replay = New-Item -ItemType Directory -Path 'evidence/campaign-replay' -ErrorAction Stop
$env:DKC_REV1_SAVE_DIR = $replay.FullName
try {
    & '.\build\ptbr-pilot\dkc_rev1_headless.exe' `
        '.\Donkey Kong Country (USA) (Rev 1).sfc' 15354 `
        (Join-Path $replay.FullName 'reptile-rumble') `
        '.\recipes\usa-rev1\campaign-to-reptile-rumble.inputs'
} finally {
    Remove-Item Env:DKC_REV1_SAVE_DIR
}
```

Quadros para inspecionar em perfis vazios independentes: 5064 (mapa após morrer), 8659 (mapa após concluir Jungle Hijinxs), 9963 (escalada sob chuva), 13121 (mapa após Ropey Rampage), 14039 (dica de Coral Capers) e 15354 (entrada da caverna).

## Retomada

Retomar em Reptile Rumble e seguir por Kongo Jungle. Visitar Funky e Candy pelo mapa para conferir as falas em contexto. Registrar o progresso ao salvar com Candy, fechar o jogo e confirmar o mesmo arquivo em um novo processo. A campanha de Monkey Mines e o aceite de V14, V16 e V17 continuam pendentes.

## Rolamento, barril DK e troca de personagem (V06)

Em 2026-11-23, o [roteiro de 5.392 quadros](../recipes/usa-rev1/campaign-jungle-actions.inputs) foi reproduzido desde o menu, em um novo perfil de um jogador. A entrada é Jungle Hijinxs (`0x0016`). O roteiro usa apenas comandos de controle e termina na mesma fase, com Donkey Kong à frente e as cinco vidas iniciais.

| Quadro | Ação confirmada nas capturas |
| ---: | --- |
| 4.520 | Donkey avança em rolamento. |
| 4.620 | Um segundo rolamento atinge o primeiro Kritter, sem perda de vida. |
| 4.660 | Donkey carrega o barril DK acima da cabeça. |
| 4.684–4.720 | O barril é arremessado e quebra. Diddy é libertado e se junta à dupla. |
| 4.956–4.970 | Após o comando A do SNES, Diddy assume a liderança e responde ao direcional. |
| 5.016 | Diddy aparece no ar após o salto. |
| 5.359–5.392 | Depois de os dois voltarem ao chão, Select devolve o controle a Donkey. O direcional volta a mover Donkey, com Diddy seguindo atrás. |

O teste confirma o uso do Y do SNES para pegar o barril e soltá-lo ao liberar o botão, o B para pular e a troca por A ou Select. No teclado do port, essas ações correspondem a X, Z, C e Shift. [Manual da Nintendo](https://www.nintendo.co.jp/clvs/manuals/common/pdf/CLV-P-SAALE.pdf) · [Mapeamento do port](11-TESTE-INTERATIVO.md#abrir-e-jogar)

O coletor de QA repetiu o percurso sem snapshot. Em cinco pontos, os executáveis sem janela da versão base e do piloto reproduziram a mesma captura do coletor. Entre os dois builds, também coincidiram os hashes de imagem, WRAM, SRAM e áudio acumulado nesses quadros. A sequência de entradas gravada pelo coletor coincidiu quadro a quadro com o roteiro. Os 65 testes Python passaram. Evidências locais em `evidence/2026-11-23/v06-jungle/`. A validação desta sequência cobre um jogador e execução sem janela.

Para repetir, use o comando da seção [Repetir o percurso](#repetir-o-percurso) com o roteiro de Jungle Hijinxs acima, 5.392 quadros e um perfil novo.

## Primeira sala de bônus de Jungle Hijinxs (V14)

Em 2026-11-23, o [roteiro de 8.235 quadros](../recipes/usa-rev1/campaign-jungle-first-bonus.inputs) repetiu os primeiros 7.280 quadros da rota até Reptile Rumble e desviou na caixa de Rambi. O percurso começa no menu em um perfil novo, chega à caixa com três vidas e 30 bananas e entra no bônus com Rambi. As duas perdas de vida do prefixo ocorreram antes do desvio.

| Quadro | Resultado |
| ---: | --- |
| 7.338–7.378 | Diddy quebra a caixa e monta em Rambi. |
| 7.611 | Rambi abre o acesso na parede e o jogo seleciona a entrada do bônus (`0x0006`). |
| 7.651–7.708 | A sala carrega e fica jogável com Diddy montado. |
| 7.912–7.919 | O salto alcança o balão vermelho. O contador sobe de três para quatro vidas e o registro chega a 70 bananas, 40 a mais que na entrada. |
| 7.994–8.051 | A saída seleciona `0x0008` e o jogo volta à fase principal. |
| 8.196–8.235 | Diddy e Rambi estão na copa após a saída. O direcional esquerdo volta a mover a dupla e a câmera recua de 4.183 para 4.138. |

Quatro pontos de verificação foram repetidos nos executáveis sem janela da versão base e do piloto PT-BR. As capturas coincidiram com as do coletor, e os hashes de imagem, WRAM, SRAM e áudio acumulado coincidiram entre os builds. O coletor partiu do menu e suas entradas coincidiram quadro a quadro com o roteiro publicado. Os 65 testes Python passaram. As evidências ficam em `evidence/2026-11-23/v14-bonus-jungle/`.

Para repetir, use o comando da seção [Repetir o percurso](#repetir-o-percurso) com o roteiro de bônus, 8.235 quadros e um perfil novo. O resultado cobre a primeira sala, a recompensa e o retorno à fase. O percurso continua no [segundo bônus](#segunda-sala-de-bônus-de-jungle-hijinxs-v14).

## Segunda sala de bônus de Jungle Hijinxs (V14)

Em 2026-11-23, o [roteiro de 9.806 quadros](../recipes/usa-rev1/campaign-jungle-second-bonus.inputs) começou no menu em um perfil de QA vazio. Ele repete os 8.235 quadros do primeiro bônus e segue com Rambi até o segundo acesso.

| Quadro | Resultado |
| ---: | --- |
| 8.235–8.531 | Diddy e Rambi recuam pela fase e avançam contra a segunda parede. A sala fica jogável com Diddy a pé, diante dos três barris giratórios (entrada `0x001a`). |
| 8.590–8.849 | Diddy salta sob cada barril. Os três param no símbolo do Rambi. |
| 8.969–9.272 | A ficha dourada do Rambi aparece. Diddy se aproxima e comemora a coleta. |
| 9.435–9.767 | O jogo seleciona a entrada `0x006e`. Diddy retorna montado em Rambi à fase principal, com quatro vidas e 70 bananas. |
| 9.791–9.806 | A dupla responde ao direcional direito, e a câmera avança de 4.252 para 4.300. |

A versão base e o piloto PT-BR repetiram os mesmos quadros do coletor em cinco pontos, incluindo os três barris combinados, a ficha, a coleta e a fase após o retorno. Os hashes de imagem, WRAM, SRAM e áudio acumulado coincidiram entre os builds nesses pontos. As entradas do coletor coincidiram quadro a quadro com o roteiro publicado. Os 65 testes Python passaram. As evidências ficam em `evidence/2026-11-23/v14-bonus-jungle2/`.

Para repetir, use o [comando de replay](#repetir-o-percurso) com o roteiro acima, 9.806 quadros e um perfil novo para cada execução. Use `build/usa-rev1/dkc_rev1_headless.exe` para a versão base. O teste cobre os dois bônus de Jungle Hijinxs em um jogador e em execução sem janela. O percurso da V14 avança para os [bônus de Ropey Rampage](#salas-de-bônus-de-ropey-rampage-v14).

## Salas de bônus de Ropey Rampage (V14)

Em 2026-11-23, dois roteiros partiram do menu em perfis de QA vazios. Cada um reaproveita a rota até Reptile Rumble e desvia para um bônus de Ropey Rampage. A tabela registra os quadros de cada roteiro separadamente.

| Roteiro | Entrada e desafio | Recompensa | Retorno à fase |
| --- | --- | --- | --- |
| [Primeiro bônus, 12.150 quadros](../recipes/usa-rev1/campaign-ropey-first-bonus.inputs) | Queda após a letra O leva ao barril que lança Diddy para a sala `0x001c`. No quadro 10.860 ele está na plataforma inicial. Os saltos passam pelas seis cordas. | Letra N conferida no quadro 11.664. O contador foi de 68 a 76 bananas entre a entrada jogável e a saída. | Entrada `0x006f`, três vidas e 76 bananas. Entre os quadros 12.126 e 12.150, o direcional direito desloca Diddy de 11.999 para 12.027. |
| [Segundo bônus, 13.952 quadros](../recipes/usa-rev1/campaign-ropey-second-bonus.inputs) | Queda no vão antes da placa de seta leva à sala `0x001b`. No quadro 12.866, o balão está sobre o terceiro barril. Diddy salta sob esse barril. | O balão fica disponível no centro no quadro 13.036. Diddy salta para pegá-lo e passa de três para quatro vidas até o quadro 13.233. | Entrada `0x0070`, quatro vidas e 69 bananas. Entre os quadros 13.918 e 13.952, o direcional esquerdo desloca Diddy de 13.412 para 13.377. |

Os executáveis sem janela da versão base e do piloto PT-BR coincidiram em oito pontos de verificação, quatro de cada roteiro. As capturas também coincidiram com as do coletor iniciado sem snapshots. Os hashes de imagem, WRAM, SRAM e áudio acumulado foram iguais entre os builds nesses pontos. Os comandos gravados coincidiram quadro a quadro com os dois roteiros. Os 65 testes Python passaram. As evidências ficam em `evidence/2026-11-23/v14-bonus-ropey/`.

Para repetir, use o [comando de replay](#repetir-o-percurso) com o roteiro e o total de quadros da tabela. Use um perfil vazio por execução e `build/usa-rev1/dkc_rev1_headless.exe` para a versão base. A V14 segue no [primeiro bônus de Reptile Rumble](#primeiro-bônus-de-reptile-rumble-v14).

## Primeiro bônus de Reptile Rumble (V14)

Em 2026-11-23, o [roteiro de 15.773 quadros](../recipes/usa-rev1/campaign-reptile-first-bonus.inputs) começou no menu com um perfil vazio e reaproveitou a rota até a saída de Ropey Rampage. No mapa, a seleção passou pela cabana do Cranky e seguiu direto à caverna. O ensaio começa a fase com três vidas e 69 bananas.

| Quadro | Resultado |
| ---: | --- |
| 14.089 | Controle disponível na caverna, entrada `0x0001`. |
| 14.565–14.728 | Donkey Kong pega o barril do outro lado da elevação perto da letra K, salta de volta com ele e vira à direita. |
| 14.758 | O barril atinge a parede perto da letra K. Os fragmentos confirmam a abertura. |
| 14.958 | Donkey e Diddy na primeira sala, entrada `0x0002`, com três vidas e 77 bananas. |
| 15.098 | Donkey atravessa a primeira passagem baixa e alcança o balão vermelho com um salto. O total sobe para quatro vidas e 82 bananas. |
| 15.245 | A dupla passa pela segunda passagem baixa e alcança a saída. O contador chega a 87 bananas, dez a mais que na entrada da sala. |
| 15.745–15.773 | Retorno pela entrada `0x0009`, com quatro vidas e 87 bananas. Após o comando à esquerda, Donkey se afasta do pneu de retorno e seu X passa de 2.042 para 2.013. |

Os executáveis sem janela da versão base e do piloto PT-BR coincidiram nos quatro pontos comparados (parede, sala, balão e retorno). As capturas também coincidiram com o coletor executado desde o menu, e os dois executáveis apresentaram os mesmos hashes de imagem, WRAM, SRAM e áudio acumulado nesses quadros. Os comandos gravados pelo coletor coincidiram com o roteiro. Os 65 testes Python passaram. Evidências locais em `evidence/2026-11-23/v14-bonus-reptile1/`.

Para repetir, use o [comando de replay](#repetir-o-percurso) com o roteiro acima, 15.773 quadros e um perfil novo por execução. Use `build/usa-rev1/dkc_rev1_headless.exe` para a versão base. O roteiro continua na [sala dos canhões de Reptile Rumble](#sala-dos-canhões-de-reptile-rumble-v14).

## Sala dos canhões de Reptile Rumble (V14)

Em 2026-11-23, o [roteiro de 16.939 quadros](../recipes/usa-rev1/campaign-reptile-second-bonus.inputs) começou no menu com um perfil vazio. Os primeiros 15.773 quadros repetem o primeiro bônus. A partir do retorno à caverna, Donkey Kong usa dois pneus para alcançar a plataforma e saltar à esquerda para o canhão de entrada.

| Quadro | Resultado |
| ---: | --- |
| 15.829–15.952 | Os dois saltos com impulso dos pneus levam à plataforma do barril DK. |
| 16.014–16.271 | Donkey entra no canhão suspenso e chega à sala `0x0048`, com quatro vidas e 92 bananas. |
| 16.289–16.501 | Um salto inicia o trajeto automático. O coletor confirma a passagem de Donkey por nove canhões distintos, do primeiro ao último. |
| 16.369–16.371 | O total de vidas passa de quatro para cinco ao atingir 100 bananas. O contador já mostra uma banana no quadro 16.371. |
| 16.591 | A dupla chega à plataforma do cacho final. O contador termina em 30, equivalente a 38 bananas coletadas na sala. |
| 16.911–16.939 | Donkey volta à plataforma da caverna pela entrada `0x00c9`, com cinco vidas e 30 bananas. O direcional direito move Donkey de 2.336 para 2.365. |

Os executáveis sem janela da versão base e do piloto PT-BR coincidiram em quatro quadros. Foram comparados o canhão de entrada, a sequência em andamento, a recompensa e o retorno à fase. Em cada ponto, as capturas coincidiram com as do coletor e os hashes de imagem, WRAM, SRAM e áudio acumulado coincidiram entre os dois executáveis. O coletor começou no menu e as entradas gravadas coincidiram com o roteiro quadro a quadro. Os 65 testes Python passaram. Evidências locais em `evidence/2026-11-23/v14-bonus-reptile2/`.

Para repetir, use o [comando de replay](#repetir-o-percurso) com o roteiro acima, 16.939 quadros e um perfil novo por execução. Use `build/usa-rev1/dkc_rev1_headless.exe` para a versão base. O terceiro bônus de Reptile Rumble é o próximo ensaio da V14. A escuta com o jogo em janela segue em V09/V14.
