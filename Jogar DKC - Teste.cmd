@echo off
if not exist "%~dp0build\usa-rev1\DKC-Rev1-Teste.exe" (
    echo Compile o projeto com scripts\build_rev1.ps1 antes de jogar.
    pause
    exit /b 1
)
start "" "%~dp0build\usa-rev1\DKC-Rev1-Teste.exe" --jungle
