@echo off
setlocal
set "DKC_REV1_BENCH_FRAMES="
set "DKC_REV1_TEST_ENTRANCE="
set "DKC_REV1_SAVE_DIR="
set "DKC_REV1_PREPARE_INPUT="
set "DKC_REV1_TEST_ROM="
if not exist "%~dp0build\ptbr-pilot\DKC-Rev1-PTBR-Piloto.exe" (
    echo Compile o piloto com scripts\build_ptbr_pilot.ps1 antes de testar.
    pause
    exit /b 1
)
start "" "%~dp0build\ptbr-pilot\DKC-Rev1-PTBR-Piloto.exe"
