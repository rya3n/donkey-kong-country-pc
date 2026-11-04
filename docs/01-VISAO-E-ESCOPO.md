# Visão e escopo

Edição inicial: 2026-11-04. Estado: objetivo acordado, requisitos técnicos iniciais propostos.

## Objetivo

Conseguir jogar Donkey Kong Country de SNES em um aplicativo nativo de Windows e construir uma base de trabalho que possamos compreender, modificar e reproduzir. A recompilação e a engenharia reversa são meios aceitos pelo usuário para chegar a esse resultado.

O caminho inicial escolhido usa o DKC1Recomp e uma ROM USA v1.0 fornecida localmente. Nosso trabalho começa pela organização, reprodução e validação dessa base. Os créditos e o histórico de terceiros permanecem identificados.

## Primeira entrega jogável proposta

| ID | Requisito | Evidência para aceitar |
| --- | --- | --- |
| R01 | Abrir o jogo no Windows com a ROM suportada | Registro de versão, hash e execução visível |
| R02 | Chegar do boot ao menu e à primeira fase | Roteiro repetível e captura da sessão |
| R03 | Mover, pular, rolar, trocar personagens e interagir | Verificação das ações na fase, com resultado esperado |
| R04 | Produzir imagem e áudio estáveis no trecho testado | Captura visível e observação de áudio identificadas |
| R05 | Salvar e recuperar progresso | Teste entre duas execuções e preservação de backup |
| R06 | Compilar localmente a revisão escolhida | Comandos completos, log e hash do executável resultante |
| R07 | Manter documentação reproduzível | Outra sessão consegue seguir o roteiro sem informações ocultas |

Estes são critérios propostos para orientar a implementação; ainda não foram executados. Passar a primeira fase constitui uma demonstração inicial, não validação do jogo completo.

## Escopo inicial

Windows x64, jogo original, ROM USA v1.0, código e engine fixados em revisões identificáveis. O primeiro diagnóstico deve estabelecer uma imagem nativa de referência de 256×224, com configuração gráfica registrada. Resolução do framebuffer e proporção de exibição são parâmetros diferentes; ambos entram no relatório.

Controle por teclado é parte da verificação inicial. Controle físico será testado quando houver dispositivo disponível, sem presumir um modelo específico.

## Itens para uma etapa posterior

Suporte à ROM v1.2, mudanças de gameplay, widescreen próprio, aumento de taxa de simulação, arte HD, mods, outras plataformas e instalador. A presença desses recursos no projeto de terceiros não os torna entregas já validadas pelo nosso projeto.

## Forma de trabalhar

O usuário define objetivos e prioridades; o assistente prepara documentação, investigações e alterações dentro desse escopo. Não há prazo, equipe ampliada ou calendário de reuniões definido. As novas propostas permanecem explicitamente identificadas até serem adotadas.

A documentação inicial e a criação do repositório público foram realizadas. A próxima etapa técnica é preparar a base reproduzível; as metas finais acordadas estão descritas a seguir.

## Meta final acordada — PT-BR e abertura direta

Após estabilizar e validar o port, a meta definida pelo usuário é traduzir o jogo para português brasileiro e entregá-lo com a experiência de um aplicativo comum de Windows: abrir o executável e jogar.

A ordem de trabalho é: port funcional, validação ampla, tradução e empacotamento final. A fase de tradução depende da aceitação da base estável. A expressão “funcionando perfeitamente” será acompanhada de evidências: campanha, transições, controles, áudio e persistência avaliados, sem defeitos críticos conhecidos nos cenários cobertos; não é uma garantia de ausência absoluta de bugs.

### Tradução

Inventariar textos e telas; definir glossário e tom em PT-BR; verificar fonte e acentos; traduzir os textos acessíveis ao jogador e revisar sua exibição no jogo. Confirmar o inventário antes de definir sua cobertura como completa. Tradução de textos em gráficos pode exigir trabalho separado. A técnica de localização ainda será escolhida após conhecer a base estável.

### Experiência de aplicativo

A abertura habitual deve iniciar o jogo sem terminal, comandos, compilação ou escolha repetida de ROM. Saves e preferências devem persistir, e os arquivos necessários devem acompanhar a instalação ou a versão portátil. O usuário não exigiu um único arquivo físico: o executável pode ter dados e bibliotecas de suporte, desde que a abertura continue simples.

Como proposta técnica, a instalação ou primeira preparação poderá importar os dados da ROM local uma única vez. O formato final — instalador, pacote portátil, dados embutidos ou arquivo de dados separado — permanece em aberto. A preparação e o pacote local devem manter a separação entre o código publicado e os dados do jogo.
