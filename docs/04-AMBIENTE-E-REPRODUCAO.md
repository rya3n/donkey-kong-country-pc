# Ambiente e reprodução

Estado atual: protótipo USA Rev 1 gerado, compilado e executado sem janela. O roteiro ativo e validado está em [Protótipo USA Rev 1](10-USA-REV1-BRINGUP.md): `python scripts/generate_rev1.py --rom CAMINHO` e `./scripts/build_rev1.ps1`. As instruções v1.0 abaixo preservam o caminho original do upstream, que não aceita a Rev 1.

## Pré-requisitos

Para o alvo atual: ROM USA Rev 1 com o SHA-256 de config/roms/usa-rev1.json; Windows x64; Python 3.11 ou superior; Git; MSVC x64 e SDK do Windows; CMake; Ninja. As ferramentas e a entrada estão disponíveis. O caminho histórico abaixo exige v1.0, que permanece ausente. O resultado anterior da suíte pública contém limitações de portabilidade registradas no diagnóstico.

As exigências de versão devem ser conferidas na revisão escolhida. O CMake do clone atual declara mínimo 3.20; o guia Windows desse clone cita Visual Studio 2022. A versão do pacote distribuído tem suas próprias notas de compatibilidade.

## 1. Identificar a entrada

No PowerShell, a partir da pasta do projeto:

```powershell
Get-FileHash -LiteralPath '.\sua-rom-USA-v1.0.sfc' -Algorithm SHA256
```

`sua-rom-USA-v1.0.sfc` é um nome de exemplo, não um arquivo existente. O resultado esperado é `fa8cacf5bbfc39ee6bbaa557adf89133d60d42f6cf9e1db30d5a36a469f74d15`. O gerador examinado exige 4.194.304 bytes, sem cabeçalho de copiador. A extensão `.smc` ou `.sfc` não determina a revisão.

## 2. Escolher e registrar a base

A inspeção inicial encontrou código e pacote de revisões diferentes. Para o primeiro build foi escolhida e aplicada a v0.0.17, correspondente ao pacote oficial. O clone estava sem alterações próprias antes da troca. As revisões exatas são registradas em `config/upstream.lock.json`: DKC1Recomp `559bab62596a97e91f389b39cdeb6cda981ab7c9`, snesrecomp `75223f35b16e4c904cea78453b9cd1fcefbcd7f2` e recomp-net `6d848d6f9a7269d511e6e97d943c2ef0774779b0`.

Comandos de consulta dentro de `upstream/`:

Em uma nova cópia do nosso projeto, preparar primeiro o clone independente a partir da raiz: `git clone --branch v0.0.17 --recurse-submodules https://github.com/elliotttate/DKC1Recomp.git upstream`. O diretório permanece ignorado no nosso repositório, e o lock é usado para conferir as revisões.

```powershell
git rev-parse HEAD
git submodule status --recursive
git status --short
```

Na sessão inicial, operações feitas por usuários diferentes acionaram a proteção de propriedade do Git. O diagnóstico usou uma exceção de `safe.directory` limitada ao comando e ao caminho específico; não foi alterada a configuração global. Se reaparecer, confirmar a propriedade do clone e trabalhar na sessão apropriada.

## 3. Confirmar o ambiente de compilação

Em um PowerShell de desenvolvedor x64 do Visual Studio, confirmar:

```powershell
Get-Command cl.exe, cmake.exe, ninja.exe, python.exe, git.exe
```

Não começar geração e compilação com pré-requisitos faltando. Downloads de dependências pelo build também exigem acesso à rede. O estado atual e os comandos efetivamente usados devem acompanhar o log da futura execução.

## 4. Compilar a revisão escolhida

O clone examinado fornece este ponto de entrada, executado dentro de `upstream/`:

```powershell
.\build_windows.ps1 -Rom '..\sua-rom-USA-v1.0.sfc' -SkipDixie
```

Na v0.0.17, o script inicializa submódulos, gera as fontes com backend Python, configura CMake/Ninja, compila, executa CTest e a suíte pública Python. Também gera a variante Dixie por padrão. Para o primeiro build do jogo original, usar `-SkipDixie`; a variante não faz parte do primeiro teste. O diretório padrão é `build-windows/release`.

Para diagnóstico manual, a geração suportada pelo script local é:

```powershell
python scripts/generate_snesrecomp.py --rom '..\sua-rom-USA-v1.0.sfc' --analysis-backend python
```

Esses comandos são instruções de reprodução pendentes. Sua presença na documentação não significa compilação concluída.

## 5. Validar e executar

Após um build bem-sucedido, registrar o hash do executável, preservar os logs e executar os cenários do plano de validação. Manter `SDL2.dll` junto ao executável quando exigido pela revisão.

O pacote oficial já extraído fica em `runtime/v0.0.17/DKC1Recomp-v0.0.17-Windows-x64/`. Ele serve como referência identificada e também exige a ROM suportada. Executá-lo futuramente não substitui comprovar uma compilação própria.

## Evidências da futura execução

Reservar uma pasta local por execução, por exemplo `evidence/AAAA-MM-DD/execucao-01/`, com comandos, saída completa, hashes e resultado dos cenários. Dados derivados do jogo e saves devem permanecer locais.

## Verificação antes de gerar o jogo

Executar `python scripts/check_project.py` na raiz do nosso projeto. A opção `--rom CAMINHO` permite conferir um arquivo específico; sem ela, o verificador examina apenas arquivos .smc/.sfc na raiz. O resultado compara os três commits com o lock, calcula o hash da ROM e procura o ambiente MSVC/CMake/Ninja. Ferramenta detectada não equivale a compilação validada.

O usuário confirmou que não dispõe da v1.0 e depois decidiu trabalhar com a Rev 1 disponível. O verificador agora consulta active_rom_profile no lock; seu resultado atual aceita a Rev 1 e não declara compatibilidade funcional do jogo.

## Local das instalações

Orientação do usuário: novas instalações devem ter destino principal no disco E:, sob `E:\Ferramentas`. A instalação de BuildTools iniciada no C: foi removida pelo instalador oficial e refeita no E:. Compilador, CMake e Ninja foram conferidos no E:. O SDK do Windows 10.0.26100.0 e o instalador compartilhado permaneceram no C:, como registrado no diagnóstico; não foram apagados manualmente.

O ambiente de desenvolvedor instalado pode ser carregado no PowerShell com `& 'E:\Ferramentas\VisualStudio\2022\BuildTools\Common7\Tools\Launch-VsDevShell.ps1' -Arch amd64 -HostArch amd64`. Depois, voltar à pasta do projeto. O teste efetivamente realizado usou VsDevCmd.bat em um processo cmd, com o compilador x64.
