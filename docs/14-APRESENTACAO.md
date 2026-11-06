# Apresentação sem limpeza preta intermediária

Registro de 2026-11-05. O usuário confirmou o funcionamento dos saves e relatou piscadas rápidas da tela inteira, também durante a abertura e em todas as fases. O relato indica um problema geral de apresentação; a confirmação da causa no monitor ainda depende do novo teste humano.

## Alteração

O host anterior executava FillRect preto diretamente na janela antes de desenhar o framebuffer. Essas duas escritas deixavam uma imagem preta intermediária disponível durante a atualização.

Agora runner/gdi_present.c compõe fundo, bordas e imagem em um DIB de memória. Somente depois de concluir essa composição, copia o quadro inteiro para a janela com BitBlt. O fundo automático da classe também foi removido; WM_ERASEBKGND já era tratado. O buffer acompanha o tamanho da área de jogo e libera os objetos GDI ao fechar. Falhas de composição não apresentam um quadro parcialmente preparado e são registradas no log.

A imagem continua em 4:3, com o mesmo escalonamento de pixels. Quadros pretos produzidos pelo próprio jogo, como transições, continuam sendo exibidos. O núcleo, clocks, áudio, entradas e persistência não foram alterados. O alvo permanece 60,0988 Hz.

## Verificação executada

| Verificação | Resultado e alcance |
| --- | --- |
| Compilação Release MSVC | Aplicativo e testes nativos compilados |
| Teste gráfico sem ROM | Destino permanece intacto durante a composição; saída RGB equivalente ao desenho anterior em seis tamanhos, incluindo 4:3, largo, alto e 1×1 |
| Carregamento e transições | Texto de preparação equivalente e quadro preto real preservado |
| Recursos GDI | 500 redimensionamentos, sem aumento de objetos após liberar o buffer |
| Persistência | Sete testes de IO e três pares de salvar na Candy/reabrir em processos novos passaram; aplicativo, runner e disco coincidiram |
| Regressão de execução | Framebuffer e WRAM do aplicativo após 4.800 quadros de preparação e 600 adicionais coincidiram com o runner de 5.400 quadros |
| Agendamento, janela oculta | 600 quadros; descartados 60 de aquecimento: média 16,638 ms, p95 17,945 ms, zero conclusões além do prazo, alvo 60,0988 Hz |
| Dados pessoais | Save e backup permaneceram byte a byte iguais aos arquivos anteriores ao QA |

O teste de agendamento com janela oculta mede a execução e o relógio do host; não mede o compositor ou a atualização física do monitor. Os testes GDI usam destinos em memória e comprovam o contrato de composição, sem demonstrar que o sintoma visual desapareceu no computador do usuário. A ausência de piscadas permanece pendente de confirmação humana.

Evidências privadas: evidence/2026-11-05/flicker/, incluindo presenter-tests.log, save-io-tests.log, saves-regression/results.json e pacing/. Nenhum save de teste foi copiado para o perfil pessoal. Nenhuma dependência nova instalada.

## Repetir

Depois de compilar com scripts/build_rev1.ps1, executar build/usa-rev1/rev1_present_tests.exe para o teste gráfico. A regressão de saves usa scripts/verify_rev1_saves.py, conforme [Salvamento de progresso](13-SAVES.md).

Para a confirmação visual, abrir Jogar DKC.cmd e observar a apresentação e algumas fases, inclusive com o tamanho habitual da janela. Registrar se a tela inteira ainda apaga rapidamente. O aceite desta correção não equivale à validação da campanha completa.

## Referências da implementação

[CreateDIBSection — Microsoft](https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-createdibsection) documenta o bitmap em memória e a sincronização GDI. [BitBlt — Microsoft](https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-bitblt) documenta a cópia de um bloco entre contextos de desenho. A implementação própria fica no host Rev 1; a engine upstream permanece intacta.
