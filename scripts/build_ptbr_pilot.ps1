[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$report = & python (Join-Path $PSScriptRoot 'check_project.py') --json
if ($LASTEXITCODE -ne 0) { throw "Preflight failed: $report" }
$toolchain = ($report | ConvertFrom-Json).toolchain
& python (Join-Path $PSScriptRoot 'generate_ptbr_menu_pilot.py') --rom (Join-Path $projectRoot 'Donkey Kong Country (USA) (Rev 1).sfc')
if ($LASTEXITCODE -ne 0) { throw 'PT-BR menu data generation failed.' }
$developerShell = Join-Path $toolchain.installation 'Common7/Tools/Launch-VsDevShell.ps1'
& $developerShell -Arch amd64 -HostArch amd64 -SkipAutomaticLocation
if (-not $env:VSCMD_VER) { throw 'Visual Studio developer environment was not loaded.' }
$buildDirectory = Join-Path $projectRoot 'build/ptbr-pilot'
& $toolchain.cmake -S $projectRoot -B $buildDirectory -G Ninja `
    -DCMAKE_BUILD_TYPE=Release -DCMAKE_MSVC_RUNTIME_LIBRARY=MultiThreaded `
    -DDKC_BUILD_PTBR_PILOT=ON "-DCMAKE_MAKE_PROGRAM=$($toolchain.ninja)"
if ($LASTEXITCODE -ne 0) { throw 'Pilot CMake configuration failed.' }
& $toolchain.cmake --build $buildDirectory --parallel 6
if ($LASTEXITCODE -ne 0) { throw 'Pilot native build failed.' }
