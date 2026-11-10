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
