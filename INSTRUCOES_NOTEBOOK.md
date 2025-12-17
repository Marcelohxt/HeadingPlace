# 📋 Instruções para Notebook Externo

## 🧪 Passo 1: Testar no Desktop (Python)

Antes de criar o executável, vamos testar o programa:

```powershell
# Ativar ambiente virtual
. .\.venv\Scripts\Activate.ps1

# Instalar dependências (se ainda não instalou)
pip install -r requirements.txt

# Executar testes
python test_program.py

# Testar o programa completo
python -m app.main
```

**O que validar:**
- ✅ Microfone está sendo lido
- ✅ Detecção de voz funciona
- ✅ Gravação inicia ao detectar voz
- ✅ Grava por 1 hora (ou tempo configurado)
- ✅ Salva arquivo em `recordings/`
- ✅ Retorna ao modo MONITORING após gravação

---

## 🔨 Passo 2: Criar Executável

```powershell
# Certifique-se de que o ambiente virtual está ativo
. .\.venv\Scripts\Activate.ps1

# Instalar PyInstaller (se necessário)
pip install pyinstaller

# Criar executável
python build_exe.py
```

O executável será criado em: `dist/voice_recorder.exe`

---

## 🧪 Passo 3: Testar Executável no Desktop

1. **Teste sem console:**
   - Execute `dist/voice_recorder.exe`
   - Verifique que **NÃO abre janela de console**
   - O programa roda em segundo plano

2. **Verificar funcionamento:**
   - Abra o **Gerenciador de Tarefas** (Ctrl+Shift+Esc)
   - Procure por `voice_recorder.exe` nos processos
   - Verifique a pasta `recordings/` - arquivos devem aparecer após detecção de voz
   - Verifique a pasta `logs/` - logs devem ser gerados

3. **Teste completo:**
   - Fale algo para ativar a gravação
   - Aguarde 1 hora (ou tempo configurado)
   - Verifique se o arquivo foi salvo
   - Verifique se retornou ao modo de monitoramento

4. **Encerrar:**
   - Use o Gerenciador de Tarefas para finalizar o processo

---

## 📦 Passo 4: Copiar para Notebook

**Copie APENAS o arquivo executável:**

```
dist/voice_recorder.exe  →  Notebook (qualquer local)
```

**NÃO copie:**
- ❌ Pasta `app/`
- ❌ Arquivos `.py`
- ❌ Ambiente virtual `.venv/`
- ❌ Outros arquivos do projeto

---

## ⚙️ Passo 5: Configurar Notebook

### 5.1. Permissões de Microfone

1. Abra **Configurações** do Windows (Win+I)
2. Vá em **Privacidade e Segurança** → **Microfone**
3. Ative **"Permitir que aplicativos de desktop acessem o microfone"**
4. Role para baixo e certifique-se que está habilitado

### 5.2. Testar no Notebook

1. Execute `voice_recorder.exe` no notebook
2. Verifique no **Gerenciador de Tarefas** se está rodando
3. Fale algo para testar a detecção
4. Verifique se os arquivos estão sendo salvos

**Local dos arquivos no notebook:**
- Gravações: `C:\Users\[SEU_USUARIO]\Desktop\[PASTA_Onde_Está_o_EXE]\recordings\`
- Logs: `C:\Users\[SEU_USUARIO]\Desktop\[PASTA_Onde_Está_o_EXE]\logs\`

---

## 🚀 Passo 6: Iniciar Automaticamente com Windows

### Método 1: Pasta de Inicialização (Recomendado)

1. Pressione **Win+R**
2. Digite: `shell:startup`
3. Pressione Enter
4. A pasta de inicialização será aberta
5. **Copie o `voice_recorder.exe`** para essa pasta
   - Ou crie um **atalho** do executável e coloque o atalho

### Método 2: Usando o Registro do Windows (Avançado)

1. Pressione **Win+R**
2. Digite: `regedit`
3. Navegue até: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
4. Clique com botão direito → **Novo** → **Valor de String**
5. Nome: `VoiceRecorder`
6. Valor: Caminho completo do executável (ex: `C:\Users\...\voice_recorder.exe`)

---

## ✅ Passo 7: Verificar Funcionamento

### Verificar se está rodando:

1. **Gerenciador de Tarefas:**
   - Pressione **Ctrl+Shift+Esc**
   - Procure por `voice_recorder.exe`
   - Deve aparecer na lista de processos

2. **Pasta de gravações:**
   - Navegue até a pasta onde o `.exe` está
   - Abra a pasta `recordings/`
   - Arquivos `.wav` devem aparecer após cada gravação de 1 hora

3. **Logs:**
   - Abra a pasta `logs/`
   - Verifique o arquivo `voice_recorder_YYYYMMDD.log`
   - Deve conter informações sobre o funcionamento

### Comportamento Esperado:

- ✅ Inicia automaticamente ao ligar o notebook
- ✅ Roda em segundo plano (sem janela)
- ✅ Fica em modo MONITORING (aguardando voz)
- ✅ Ao detectar voz, inicia gravação de 1 hora
- ✅ Salva arquivo automaticamente
- ✅ Retorna ao modo MONITORING
- ✅ Repete o ciclo continuamente

---

## 🔧 Troubleshooting

### Executável não inicia:
- Verifique permissões de microfone
- Execute como Administrador (botão direito → Executar como administrador)
- Verifique logs em `logs/`

### Não detecta voz:
- Verifique se o microfone está funcionando
- Ajuste `VAD_AGGRESSIVENESS` em `app/config.py` (antes de criar o .exe)
- Verifique logs para erros

### Não salva arquivos:
- Verifique permissões de escrita na pasta
- Verifique se há espaço em disco
- Verifique logs para erros

### Parar o programa:
- Abra Gerenciador de Tarefas
- Encontre `voice_recorder.exe`
- Clique com botão direito → Finalizar tarefa

---

## 📝 Notas Importantes

- O executável cria as pastas `recordings/` e `logs/` automaticamente
- Os arquivos são salvos no mesmo diretório onde o `.exe` está
- O programa roda continuamente até ser encerrado manualmente
- Cada gravação tem duração fixa de 1 hora (configurável em `app/config.py`)

