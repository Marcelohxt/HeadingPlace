"""
Script para criar executável usando PyInstaller.
Execute: python build_exe.py
"""

import subprocess
import sys
import os
from pathlib import Path

def build_exe():
    """Cria o executável usando PyInstaller."""
    
    # Verificar se PyInstaller está instalado
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller não está instalado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Comando PyInstaller
    # Nota: PyInstaller inclui automaticamente módulos Python importados
    cmd = [
        "pyinstaller",
        "--onefile",                    # Arquivo único
        "--noconsole",                  # Sem janela de console
        "--name=voice_recorder",        # Nome do executável
        "--hidden-import=pyaudio",      # Import oculto necessário
        "--hidden-import=webrtcvad",    # Import oculto necessário
        "--hidden-import=numpy",        # Import oculto necessário
        "--hidden-import=wave",         # Import oculto necessário
        "--hidden-import=threading",    # Import oculto necessário
        "--hidden-import=queue",        # Import oculto necessário
        "--hidden-import=logging",      # Import oculto necessário
        "--hidden-import=app",           # Módulo principal
        "--hidden-import=app.audio",    # Módulos de áudio
        "--hidden-import=app.audio.microphone",
        "--hidden-import=app.audio.vad",
        "--hidden-import=app.audio.recorder",
        "--hidden-import=app.core",     # Módulos core
        "--hidden-import=app.core.pipeline",
        "--hidden-import=app.core.state_manager",
        "--hidden-import=app.core.timer",
        "--hidden-import=app.utils",    # Módulos utils
        "--hidden-import=app.utils.logger",
        "--hidden-import=app.utils.paths",
        "--collect-all=pyaudio",        # Coletar todos os dados do pyaudio
        "--collect-all=webrtcvad",      # Coletar todos os dados do webrtcvad
        "app/main_no_console.py"        # Ponto de entrada (modo sem console)
    ]
    
    print("=" * 60)
    print("Criando executável com PyInstaller...")
    print("=" * 60)
    print(f"Comando: {' '.join(cmd)}")
    print("=" * 60)
    print("\nIsso pode levar alguns minutos...\n")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        
        exe_path = Path("dist") / "voice_recorder.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print("\n" + "=" * 60)
            print("✅ Executável criado com sucesso!")
            print("=" * 60)
            print(f"📁 Localização: {exe_path.absolute()}")
            print(f"📦 Tamanho: {size_mb:.2f} MB")
            print("=" * 60)
        else:
            print("\n⚠️ Executável não encontrado em dist/")
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 60)
        print("❌ Erro ao criar executável")
        print("=" * 60)
        print(e.stderr)
        sys.exit(1)

if __name__ == "__main__":
    build_exe()

