# Ambiente e reprodução

Estado: roteiro proposto, ainda não validado de ponta a ponta nesta máquina. Nesta etapa criamos documentação; os comandos abaixo não foram executados como nova compilação.

## Pré-requisitos

ROM USA v1.0 com o SHA-256 do diagnóstico; Windows x64; Python 3; Git; compilador MSVC com ferramentas C++ de desktop e SDK do Windows; CMake; Ninja. Python, Git e Ninja foram encontrados. A disponibilidade do ambiente C/CMake ainda precisa ser resolvida.

As exigências de versão devem ser conferidas na revisão escolhida. O CMake do clone atual declara mínimo 3.20; o guia Windows desse clone cita Visual Studio 2022. A versão do pacote distribuído tem suas próprias notas de compatibilidade.

## 1. Identificar a entrada

No PowerShell, a partir da pasta do projeto:

```powershell
Get-FileHash -LiteralPath '.\sua-rom-USA-v1.0.sfc' -Algorithm SHA256
```

`sua-rom-USA-v1.0.sfc` é um nome de exemplo, não um arquivo existente. O resultado esperado é `fa8cacf5bbfc39ee6bbaa557adf89133d60d42f6cf9e1db30d5a36a469f74d15`. O gerador examinado exige 4.194.304 bytes, sem cabeçalho de copiador. A extensão `.smc` ou `.sfc` não determina a revisão.

## 2. Escolher e registrar a base

O clone atual e o pacote v0.0.17 têm commits diferentes. Primeiro escolher se reproduziremos o clone ou o código correspondente ao pacote; depois registrar o commit exato e os submódulos. Essa escolha permanece aberta. Guardar alterações locais antes de qualquer troca de revisão.

Comandos de consulta dentro de `upstream/`:

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
.\build_windows.ps1 -Rom '..\sua-rom-USA-v1.0.sfc'
```

Nesse clone, o script inicializa submódulos, gera as fontes com backend Python, configura CMake/Ninja, compila, executa CTest e a suíte pública Python. Seu diretório padrão é `build-windows/release`. Conferir novamente o script depois de escolher outra revisão.

Para diagnóstico manual, a geração suportada pelo script local é:

```powershell
python scripts/generate_snesrecomp.py --rom '..\sua-rom-USA-v1.0.sfc' --analysis-backend python
```

Esses comandos são instruções de reprodução pendentes. Sua presença na documentação não significa compilação concluída.

## 5. Validar e executar

Após um build bem-sucedido, registrar o hash do executável, preservar os logs e executar os cenários do plano de validação. Manter `SDL2.dll` junto ao executável quando exigido pela revisão.

O pacote oficial já extraído fica em `runtime/v0.0.17/DKC1Recomp-v0.0.17-Windows-x64/`. Ele serve como referência identificada e também exige a ROM suportada. Executá-lo futuramente não substitui comprovar uma compilação própria.

## Evidências da futura execução

Reservar uma pasta local por execução, por exemplo `evidence/AAAA-MM-DD/execucao-01/`, com comandos, saída completa, hashes e resultado dos cenários. A pasta é uma convenção proposta e ainda não contém resultados. Dados derivados do jogo e saves devem permanecer locais.
