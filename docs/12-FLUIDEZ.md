# Verificação de fluidez

Registro de 2026-11-04, após o primeiro teste do usuário. Relato: primeiras fases fluidas, com perda de fluidez em trechos posteriores à chuva, começando pela primeira caverna. Foi solicitada a verificação das fases seguintes, preservando a velocidade original.

## Retorno após a correção

O usuário confirmou que o jogo agora está funcionando perfeitamente em seu teste. O ajuste de fluidez foi aceito, e o código de 6b2b5b9 permanece como base de trabalho. A cobertura exata dos trechos jogados não foi informada; campanha completa e persistência continuam com seus próprios critérios de validação. Nenhuma alteração adicional de velocidade ou código foi necessária para esse aceite.

## Correção aplicada

O host já usava 60,0988 quadros de simulação por segundo, aproximadamente o ritmo NTSC. Esse alvo foi mantido. Não houve aumento de FPS, geração de quadros, mudança de física, clocks do cartucho ou taxa de áudio de 32.040 Hz.

Para repetir o teste humano rapidamente, abrir **Testar caverna.cmd**. Ele usa --caverna para entrar diretamente em Reptile Rumble, percorrendo a mesma preparação do diagnóstico, e entrega o controle sem limite de duração. Os controles continuam iguais. O launcher limpa a variável de benchmark para impedir encerramento automático. Essa entrada direta é uma facilidade de teste, sem representar a progressão normal da campanha.

A espera da janela usava timeouts em milissegundos. Em Reptile Rumble, uma medição reproduziu intervalos irregulares mesmo com o cálculo terminando em cerca de 7 ms. Substituímos a espera por um waitable timer de alta resolução e mantivemos a consulta ao relógio QPC antes de permitir cada quadro. Eventos de teclado continuam acordando a janela sem adiantar a simulação. Após atraso excessivo, o host retoma a cadência sem uma rajada de quadros para compensá-lo.

A fila de áudio agora espera o evento de conclusão do WinMM quando fica cheia, em vez de consultar repetidamente por timeout. Nenhuma dessas mudanças amplia a cobertura AOT ou altera o código do jogo. A candidata anterior de 55 variantes continua desativada; o padrão mantém 39.

## Comparação da janela

Dois processos independentes, entrada limpa em Reptile Rumble, 900 quadros interativos neutros por execução. Análise dos últimos 840, descartando 60 de aquecimento, com o analisador existente upstream/tools/analyze_pacing.py. Não havia outra execução do jogo ou varredura de fases durante cada medição.

| Medida | Antes | Depois |
| --- | --- | --- |
| Alvo de simulação | 60,0988 Hz | 60,0988 Hz |
| Intervalo médio entre conclusões de apresentação | 16,643 ms | 16,641 ms |
| Percentil 95 do intervalo | 30,796 ms | 17,417 ms |
| Percentil 99 do intervalo | 31,988 ms | 17,862 ms |
| Intervalo máximo | 32,401 ms | 23,040 ms |
| Trabalho médio por quadro | 7,035 ms | 7,175 ms |
| Atraso de início no percentil 95 | 14,609 ms | 0,934 ms |
| Conclusões após o prazo do quadro | 175 | 0 |

São timestamps do host e da conclusão da chamada GDI. Não medem diretamente o momento em que o monitor mostrou cada imagem. A melhora observada não garante a eliminação de todos os engasgos do Windows ou de todas as cenas do jogo. O arquivo de log usa o esquema dkc1.pacing.v1 e fica desativado no uso normal, salvo quando DKC1_PACING_LOG for definido.

## Cobertura das fases seguintes

Foram executadas 40 entradas de fases e chefes, incluindo as duas fases iniciais como controles e todas as entradas principais da primeira caverna até Gang Plank Galleon. Cada processo começou do boot limpo. Um mecanismo exclusivo de diagnóstico redirecionou a entrada do mapa no quadro 4202, antes do carregamento pelo próprio cartucho, mantendo a ROM intacta. Esse redirecionamento não é usado pelo launcher normal.

Os identificadores estruturais foram consultados no disassembly de referência e as capturas locais foram inspecionadas. Em nove casos a captura aos 5.100 quadros já mostrava retorno ao mapa após o trecho neutro; esses casos foram repetidos com captura aos 4.400 quadros para conferir a sala efetivamente carregada. Não foram tratados mapas como confirmação visual de gameplay.

A [matriz completa](validation/rev1-entry-performance.csv) registra 300 amostras de cálculo por entrada, dos quadros 4350 a 4649, com entrada neutra. Houve 40 saídas com código zero. Das 12.000 amostras, nenhuma excedeu o orçamento de 16,639 ms; o maior percentil 95 foi 8,097 ms em Platform Perils e o maior valor isolado foi 11,718 ms em Bouncy Bonanza. O tempo medido inclui execução, desenho PPU e produção de áudio, sem espera de apresentação.

Essa cobertura verifica carregamento e um trecho inicial de cada cena. Não é uma campanha completa: não cobre todos os inimigos, posições da câmera, combates, bônus, transições, ações do jogador ou comportamento no decorrer de uma fase inteira. O teste humano nos trechos relatados continua necessário.

## Regressão e carga acumulada

- Três novos replays de 600 quadros repetiram todos os campos do relatório anterior, incluindo imagem, WRAM, VRAM e cadeia de áudio.
- A execução da janela por 900 quadros na caverna terminou com framebuffer e WRAM idênticos à mesma sequência automatizada de 5.700 quadros desde boot.
- O teste da caverna foi repetido com os 1.803 registros de cobertura acumulados da sessão anterior do usuário, usando a API de teste já existente na engine. O relatório completo continuou idêntico ao teste sem essa carga: imagem, WRAM, VRAM, áudio e contagens. O p95 de cálculo nessa repetição foi 5,422 ms, sem indicar saturação pelo tamanho da tabela nesse trecho. Esse teste coincidiu com a recaptura de outras entradas e não é uma comparação isolada de velocidade.
- Fonte, engine e submódulos fixados permaneceram sem alterações. O define SNESRECOMP_TIER2_TEST é usado somente pelo alvo headless para disponibilizar a API de diagnóstico, sem habilitar esse caminho no aplicativo do jogador.

## Como repetir

Compilar com scripts/build_rev1.ps1. Para repetir a varredura, escolher uma pasta de saída nova:

```powershell
python scripts/profile_rev1_levels.py --rom '.\Donkey Kong Country (USA) (Rev 1).sfc' --out 'evidence/nova-varredura'
```

O script aceita --only EA para selecionar a primeira caverna e --frames 4400 para uma captura anterior. Os resultados e as imagens ficam locais. O CSV público contém apenas identificadores e medidas de tempo.

Para medir a janela em um processo de teste que encerra automaticamente:

```powershell
$env:DKC_REV1_BENCH_FRAMES = '900'
$env:DKC_REV1_TEST_ENTRANCE = 'EA'
$env:DKC1_PACING_LOG = (Join-Path (Get-Location) 'evidence/pacing-caverna.jsonl')
& '.\build\usa-rev1\DKC-Rev1-Teste.exe' --jungle
```

Criar evidence antes do comando, se necessário. Esse modo ignora a pausa por perda de foco para medir um número fixo de quadros, mas continua limitado à cadência normal. Fechar o processo antes de analisar o log. Apagar as três variáveis desta sessão de PowerShell antes do uso normal. O launcher existente não define nenhuma delas.

Os logs desta edição estão em evidence/2026-11-04/usa-rev1/performance/. A API de semeadura usa DKC_REV1_COVERAGE_SEED apenas no runner headless; aceita tuplas estruturais, rejeita alvos RAM e não importa bytes de código.

## Referências

- [Microsoft: CreateWaitableTimerExW](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-createwaitabletimerexw), [SetWaitableTimerEx](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-setwaitabletimerex) e [MsgWaitForMultipleObjectsEx](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-msgwaitformultipleobjectsex).
- [Microsoft: waveOutOpen e CALLBACK_EVENT](https://learn.microsoft.com/en-us/windows/win32/api/mmeapi/nf-mmeapi-waveoutopen).
- [Disassembly DKC1 — identificadores de entrada](https://github.com/Yoshifanatic1/Donkey-Kong-Country-1-Disassembly/blob/c2080f40469c716923f550706509a0d354229841/DKC1/Misc_Defines_DKC1.asm), consultado como referência estrutural; configuração e fonte v1.0 do upstream não foram usadas para recompilar a Rev 1.
- upstream/docs/HOST_PACING.md, consultado para a distinção entre custo de execução e apresentação no monitor. A implementação completa de apresentação desse projeto não foi importada.
