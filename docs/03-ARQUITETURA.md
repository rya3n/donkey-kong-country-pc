# Arquitetura inicial

Estado: integração experimental Rev 1 iniciada. A seção de componentes do upstream descreve a referência; o alvo próprio atual está detalhado em [Protótipo USA Rev 1](10-USA-REV1-BRINGUP.md).

## Como o port é produzido

```text
ROM USA v1.1 (Rev 1) + configuração própria de entradas
                        |
                        v
            gerador do snesrecomp
                        |
                        v
          fontes C derivadas da ROM (locais)
                        |
         + runtime + host Windows + dependências
                        |
                        v
          compilador C e etapa de ligação
                        |
                        v
          executável nativo + dados da ROM local
```

A recompilação estática traduz trechos identificados do programa do SNES em código que o compilador do PC consegue processar. O runtime fornece os serviços necessários para reproduzir o comportamento do hardware e conectar imagem, áudio e controles ao sistema operacional.

Um aplicativo nativo ainda pode usar modelos de PPU, áudio e outros componentes do SNES. O alvo próprio atual é híbrido: 39 variantes AOT e interpretação de caminhos ainda não compilados. Sua execução não comprova recompilação integral nem equivalência com hardware. A configuração v1.0 do upstream permanece separada e sem alterações.

## Componentes da base local

| Componente | Papel | Local de referência |
| --- | --- | --- |
| Metadados de recompilação | Entradas, limites e contratos de dispatch | `upstream/recomp/` |
| Gerador | Valida a ROM e chama análise/emissão | `upstream/scripts/generate_snesrecomp.py` |
| Framework | Recompilação e runtime compartilhado | `upstream/snesrecomp/` |
| Integração do jogo | Adaptação do DKC1 ao runtime | `upstream/runner/dkc1_game.c` |
| Verificação de ROM | Carregamento e checagem da entrada | `upstream/runner/verified_rom.c` |
| Host | Janela, apresentação, áudio e entrada | `upstream/runner/` |
| Fontes geradas | Saída privada do gerador | `upstream/generated/snesrecomp/` — ainda não criada |
| Validação | Modelos, replays, capturas e análise | `upstream/tests/` e `upstream/tools/` |

No clone examinado, o build Windows usa SDL2 e miniz via CMake. O pacote v0.0.17 descreve apresentação Direct3D 11 e fallback OpenGL; não presumimos que os detalhes desse pacote sejam idênticos aos do clone atual.

## Domínios que precisamos distinguir

Apresentação trata de framebuffer, escala, proporção, filtros e margens. Streaming e ativação tratam de tiles, VRAM, sprites e ciclo de vida dos objetos. Gameplay trata de colisões, limites, física, saídas e progressão.

Uma imagem mais larga não comprova que objetos fora da área original funcionam corretamente. Uma mudança futura deve declarar o domínio afetado e comprovar seus efeitos. O primeiro marco proposto usa a apresentação nativa como referência antes de avaliar melhorias.

## Como investigar um problema

Identificar ROM, código, engine e executável; obter uma reprodução pequena; consultar os diagnósticos existentes; comparar estado e imagem; só então alterar o subsistema responsável. Para endereços e símbolos, a orientação do upstream começa em `python tools/atlas.py <consulta>`.

O `upstream/AGENTS.md` governa alterações naquele clone. Ele pede consulta ao catálogo de diagnósticos antes de criar ferramentas duplicadas, preservação de `reference/` e correções no gerador ou nos metadados em vez de edições manuais em `generated/`. Este documento resume a direção; as instruções completas devem ser lidas antes da alteração correspondente.
