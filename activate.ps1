# Script de ativação do ambiente virtual
# Use: . .\activate.ps1

$venvPath = Join-Path $PSScriptRoot ".venv"
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"

if (Test-Path $activateScript) {
    Write-Host "Ativando ambiente virtual Python 3.11..." -ForegroundColor Green
    & $activateScript
} else {
    Write-Host "Script de ativação não encontrado. Ativando manualmente..." -ForegroundColor Yellow
    
    # Ativação manual
    $env:VIRTUAL_ENV = $venvPath
    $oldPath = $env:Path
    
    # Adicionar Scripts ao PATH
    $scriptsPath = Join-Path $venvPath "Scripts"
    if (Test-Path $scriptsPath) {
        $env:Path = "$scriptsPath;$oldPath"
        Write-Host "✅ Ambiente virtual Python 3.11 ativado!" -ForegroundColor Green
        python --version
    } else {
        Write-Host "❌ Erro: Diretório Scripts não encontrado em $venvPath" -ForegroundColor Red
    }
}

