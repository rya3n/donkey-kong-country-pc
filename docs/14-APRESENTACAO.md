# Apresentação sem limpeza preta intermediária

Registro de 2026-11-05. O usuário confirmou o funcionamento dos saves e relatou piscadas rápidas da tela inteira, também durante a abertura e em todas as fases. O relato indica um problema geral de apresentação; a confirmação da causa no monitor ainda depende do novo teste humano.

Retorno posterior do usuário em 2026-11-05: a tela parou de piscar após a correção 7043b6d. P16 aceita no teste relatado. O registro abaixo preserva as evidências e limites da execução original.

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

O teste de agendamento com janela oculta mede a execução e o relógio do host; não mede o compositor ou a atualização física do monitor. Os testes GDI usam destinos em memória e comprovam o contrato de composição. A confirmação visual posterior veio do usuário, sem ampliar a cobertura para a campanha completa.

Evidências privadas: evidence/2026-11-05/flicker/, incluindo presenter-tests.log, save-io-tests.log, saves-regression/results.json e pacing/. Nenhum save de teste foi copiado para o perfil pessoal. Nenhuma dependência nova instalada.

## Repetir

Depois de compilar com scripts/build_rev1.ps1, executar build/usa-rev1/rev1_present_tests.exe para o teste gráfico. A regressão de saves usa scripts/verify_rev1_saves.py, conforme [Salvamento de progresso](13-SAVES.md).

Para repetir o teste visual, abrir Jogar DKC.cmd e observar a apresentação e algumas fases, inclusive com o tamanho habitual da janela. O aceite desta correção não equivale à validação da campanha completa.

## Preencher a janela e detectar o monitor

Após o aceite das piscadas, o usuário pediu retirar as bordas e adaptar a apresentação a monitores diferentes. O modo padrão agora preenche toda a área da janela com a imagem completa. Não corta as laterais, o chão ou a interface; em monitores largos, a imagem fica mais larga que na proporção original. Detectar a resolução não cria conteúdo lateral adicional no jogo.

- **F6:** alterna preencher e 4:3 original. Em 4:3, bordas pretas voltam quando o formato da janela exigir.
- **F11:** alterna janela e tela cheia sem moldura. Consulta MonitorFromWindow e GetMonitorInfo para usar o monitor atual, incluindo sua posição no desktop, em vez de assumir o monitor principal.
- Ao voltar da tela cheia, restaura tamanho, posição e estado da janela. Mudanças de resolução ou de monitor durante a tela cheia reajustam o tamanho. O programa não muda resolução nem frequência do sistema.
- A escolha de proporção vale para a sessão; a próxima abertura começa em preencher. O jogo continua pausando quando perde foco e Esc continua fechando o aplicativo.

Preencher remove as bordas acrescentadas pelo host. Preto que faça parte da própria imagem, carregamentos e transições do cartucho permanece visível. Os dois modos continuam usando composição fora da tela e a mesma simulação a 60,0988 Hz.

Verificações desta extensão: build Release passou; comparação RGB em oito tamanhos (4:3, widescreen, ultrawide, retrato e mínimo 1×1) comprovou cobertura total em preencher e equivalência do modo 4:3 anterior. Testes de composição isolada, preto real e 500 redimensionamentos continuaram passando. Janelas ocultas passaram por 20 ciclos de tela cheia/reajuste/restauração por monitor conectado, verificando limites do cliente, origem, estilo e posição restaurada. O boot de 600 quadros preservou framebuffer e WRAM da referência. Evidências em evidence/2026-11-05/display-modes/.

Os testes usam janelas ocultas e destinos GDI em memória. A inspeção visual dos novos modos e sua validação em outros computadores permanecem pendentes; não foram simulados monitores desconectados ou configurações de DPI diferentes.

Retorno posterior de 2026-11-05: o usuário confirmou que a versão com os novos modos está funcionando perfeitamente. P17 aceita no teste relatado; outros computadores e configurações de monitor continuam sem cobertura declarada. A próxima etapa é a validação da campanha e de saves com progresso real.

## Referências da implementação

[CreateDIBSection — Microsoft](https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-createdibsection) documenta o bitmap em memória e a sincronização GDI. [BitBlt — Microsoft](https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-bitblt) documenta a cópia de um bloco entre contextos de desenho. A implementação própria fica no host Rev 1; a engine upstream permanece intacta.

[Posicionamento em vários monitores — Microsoft](https://learn.microsoft.com/en-us/windows/win32/gdi/positioning-objects-on-multiple-display-monitors) orienta consultar o monitor da janela e suas dimensões para tela cheia. [SetWindowPlacement — Microsoft](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowplacement) documenta a restauração da posição e do estado da janela.
