@echo off
setlocal
set "DKC_REV1_BENCH_FRAMES="
set "DKC_REV1_TEST_ENTRANCE="
set "DKC_REV1_SAVE_DIR="
set "DKC_REV1_PREPARE_INPUT="
set "DKC_REV1_TEST_ROM="
if not exist "%~dp0build\usa-rev1\DKC-Rev1-Teste.exe" (
    echo Compile o projeto com scripts\build_rev1.ps1 antes de jogar.
    pause
    exit /b 1
)
start "" "%~dp0build\usa-rev1\DKC-Rev1-Teste.exe"
