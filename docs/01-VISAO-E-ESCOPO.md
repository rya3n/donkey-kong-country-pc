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

O pedido mais recente define a prioridade: concluir e revisar a documentação antes de avançar com código, ferramentas adicionais e GitHub público.
