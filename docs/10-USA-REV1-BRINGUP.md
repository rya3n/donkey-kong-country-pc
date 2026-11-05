# Protótipo USA Rev 1

Registro de 2026-11-04. Este é o primeiro alvo próprio para a ROM USA v1.1 (Rev 1), compilado para Windows x64. Ele executa sem janela e usa código recompilado junto com o interpretador de apoio do snesrecomp. Não é uma versão pronta para jogar.

## Entrada e procedência

- ROM local: `Donkey Kong Country (USA) (Rev 1).sfc`, 4.194.304 bytes, sem cabeçalho adicional.
- SHA-256: `df2644d435330192a13768cc1f79c5aa3084a64217a5250c6dd4ffdbe2175be4`.
- Cabeçalho: revisão 1, HiROM, checksum armazenado e calculado `0xD17C`.
- Fonte DKC1Recomp: `559bab62596a97e91f389b39cdeb6cda981ab7c9` (v0.0.17).
- Engine: `75223f35b16e4c904cea78453b9cd1fcefbcd7f2`.
- Recomp-net: `6d848d6f9a7269d511e6e97d943c2ef0774779b0`.

Rev 1 é v1.1, não v1.0. O hash continua obrigatório. A ROM v1.2 disponível é rejeitada. A checagem e as configurações v1.0 do upstream permanecem intactas.

## Componentes próprios

| Arquivo | Função |
| --- | --- |
| config/roms/usa-rev1.json | Identidade exata da entrada experimental |
| recomp/usa-rev1/bank00.cfg | Entradas iniciais lidas dos vetores da ROM |
| scripts/generate_rev1.py | Confere entrada e fontes fixadas; chama o gerador genérico |
| runner/usa_rev1.c | Carregamento, quadros, imagem, áudio e relatório sem janela |
| CMakeLists.txt | Liga o código derivado ao runtime e aos adaptadores genéricos |
| scripts/build_rev1.ps1 | Carrega o ambiente MSVC detectado e compila |
| recipes/usa-rev1/boot-to-jungle.inputs | Entrada gravada do boot até a primeira fase |

O host lê reset e NMI da ROM. Não utiliza os hooks de gameplay, endereços de funções ou adaptações widescreen da v1.0. O agendamento de quadros/HDMA e os adaptadores headless e de entrada se apoiam no host MIT do DKC1Recomp; o runtime compartilhado mantém suas próprias licenças.

## Reprodução atual

Na raiz do projeto, com Python 3.11+ e as ferramentas MSVC/CMake/Ninja preparadas:

```powershell
git clone --branch v0.0.17 --recurse-submodules https://github.com/elliotttate/DKC1Recomp.git upstream
python scripts/check_project.py --json
python scripts/generate_rev1.py --rom '.\Donkey Kong Country (USA) (Rev 1).sfc'
.\scripts\build_rev1.ps1
```

O clone só é necessário em uma cópia nova. O verificador confere os commits do lock. Nenhuma ROM acompanha o repositório. A geração cria fontes privadas em experimental/usa-rev1/generated e funcs.h ao lado da configuração; ambos ficam fora da publicação. CMake verifica a identidade da geração antes de configurar o alvo.

Teste de 600 quadros, sem botões:

```powershell
New-Item -ItemType Directory -Force evidence/rev1-600 | Out-Null
$env:SNESRECOMP_TIER2_DIR = (Resolve-Path evidence/rev1-600).Path
$env:SNESRECOMP_TIER2_MANIFEST = Join-Path $env:SNESRECOMP_TIER2_DIR 'tier2.json'
.\build\usa-rev1\dkc_rev1_headless.exe '.\Donkey Kong Country (USA) (Rev 1).sfc' 600 'evidence/rev1-600/frame'
```

Entrada na fase, em um processo novo:

```powershell
New-Item -ItemType Directory -Force evidence/rev1-jungle | Out-Null
$env:SNESRECOMP_TIER2_DIR = (Resolve-Path evidence/rev1-jungle).Path
$env:SNESRECOMP_TIER2_MANIFEST = Join-Path $env:SNESRECOMP_TIER2_DIR 'tier2.json'
.\build\usa-rev1\dkc_rev1_headless.exe '.\Donkey Kong Country (USA) (Rev 1).sfc' 4800 'evidence/rev1-jungle/frame' '.\recipes\usa-rev1\boot-to-jungle.inputs'
```

O programa salva o último quadro em PPM e imprime JSON com hashes de framebuffer, WRAM, VRAM e uma cadeia de hashes do áudio. Na receita, cada linha contém máscara hexadecimal e quantidade decimal de quadros: 0000 neutro, 0008 Start, 0001 botão B do SNES. São 4.800 quadros desde boot limpo, sem save state. Os eventos e perfis ficam nos diretórios locais de evidência.

## Resultados observados

Geração padrão: 9 raízes, 39 variantes AOT exatas em cinco bancos e 29 entradas distintas de dispatch. Esses números descrevem a saída do gerador, não a porcentagem recompilada do jogo. O relatório contou 3.310.351 passos interpretados no teste de 600 quadros.

Compilação com MSVC x64, CMake 3.31.6-msvc6 e Ninja 1.12.1 concluída. O compilador emitiu avisos de rótulos não utilizados no C gerado. Executável de referência deste registro, SHA-256: `6351c1b2fe7a8c6d887e1e4c2414882cb4fba63bbee004356527565c5b5aaae6`. Outro diretório ou horário de build pode produzir hash de binário diferente; comparar também as identidades e os resultados.

Três execuções independentes de 600 quadros produziram os mesmos quatro hashes abaixo. A recompilação final da configuração padrão repetiu esses valores:

| Saída | SHA-256 |
| --- | --- |
| Framebuffer BGRA | a7366146a96b47e75d48d3814bfe0859c71f68bcc3fac3d7429befb9b50430dd |
| WRAM | 179f92617d4af96afa7861139894fcdd8d0fb8cad4170cfe9dedf7388f826222 |
| VRAM | 628205f68fcfb17ebff713087d104ca0d896205b38855678dc0578b5386b6aec |
| Cadeia de áudio | 02da909a3411c87683ba9de70f2e905c391625b5408bd8f6cb4ab41777fd1e41 |

A cadeia de áudio começa com 32 bytes zero. Para cada quadro, SHA-256 do hash anterior concatenado com o PCM produzido substitui o hash. Não é o SHA-256 simples de um arquivo de áudio completo. Em 352 dos 600 quadros houve amostras não nulas; não houve teste de reprodução audível.

Capturas inspecionadas: Nintendo Presents em 600 quadros; animação de abertura em 3.600 sem entrada; mapa Kongo Jungle e seleção de Jungle Hijinxs nos pilotos com Start; personagem na primeira fase aos 4.800 quadros com a receita publicada. A entrada na fase foi repetida em um processo novo. Hash de framebuffer da receita: `d838411ab3a44fd43205bf1d658e20c18e9ed95123d8c308bef9673047e0d034`.

Os testes de entrada retornaram: perfil Rev 1 aceito (verificador 0), v1.2 rejeitada (verificador 1; host 2, antes de executar). Logs, perfis, capturas e resumos completos estão localmente em evidence/2026-11-04/usa-rev1/. Capturas e dados do jogo não são publicados.

## Experimento de cobertura retirado da base

Usamos o perfil limpo dos primeiros 600 quadros com a opção experimental --profile-manifest do gerador. A saída passou de 39 para 55 variantes, com 45 entradas de dispatch. Três execuções da candidata foram determinísticas entre si, mas divergiram da base em WRAM e áudio; o framebuffer e a VRAM finais ficaram iguais.

| Medida | Base 39 | Candidata 55 |
| --- | --- | --- |
| Passos interpretados | 3.310.351 | 3.260.945 |
| WRAM SHA-256 | 179f92617d4af96afa7861139894fcdd8d0fb8cad4170cfe9dedf7388f826222 | 31e9b95bd4b080118f88340a610c9b752c1f9c6a2395006116170261d8f2173e |
| Cadeia de áudio SHA-256 | 02da909a3411c87683ba9de70f2e905c391625b5408bd8f6cb4ab41777fd1e41 | 23fbd60c56d26f2c1137ce277e5d34c8988ec95c6ee93d3bd22337d5b45bfb80 |

A candidata não foi promovida. A geração e o executável atuais voltaram à configuração padrão de 39 variantes, sem perfil. A causa das diferenças ainda não foi isolada; não atribuímos a mudança apenas a timing ou a uma função específica. O próximo trabalho de cobertura deve localizar o primeiro ponto de divergência antes de ampliar a recompilação. Determinismo e imagem final igual não comprovam equivalência.

## Limites e próximos passos

Ainda faltam comparação com referência independente, janela, proporção de apresentação, áudio audível, entrada ao vivo e validação de movimento, saltos, colisões, mortes e saídas. O host não implementa persistência em disco ou save states. A entrada na primeira fase não aprova V05 por completo nem a campanha. PT-BR e abertura direta continuam posteriores à estabilização.

Nenhuma ferramenta nova foi instalada nesta etapa. As instalações já preparadas no E: foram reutilizadas. O SDK e o instalador compartilhado previamente registrados no C: permanecem como no diagnóstico.
