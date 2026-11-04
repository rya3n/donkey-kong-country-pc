# Diagnóstico e evidências

Observações locais de 2026-11-04. Hashes identificam arquivos; não provam correção funcional.

## E01 — ROM disponível

| Campo | Valor observado |
| --- | --- |
| Arquivo | `Donkey Kong Country (U) (V1.2) [!].smc` |
| Tamanho | 4.194.304 bytes, sem os 512 bytes adicionais de cabeçalho de copiador |
| Título interno | `DONKEY KONG COUNTRY` |
| Byte de mapeamento | `0x31` |
| Código de região | `1` |
| Byte de revisão | `2` |
| Checksum armazenado / calculado | `0x2BCC` / `0x2BCC` |
| Complemento armazenado | `0xD433` |
| SHA-256 | `628147468c3539283197f58f03b94df49758a332831857481ea9cc31645f0527` |
| MD5 | `2e604bc12fb8f9467765c807c24877fa` |

O nome, o cabeçalho interno e o checksum são consistentes com a identificação local como revisão 1.2. Não foi feita comparação byte a byte com um dump externo. O checksum simples do SNES não autentica a origem do arquivo.

## E02 — Entrada exigida pela base escolhida

O `upstream/scripts/generate_snesrecomp.py` exige, para o jogo original, USA v1.0 sem cabeçalho de copiador:

- Tamanho: `4194304` bytes.
- SHA-256: `fa8cacf5bbfc39ee6bbaa557adf89133d60d42f6cf9e1db30d5a36a469f74d15`.

O hash da ROM local é diferente. Renomear o arquivo ou alterar apenas a verificação não converte uma revisão em outra. A ROM v1.0 ainda não foi encontrada na pasta examinada.

## E03 — Código local e pacote distribuído na inspeção inicial

| Referência | Identidade |
| --- | --- |
| Repositório clonado | `https://github.com/elliotttate/DKC1Recomp` |
| Commit local do DKC1Recomp | `3eb9a10c49cb210df2bd63addafe2a78cf9f4e22` |
| Commit local do snesrecomp | `de94587464524ebac8dcd62e14618bf0d3953644` |
| Submódulo recomp-net | `6d848d6f9a7269d511e6e97d943c2ef0774779b0` |
| Pacote de referência | `DKC1Recomp-v0.0.17-Windows-x64.zip` |
| Commit declarado pelo pacote | `559bab62596a97e91f389b39cdeb6cda981ab7c9` |
| Engine declarada pelo pacote | `75223f35b16e4c904cea78453b9cd1fcefbcd7f2` |
| SHA-256 do ZIP | `adf90d506a255d6909906c512eacb7ab83a68b425a44373c289fe95cb489f5df` |
| SHA-256 de DKC1Recomp.exe | `e46ddf4e0e6105d7d7c52af81555632a6b4694d14990341e975932e611985541` |

O ZIP foi conferido contra o digest obtido na API oficial do GitHub. Na revisão documental, os 20 arquivos listados em `BUILDINFO.json` conferiram em tamanho e SHA-256, sem divergências. O manifesto e o ZIP vieram da mesma distribuição; isso não constitui uma auditoria independente do executável.

**Conclusão da inspeção inicial:** o clone então disponível não era o código identificado pelo pacote v0.0.17. Essa divergência foi posteriormente resolvida na preparação técnica descrita em E07. O registro acima preserva a identidade usada nos testes iniciais.

## E04 — Ferramentas observadas na inspeção inicial

| Ferramenta | Resultado da consulta |
| --- | --- |
| Python | 3.12.10 |
| Git | 2.55.0.windows.2 |
| Ninja | 1.13.0.git.kitware.jobserver-pipe-1 |
| `cl`, `cmake`, `clang`, `gcc` | Não encontrados no PATH desta sessão |

A ausência no PATH não demonstra que uma ferramenta inexiste em todo o computador. O ambiente de desenvolvedor do Visual Studio ainda precisa ser confirmado. A sessão usa PowerShell no Windows.

## E05 — Testes executados na preparação

Comando executado dentro de `upstream/`:

```powershell
python -m unittest discover -s tests -v
```

Resumo observado: `Ran 251 tests` e `FAILED (errors=10, skipped=14)`. Os erros exibidos vieram de chamadas a executáveis de compilação ausentes, com `FileNotFoundError [WinError 2]`. Há erros de subtestes; não usamos esses totais para calcular uma porcentagem de aprovação.

A saída integral não foi salva em arquivo na execução inicial. Este registro é um resumo da sessão, não um artefato completo reproduzível. Não afirmamos que resolver o compilador fará toda a suíte passar; a nova execução deverá confirmar isso.

## E06 — Estado funcional e organização

Na observação inicial, não houve geração de fontes a partir da ROM, compilação própria, boot ou gameplay local. O repositório público ainda não existia. A tentativa pelo navegador foi interrompida pela ferramenta por não identificar a URL com segurança; não foi um erro do código do port.

Atualização na mesma data: o repositório público foi criado como [rya3n/donkey-kong-country-pc](https://github.com/rya3n/donkey-kong-country-pc) usando a autenticação existente do Git e a API do GitHub. A publicação inicial contém documentação; o estado funcional do jogo permanece sem validação local.

As notas de release do pacote relatam recursos e testes dos mantenedores. Eles devem ser tratados como resultados externos, separados dos nossos.

## E07 — Início técnico após a revisão do Notion

As 11 páginas do projeto foram lidas pela conexão sem truncamento. Foram identificadas pendências de estado atual, ações futuras de PT-BR/empacotamento e escolha da revisão de código. O usuário confirmou que ainda não dispõe da ROM USA v1.0; a geração permanece bloqueada por essa entrada.

O clone limpo foi fixado na tag v0.0.17, commit `559bab62596a97e91f389b39cdeb6cda981ab7c9`; os submódulos foram inicializados em `75223f35b16e4c904cea78453b9cd1fcefbcd7f2` e `6d848d6f9a7269d511e6e97d943c2ef0774779b0`. O primeiro resultado de `python scripts/check_project.py --json` confirmou as três revisões e rejeitou a ROM v1.2 disponível, com saída 1 por pré-requisitos pendentes. A ausência de ROM não foi contornada.

Após a orientação de instalar no E:, a instância de BuildTools recém-criada no C: foi removida pelo desinstalador oficial, com código de saída 0. A reinstalação em `E:\Ferramentas\VisualStudio\2022\BuildTools` terminou com saída 0, instalação completa e sem reinicialização exigida. A antiga pasta principal no C: deixou de existir. O SDK do Windows e o instalador compartilhado da Microsoft permaneceram no C:, apesar dos destinos de cache/compartilhados solicitados no E:; não foram movidos ou apagados manualmente.

Ferramentas verificadas: BuildTools 17.14.44, toolset MSVC 14.44.35207, CMake 3.31.6-msvc6 e Ninja 1.12.1, com compilador/CMake/Ninja no E:. Um programa mínimo usando windows.h e QueryPerformanceFrequency compilou, vinculou e executou com sucesso, imprimindo MSVC_WINDOWS_SDK_OK. O SDK usado é 10.0.26100.0.

A suíte pública da v0.0.17 executou 303 testes em 11,540 segundos e terminou com FAILED (errors=2, skipped=10). Os dois erros são test_hd_material_cache e setUpClass de test_hd_preload, que chamam cc e usam flags GCC/Clang e sanitizers indisponíveis nesse ambiente MSVC. Não foram alterados nem ignorados para produzir uma aprovação artificial. Os dez skips permanecem registrados no log integral; a suíte não é considerada aprovada.

O verificador final confirmou os três commits e detectou as três ferramentas no E:. Sua única pendência de pré-requisitos é a ROM USA v1.0, com saída 1 esperada. Logs completos locais: evidence/2026-11-04/environment/toolchain.log, public-tests.log e preflight.json. Essas evidências ficam fora da publicação, conforme .gitignore. Nenhum teste de boot ou gameplay foi executado.
