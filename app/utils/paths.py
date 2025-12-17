"""
Gerenciamento de caminhos e diretórios.
"""

import os
import sys
from pathlib import Path
from app.config import RECORDINGS_DIR, LOGS_DIR


def get_project_root() -> Path:
    """Retorna o diretório raiz do projeto."""
    # Se estiver rodando como executável PyInstaller
    if getattr(sys, 'frozen', False):
        # sys.executable aponta para o .exe
        # O diretório do executável é onde queremos salvar os arquivos
        return Path(sys.executable).parent
    else:
        # Modo desenvolvimento: usar __file__
        return Path(__file__).parent.parent.parent


def ensure_directories():
    """Garante que os diretórios necessários existem."""
    root = get_project_root()
    
    recordings_path = root / RECORDINGS_DIR
    logs_path = root / LOGS_DIR
    
    recordings_path.mkdir(parents=True, exist_ok=True)
    logs_path.mkdir(parents=True, exist_ok=True)
    
    return recordings_path, logs_path


def get_recording_filename() -> str:
    """Gera um nome de arquivo único para a gravação."""
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"recording_{timestamp}.wav"
    return filename


def get_recording_path(filename: str) -> Path:
    """Retorna o caminho completo para um arquivo de gravação."""
    root = get_project_root()
    return root / RECORDINGS_DIR / filename

