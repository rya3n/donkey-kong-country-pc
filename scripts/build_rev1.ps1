[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$report = & python (Join-Path $PSScriptRoot 'check_project.py') --json
if ($LASTEXITCODE -ne 0) { throw "Preflight failed: $report" }
$toolchain = ($report | ConvertFrom-Json).toolchain
if (-not $toolchain.installation) { throw 'A complete Visual Studio installation is required.' }
$developerShell = Join-Path $toolchain.installation 'Common7/Tools/Launch-VsDevShell.ps1'
& $developerShell -Arch amd64 -HostArch amd64 -SkipAutomaticLocation
if (-not $env:VSCMD_VER) { throw 'Visual Studio developer environment was not loaded.' }

$buildDirectory = Join-Path $projectRoot 'build/usa-rev1'
& $toolchain.cmake -S $projectRoot -B $buildDirectory -G Ninja `
    -DCMAKE_BUILD_TYPE=Release -DCMAKE_MSVC_RUNTIME_LIBRARY=MultiThreaded `
    "-DCMAKE_MAKE_PROGRAM=$($toolchain.ninja)"
if ($LASTEXITCODE -ne 0) { throw 'CMake configuration failed.' }
& $toolchain.cmake --build $buildDirectory --parallel 6
if ($LASTEXITCODE -ne 0) { throw 'Native build failed.' }
