# Salvamento de progresso

Registro de 2026-11-05. O host Windows da USA Rev 1 agora carrega e grava a SRAM de 2.048 bytes do cartucho. A implementação preserva a lógica de salvamento da ROM: o jogador salva na Candy e depois seleciona o mesmo arquivo no menu do jogo.

## Como usar

1. Abrir **Jogar DKC.cmd** na pasta do projeto. O antigo Jogar DKC - Teste.cmd também passa a iniciar pelo menu normal.
2. Escolher um arquivo no menu, jogar e salvar na Candy.
3. Fechar normalmente, abrir novamente e selecionar esse arquivo para continuar.

Os saves pessoais ficam em **data/usa-rev1/saves/save.srm**, na pasta do projeto no E:, fora de build/. O arquivo contém os slots do cartucho. Recompilar o executável não remove essa pasta. Na abertura seguinte, um save existente de tamanho correto recebe uma cópia em save.srm.bak antes da execução da ROM. Esse backup representa o início da sessão anterior; não é um histórico ilimitado.

Os modos --jungle e --caverna continuam como atalhos de teste e não carregam nem gravam os saves pessoais. Testar caverna.cmd permanece isolado do progresso normal. Para jogar e continuar a campanha, usar Jogar DKC.cmd. Nenhum arquivo de teste foi copiado para a pasta pessoal.

## Proteção dos arquivos

O adaptador próprio reserva o perfil para um único processo gravador. Outra janela usando o mesmo perfil é recusada. O módulo MIT desktop_sram.c, da revisão fixada do DKC1Recomp, confere os 2.048 bytes antes de alterar a SRAM, compara alterações por quadro e grava somente quando os bytes mudam. Primeiro escreve um temporário, sincroniza e então substitui o arquivo de destino. Falhas detectadas na gravação preservam o arquivo anterior.

Na falha de escrita, a janela pausa e oferece nova tentativa. Cancelar mantém a sessão pausada com o progresso ainda em memória; F5 tenta gravar novamente e continuar. Fechar normalmente também tenta gravar antes de encerrar. F5 nesse estado é uma tentativa de concluir a escrita da SRAM; não cria um salvamento em qualquer ponto da fase.

Arquivos truncados ou maiores que o esperado interrompem a abertura sem serem substituídos. A checagem do host é de tamanho/leitura; ela não promete detectar toda corrupção em um arquivo de 2.048 bytes. As verificações internas de slots continuam a cargo da ROM. Para restaurar manualmente um backup, fechar todas as janelas antes de copiar os arquivos.

## Validação realizada

O byte de tamanho de SRAM no cabeçalho da ROM Rev 1 e o runtime indicam 2.048 bytes. A validação funcional começou com perfis vazios e usou a rotina original de Candy para produzir o arquivo, em vez de fabricar um save.

Foram três repetições independentes. Cada uma executou o runner automatizado e o aplicativo Windows em perfis separados, salvou na Candy, encerrou os processos e iniciou processos novos que carregaram pelo menu. A entrada no teste de Candy foi redirecionada para $00FA antes do carregamento da cena; o trecho de movimento/pulo entrou no barril de salvar. A etapa de reabertura não forçou entrada e não carregou snapshot.

Os seis pares de comparação passaram: framebuffer, WRAM, SRAM em memória e arquivo em disco coincidiram entre os hosts. O reinício retornou à localização salva da Candy, e as capturas foram inspecionadas. O fixture mostra o primeiro arquivo a 00:00 / 00%; não é uma campanha concluída nem validação de todos os pontos de salvamento.

SHA-256 da SRAM produzida e recarregada nas três repetições: **d07d87bb3767681d50c531267f3dd0a89fc1e1ffd41f7164ba77368c5f2c5b2a**. Os testes ficam em evidence/2026-11-04/usa-rev1/saves/roundtrip-01/, iniciados na sessão anterior; nenhum save, captura ou ROM integra a publicação.

Na conclusão da etapa, os três pares foram repetidos em evidence/2026-11-05/saves/roundtrip-02/, incluindo o mesmo tratamento WM_CLOSE usado ao fechar a janela. Todos passaram novamente, com o backup da reabertura igual ao save produzido na sessão anterior.

Sete testes de arquivos reais e processos separados passaram: primeira abertura sem escrita desnecessária, leitura/gravação com backup, tamanhos incorretos, falha de escrita seguida de retry, falha de backup, exclusão de um segundo gravador e diretório Unicode.

O replay de 600 quadros sem persistência manteve todos os campos do relatório de referência. Um smoke test de 900 quadros com SRAM ativa manteve o alvo de 60,0988 Hz, intervalo médio de 16,639 ms, p95 de 17,424 ms e zero estouros do prazo após aquecimento. Esse processo rodou com janela oculta; mede o agendamento do host e não substitui uma nova avaliação visual na janela. Evidência em evidence/2026-11-05/saves/.

## Reproduzir os testes

Após compilar com scripts/build_rev1.ps1, executar na raiz:

```powershell
python -m unittest discover -s tests -p test_saves_io.py -v
python scripts/verify_rev1_saves.py --rom '.\Donkey Kong Country (USA) (Rev 1).sfc' --out 'evidence/nova-validacao-saves'
```

A pasta de saída da verificação funcional deve ser nova. Os perfis de QA são criados dentro dela; o runner automatizado só habilita persistência quando DKC_REV1_SAVE_DIR é explicitamente definido. O aplicativo também aceita essa variável para QA, e os launchers de uso normal a limpam. DKC_REV1_PREPARE_INPUT e DKC_REV1_TEST_ROM são exclusivos da preparação automatizada com benchmark. Os arquivos públicos de entrada são sequências de botões, não saves.

## Procedência e limites

runner/usa_rev1_saves.c integra o módulo [desktop_sram.c do DKC1Recomp](https://github.com/elliotttate/DKC1Recomp/blob/559bab62596a97e91f389b39cdeb6cda981ab7c9/runner/desktop_sram.c). O aviso MIT está em third_party/DKC1Recomp-LICENSE.txt. Foram reutilizadas a persistência existente e a ideia do fixture documentado em upstream/docs/INGAME_SAVES.md, adaptando a sequência e validando a ROM Rev 1. O código, a engine e os metadados v1.0 do clone permanecem intactos.

Save states, retomada exata no meio de uma fase e persistência de preferências ainda não foram implementados neste host. A cadência, física e áudio não foram acelerados. A conclusão desta etapa aprova a persistência da SRAM no cenário coberto; campanha ampla, tradução PT-BR e pacote final continuam nas etapas próprias.
