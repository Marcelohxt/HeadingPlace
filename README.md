# 🎤 Voice Trigger Recorder

Sistema de gravação automática por detecção de voz para Windows.

## 📌 Objetivo

Criar um executável para Windows que:

- ✅ Escuta continuamente o microfone
- ✅ Detecta presença de voz humana (VAD)
- ✅ Inicia gravação automática ao detectar voz
- ✅ Grava por exatamente 1 hora
- ✅ Salva o áudio localmente
- ✅ Retorna ao modo de escuta após finalizar
- ✅ Opera de forma contínua e automática

## 🧠 Conceito Central

Sistema baseado em estados:

- **MONITORING** → escutando ambiente (VAD ativo)
- **RECORDING** → gravando áudio por tempo fixo (1h)

## 🗂️ Estrutura do Projeto

```
voice-trigger-recorder/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── app/
│   ├── main.py                # Ponto de entrada
│   ├── config.py              # Parâmetros do sistema
│   ├── audio/
│   │   ├── microphone.py      # Captura de áudio
│   │   ├── vad.py             # Detecção de voz
│   │   └── recorder.py        # Gravação de arquivos
│   │
│   ├── core/
│   │   ├── state_manager.py   # Controle de estados
│   │   ├── timer.py           # Controle de tempo (1h)
│   │   └── pipeline.py        # Fila e fluxo de áudio
│   │
│   └── utils/
│       ├── logger.py          # Logs do sistema
│       └── paths.py           # Diretórios e arquivos
│
├── recordings/                # Arquivos gerados
│
└── build/
    └── exe/                   # Executável final
```

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Windows 10/11
- Microfone configurado

### Instalação das Dependências

```bash
pip install -r requirements.txt
```

**Nota:** No Windows, pode ser necessário instalar o PyAudio manualmente:

```bash
pip install pipwin
pipwin install pyaudio
```

Ou baixar o wheel apropriado de: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

## 💻 Uso

### Executar o Script

```bash
python -m app.main
```

### Comportamento

1. O sistema inicia em modo **MONITORING**
2. Escuta continuamente o microfone
3. Ao detectar voz, muda para **RECORDING**
4. Grava por exatamente 1 hora
5. Salva o arquivo em `recordings/recording_YYYYMMDD_HHMMSS.wav`
6. Retorna automaticamente para **MONITORING**
7. Repete o ciclo indefinidamente

### Encerrar

Pressione `Ctrl+C` para encerrar o aplicativo graciosamente.

## ⚙️ Configuração

Edite `app/config.py` para ajustar:

- `SAMPLE_RATE`: Taxa de amostragem (padrão: 16000 Hz)
- `VAD_AGGRESSIVENESS`: Sensibilidade do VAD (0-3, padrão: 2)
- `RECORDING_DURATION_SECONDS`: Duração da gravação (padrão: 3600s = 1h)
- `MIN_VOICE_FRAMES`: Frames mínimos de voz para trigger (padrão: 3)

## 📦 Criar Executável

### Usando PyInstaller

```bash
pip install pyinstaller

pyinstaller --onefile --windowed --name voice_recorder app/main.py
```

O executável será gerado em `dist/voice_recorder.exe`

### Usando cx_Freeze

```bash
pip install cx_Freeze
```

Crie um arquivo `setup.py`:

```python
from cx_Freeze import setup, Executable

setup(
    name="Voice Recorder",
    version="1.0",
    description="Sistema de gravação por detecção de voz",
    executables=[Executable("app/main.py", base="Win32GUI")]
)
```

Execute:

```bash
python setup.py build
```

## 📝 Logs

Os logs são salvos em:
- Console (nível INFO)
- Arquivo: `logs/voice_recorder_YYYYMMDD.log` (nível DEBUG)

## 🔧 Troubleshooting

### Erro ao instalar PyAudio

No Windows, use:
```bash
pip install pipwin
pipwin install pyaudio
```

### Microfone não detectado

Verifique:
1. Permissões do Windows para acesso ao microfone
2. Dispositivo padrão configurado corretamente
3. Drivers do microfone atualizados

### VAD não detecta voz

Ajuste em `config.py`:
- Aumente `VAD_AGGRESSIVENESS` (0-3)
- Diminua `MIN_VOICE_FRAMES`

## 📄 Licença

Este projeto é fornecido como está, sem garantias.

## 👤 Autor

Desenvolvido para gravação automática por detecção de voz.

