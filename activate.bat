@echo off
REM Script de ativação do ambiente virtual para CMD
REM Use: activate.bat

set "VENV_PATH=%~dp0.venv"
set "SCRIPTS_PATH=%VENV_PATH%Scripts"

if exist "%SCRIPTS_PATH%\activate.bat" (
    call "%SCRIPTS_PATH%\activate.bat"
    echo Ambiente virtual Python 3.11 ativado!
) else (
    echo Script de ativação não encontrado. Ativando manualmente...
    set "VIRTUAL_ENV=%VENV_PATH%"
    set "PATH=%SCRIPTS_PATH%;%PATH%"
    echo Ambiente virtual Python 3.11 ativado!
    python --version
)

