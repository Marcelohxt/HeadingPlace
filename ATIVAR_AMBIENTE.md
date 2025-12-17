# 🐍 Como Ativar o Ambiente Virtual

## Método 1: PowerShell (Recomendado)

```powershell
# Permitir execução de scripts (apenas uma vez)
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# Ativar ambiente virtual
. .\.venv\Scripts\Activate.ps1
```

Ou simplesmente execute:
```powershell
. .\activate.ps1
```

## Método 2: CMD (Prompt de Comando)

```cmd
.venv\Scripts\activate.bat
```

Ou:
```cmd
activate.bat
```

## Método 3: Ativação Manual (se os scripts não funcionarem)

```powershell
$env:VIRTUAL_ENV = "$PWD\.venv"
$env:Path = ".\.venv\Scripts;" + $env:Path
python --version  # Deve mostrar Python 3.11.9
```

## Verificar se está ativo

Quando o ambiente virtual estiver ativo, você verá `(.venv)` no início do prompt:

```
(.venv) PS C:\Users\...\headingPlace>
```

## Desativar

```powershell
deactivate
```

## Instalar dependências

Após ativar o ambiente virtual:

```powershell
pip install -r requirements.txt
```

