# 🚀 Guia Rápido de Teste e Build

## ✅ Checklist de Preparação

- [x] Ambiente virtual Python 3.11 criado e ativo
- [x] Script de teste criado (`test_program.py`)
- [x] Versão sem console criada (`app/main_no_console.py`)
- [x] Script de build atualizado (`build_exe.py`)
- [x] Instruções para notebook criadas

---

## 📝 Passo a Passo

### 1️⃣ Testar em Python (Desktop)

```powershell
# Certifique-se que o ambiente virtual está ativo
. .\.venv\Scripts\Activate.ps1

# Teste rápido (verifica componentes)
python test_quick.py

# Teste completo (valida funcionalidades)
python test_program.py

# Teste o programa completo (modo console)
python -m app.main
```

**O que validar:**
- ✅ Microfone lê áudio
- ✅ VAD detecta voz
- ✅ Gravação funciona
- ✅ Ciclo completo (MONITORING → RECORDING → MONITORING)

---

### 2️⃣ Instalar Dependências (se necessário)

```powershell
pip install -r requirements.txt
```

---

### 3️⃣ Criar Executável

```powershell
# Certifique-se que PyInstaller está instalado
pip install pyinstaller

# Criar executável
python build_exe.py
```

**Resultado:** `dist/voice_recorder.exe`

---

### 4️⃣ Testar Executável no Desktop

1. **Execute o .exe:**
   ```powershell
   .\dist\voice_recorder.exe
   ```

2. **Verifique:**
   - ❌ **NÃO deve abrir janela de console**
   - ✅ Deve aparecer no Gerenciador de Tarefas
   - ✅ Pasta `recordings/` deve ser criada
   - ✅ Pasta `logs/` deve ser criada

3. **Teste funcional:**
   - Fale algo para ativar gravação
   - Aguarde (pode configurar tempo menor para teste)
   - Verifique se arquivo foi salvo

4. **Encerrar:**
   - Gerenciador de Tarefas → Finalizar `voice_recorder.exe`

---

### 5️⃣ Copiar para Notebook

**Copie APENAS:**
```
dist/voice_recorder.exe
```

**Para o notebook** (qualquer local, ex: Desktop)

---

### 6️⃣ Configurar Notebook

#### A. Permissões de Microfone

1. Win+I → **Privacidade e Segurança** → **Microfone**
2. Ativar: **"Permitir que aplicativos de desktop acessem o microfone"**

#### B. Testar no Notebook

1. Execute `voice_recorder.exe`
2. Verifique no Gerenciador de Tarefas
3. Teste falando algo
4. Verifique pasta `recordings/`

#### C. Iniciar Automaticamente

1. **Win+R** → Digite: `shell:startup`
2. **Copie** `voice_recorder.exe` para essa pasta
3. Reinicie o notebook para testar

---

## 🔍 Verificações Finais

### No Desktop (antes de copiar):
- [ ] Executável não abre console
- [ ] Aparece no Gerenciador de Tarefas
- [ ] Detecta voz e grava
- [ ] Salva arquivos corretamente
- [ ] Retorna ao modo MONITORING

### No Notebook:
- [ ] Permissões de microfone habilitadas
- [ ] Executável roda sem console
- [ ] Detecta microfone do notebook
- [ ] Salva arquivos localmente
- [ ] Inicia automaticamente com Windows

---

## 📁 Estrutura de Arquivos

```
headingPlace/
├── dist/
│   └── voice_recorder.exe    ← COPIAR APENAS ESTE para notebook
├── recordings/               ← Criado automaticamente
├── logs/                     ← Criado automaticamente
└── ...
```

---

## ⚠️ Importante

- O executável cria `recordings/` e `logs/` no mesmo diretório onde está
- Cada gravação tem duração de **1 hora** (configurável em `app/config.py` antes do build)
- O programa roda **continuamente** até ser encerrado
- Para parar: Gerenciador de Tarefas → Finalizar processo

---

## 🆘 Troubleshooting

**Erro ao criar executável:**
- Verifique se todas as dependências estão instaladas
- Execute: `pip install -r requirements.txt`

**Executável não funciona:**
- Verifique logs em `logs/voice_recorder_YYYYMMDD.log`
- Teste primeiro em modo Python: `python -m app.main`

**Não detecta voz:**
- Ajuste `VAD_AGGRESSIVENESS` em `app/config.py` (antes do build)
- Verifique se o microfone está funcionando

