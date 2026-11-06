# Teste interativo no Windows

Protótipo experimental USA Rev 1, preparado em 2026-11-04 para o primeiro teste do usuário. Os dados da ROM permanecem locais. Ainda usa recompilação e interpretação de apoio, sem validação da campanha ou persistência.

Atualização de 2026-11-05: a persistência da Candy foi implementada e validada no cenário de QA. Para jogar com progresso pessoal, usar Jogar DKC.cmd ou o launcher antigo, agora pelo menu normal. Ver [Salvamento de progresso](13-SAVES.md). As instruções abaixo preservam a preparação inicial sem saves e o modo de entrada direta continua disponível apenas como teste isolado.

Retorno do primeiro teste: o usuário aprovou a experiência inicial e relatou perda de fluidez após a chuva. A correção de cadência e os testes posteriores estão em [Verificação de fluidez](12-FLUIDEZ.md). O registro abaixo preserva os limites da preparação inicial.

## Abrir e jogar

Depois da compilação com `./scripts/build_rev1.ps1`, abrir `Jogar DKC.cmd` ou `Jogar DKC - Teste.cmd` na raiz do projeto. Ambos iniciam pelo menu normal com saves persistentes. A apresentação foi atualizada para compor o quadro fora da tela; ver [Apresentação da janela](14-APRESENTACAO.md) e confirmar visualmente se as piscadas desapareceram.

Para o diagnóstico sem saves pessoais, executar o aplicativo com `--jungle` ou usar `Testar caverna.cmd`. A preparação percorre a receita de 4.800 quadros desde boot limpo e entrega o controle na entrada da fase. Não usa um save state nem modifica a ROM.

Abrir DKC-Rev1-Teste.exe sem argumentos inicia pelo boot normal. O programa procura o arquivo Donkey Kong Country (USA) (Rev 1).sfc junto ao executável e nos dois diretórios acima, conferindo o hash exato. Se não o encontrar, oferece o seletor de arquivo. Manter o executável em build/usa-rev1 e a receita em recipes/usa-rev1 para usar --jungle.

| Tecla | Controle |
| --- | --- |
| Setas | Direcional |
| Z | B do SNES: pular |
| X | Y do SNES: correr/rolar |
| C | A do SNES: trocar personagem |
| V | X do SNES |
| Enter | Start: iniciar/pausar |
| Shift | Select |
| A / S | L / R |
| Esc | Fechar o teste |

Clicar na janela para dar foco ao teclado. O jogo pausa ao perder o foco ou ser minimizado e limpa as teclas mantidas. A apresentação usa framebuffer 256×224 em área 4:3, com bordas pretas ao redimensionar.

## Implementação e resultado

Host Windows próprio em runner/desktop_win32.c, com GDI para apresentação e WinMM para áudio PCM estéreo de 32.040 Hz. Não houve instalação de nova biblioteca. A rotina de execução e produção de áudio é compartilhada com o runner automatizado por runner/usa_rev1.h.

Compilados os dois alvos com MSVC. Após compartilhar a rotina, os testes de 600 quadros e da receita de 4.800 quadros repetiram todos os campos dos relatórios anteriores: imagem, WRAM, VRAM, cadeia de áudio e contagens. Isso verifica a regressão do núcleo; não comprova a apresentação ou qualidade sonora na janela.

O processo interativo foi iniciado com --jungle e expôs a janela de controle após a preparação, respondendo ao Windows. A captura via Computer Use falhou duas vezes, com FrameArrived timed out e window capture timed out. Não foram enviados comandos de jogo após essas falhas. A inspeção visual, o áudio audível e as ações ao vivo ficam para o teste do usuário.

## Limites

Não há gravação de progresso em disco, save states, suporte a controle físico ou tela cheia neste host mínimo. A saída de áudio foi implementada, mas sua qualidade não foi confirmada por escuta. Se o dispositivo não abrir, o programa avisa e permite continuar sem som. Falhas de execução encerram o trecho com mensagem, sem ignorar watchdog ou erros da engine.

O log DKC-Rev1-teste.log fica junto ao executável e é refeito a cada abertura. Fechar o jogo antes de consultá-lo; a abertura atual do log pode bloquear leitura simultânea. Evidências locais da compilação e regressão estão em evidence/2026-11-04/usa-rev1/. A divergência da candidata de 55 variantes continua aberta; esta versão mantém a configuração padrão de 39.
