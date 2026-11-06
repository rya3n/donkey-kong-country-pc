# Donkey Kong Country — Port para PC

Projeto pessoal de estudo, integração e desenvolvimento de uma versão nativa de Donkey Kong Country para Windows, partindo do trabalho público do DKC1Recomp.

**Meta final:** após estabilizar e validar o port, traduzir o jogo para PT-BR e preparar uma versão de Windows em que o jogador abra o executável e jogue, com saves persistentes e sem configuração repetida.

**Etapa atual: menus, oito falas da Candy, quatro do Funky, seis saudações e nove dicas do Cranky em PT-BR para USA v1.1 (Rev 1).** Acrescentadas quatro dicas de Monkey Mines, mantendo os nomes das fases e as pistas sobre pneus, bananas e vida extra. Fonte e traduções anteriores preservadas. Abrir **Testar DKC - PT-BR.cmd** para jogar no perfil próprio. Redação e verificações em [Dicas de Monkey Mines](docs/22-DICAS-MONKEY-MINES-PT-BR.md). As novas prévias aguardam revisão; campanha, coleta dos segredos e tradução completa continuam pendentes.

Após compilar, abra **Jogar DKC.cmd**, escolha seu arquivo no menu e salve na Candy. Para continuar, reabra e selecione o mesmo arquivo. Saves em data/usa-rev1/saves/, fora da pasta de build; detalhes em [Salvamento de progresso](docs/13-SAVES.md). O launcher antigo Jogar DKC - Teste.cmd também abre pelo menu normal. Testar caverna.cmd é isolado dos saves pessoais.

Controles: setas, Z para pular, X para correr/rolar, C para trocar, Enter para Start e Esc para fechar. F6 alterna preencher/4:3; F11 alterna janela/tela cheia. Preencher mantém toda a imagem, esticando-a conforme o formato da janela ou monitor. Detalhes em [Teste interativo](docs/11-TESTE-INTERATIVO.md).

Após o primeiro teste do usuário, corrigimos a cadência da janela preservando 60,0988 Hz e verificamos trechos iniciais de 40 entradas de fases e chefes. Resultados e cobertura em [Verificação de fluidez](docs/12-FLUIDEZ.md).

Repositório público do projeto: [rya3n/donkey-kong-country-pc](https://github.com/rya3n/donkey-kong-country-pc). Publicamos documentação, configuração e integração próprias; os arquivos de jogo, fontes derivadas da ROM e binários permanecem locais.

## Comece por aqui

| Documento | O que você encontra |
| --- | --- |
| [Visão e escopo](docs/01-VISAO-E-ESCOPO.md) | Objetivo, requisitos e limites da primeira versão |
| [Diagnóstico e evidências](docs/02-DIAGNOSTICO.md) | Arquivos, hashes, ferramentas e verificações realizadas |
| [Arquitetura](docs/03-ARQUITETURA.md) | Caminho da ROM até o executável e papel de cada componente |
| [Ambiente e reprodução](docs/04-AMBIENTE-E-REPRODUCAO.md) | Pré-requisitos e roteiro proposto de compilação |
| [Plano de validação](docs/05-VALIDACAO.md) | Como comprovar que o port funciona |
| [Etapas e pendências](docs/06-ETAPAS-E-PENDENCIAS.md) | Sequência do trabalho, dependências e critérios de conclusão |
| [Registro de decisões](docs/07-DECISOES.md) | O que foi decidido e o que permanece como proposta |
| [Créditos e publicação](docs/08-CREDITOS-E-PUBLICACAO.md) | Procedência do código e organização do futuro repositório |
| [Ferramentas e referências](docs/09-FERRAMENTAS-E-REFERENCIAS.md) | Repositórios sugeridos e possível uso no projeto |
| [Protótipo USA Rev 1](docs/10-USA-REV1-BRINGUP.md) | Comandos atuais, resultados e limites do primeiro executável |
| [Teste interativo](docs/11-TESTE-INTERATIVO.md) | Como abrir a janela e testar com teclado |
| [Verificação de fluidez](docs/12-FLUIDEZ.md) | Correção de cadência, comparação e matriz de entradas |
| [Salvamento de progresso](docs/13-SAVES.md) | Saves da Candy, backup e testes entre processos |
| [Apresentação da janela](docs/14-APRESENTACAO.md) | Correção de piscadas confirmada, preencher/4:3 e tela cheia adaptável |
| [Preparação PT-BR](docs/15-PT-BR.md) | Glossário, preservação dos nomes, inventário parcial e rascunhos |
| [Piloto PT-BR dos menus](docs/16-PILOTO-PT-BR.md) | Build separado, cinco rótulos gráficos, acentos e regressão |
| [Primeiras falas da Candy](docs/17-CANDY-PT-BR.md) | Apresentação, instruções de salvamento, fonte de diálogo e prévia isolada |
| [Oito falas da Candy](docs/18-CANDY-FALAS-COMPLETAS.md) | Mensagens de revisita, Honey Kong preservado e galeria de revisão |
| [Falas do Funky Kong](docs/19-FUNKY-PT-BR.md) | Quatro mensagens, Jumbo Barrel, restrição de transporte e prévias |
| [Primeiro lote do Cranky e fonte](docs/20-CRANKY-E-FONTE-PT-BR.md) | Seis saudações e correção da altura do ê na fonte compartilhada |
| [Dicas de Kongo Jungle](docs/21-DICAS-KONGO-JUNGLE-PT-BR.md) | Cinco dicas de fases, nomes preservados e revisão das pistas |
| [Dicas de Monkey Mines](docs/22-DICAS-MONKEY-MINES-PT-BR.md) | Quatro dicas adicionais, pneus, bananas e salto antecipado |
| [Log de atualizações](CHANGELOG.md) | Histórico datado do que mudou e do que foi verificado |

## Situação em uma leitura

- A decisão atual é trabalhar com a ROM USA Rev 1 disponível (v1.1), substituindo a espera pela v1.0. A v1.2 também está na pasta e é rejeitada pelo novo perfil.
- A configuração Rev 1 começa pelos vetores da própria ROM, sem importar os endereços e adaptações de gameplay da v1.0.
- A base de desenvolvimento está fixada na v0.0.17, commit `559bab62596a97e91f389b39cdeb6cda981ab7c9`, com engine e submódulos identificados em `config/upstream.lock.json`.
- MSVC, CMake e Ninja foram instalados e verificados em E:\Ferramentas. O SDK do Windows e o instalador compartilhado da Microsoft permanecem no C:.
- O usuário confirmou a fluidez e os saves da Candy passaram por três reinícios em processos novos. Campanha completa, save states e cobertura ampliada continuam pendentes.

## Organização dos arquivos

```text
README.md                  entrada da documentação
CHANGELOG.md               log de atualizações
docs/                      documentos do nosso projeto
config/roms/               identidade da entrada experimental
recomp/usa-rev1/            configuração nova de recompilação
runner/                    integração própria com o runtime
recipes/usa-rev1/           sequência reproduzível de botões
experimental/              fontes derivadas privadas; ignoradas
build/                     executáveis locais; ignorados
data/usa-rev1/saves/        progresso pessoal e backup; ignorados
upstream/                  clone independente do DKC1Recomp
downloads/                 arquivo ZIP oficial baixado
runtime/                   pacote oficial extraído, sem validação de gameplay local
*.smc / *.sfc              arquivos locais do usuário; fora da publicação
```

Os documentos em Markdown são a referência técnica versionável. A área exclusiva do projeto no Notion funciona como índice e cópia de consulta desta edição; a atualização entre os dois lugares é manual e deve ser registrada no log. Este projeto não tem relação de sincronização automática com o repositório dos autores do DKC1Recomp.

Os links de navegação do Notion privado ficam no arquivo local `.project-local.md`, excluído da publicação. O conteúdo técnico público pode ser consultado pelos documentos deste repositório.

**Próximas tarefas:** ampliar o teste de campanha e de saves com progresso real e investigar a divergência de memória/áudio encontrada ao ampliar a recompilação. O roteiro atual de persistência está em [Salvamento de progresso](docs/13-SAVES.md). A suíte pública anterior executou 303 testes, com 2 erros e 10 ignorados; esse resultado permanece registrado, sem declaração de aprovação.

Para repetir a checagem local, execute `python scripts/check_project.py` ou use `--json` para obter um relatório estruturado. O verificador retorna código 1 quando há pré-requisitos pendentes e não altera a ROM, o código ou o sistema.

Base consultada: [DKC1Recomp](https://github.com/elliotttate/DKC1Recomp). Os avanços relatados pelos autores são evidências externas e não equivalem a resultados obtidos aqui.
