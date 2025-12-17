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
        # Usar AppData\Roaming para garantir permissões de escrita
        # Isso funciona mesmo quando executado da pasta Startup ou outras pastas protegidas
        appdata_path = Path(os.getenv('APPDATA', ''))
        if appdata_path:
            # Criar pasta específica do app em AppData
            app_folder = appdata_path / 'VoiceRecorder'
            return app_folder
        else:
            # Fallback: usar diretório do executável
            return Path(sys.executable).parent
    else:
        # Modo desenvolvimento: usar __file__
        return Path(__file__).parent.parent.parent


def ensure_directories():
    """Garante que os diretórios necessários existem."""
    root = get_project_root()
    
    recordings_path = root / RECORDINGS_DIR
    logs_path = root / LOGS_DIR
    
    try:
        recordings_path.mkdir(parents=True, exist_ok=True)
        logs_path.mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        # Se não conseguir criar, tentar diretório do usuário como fallback
        user_home = Path.home()
        fallback_path = user_home / 'VoiceRecorder'
        recordings_path = fallback_path / RECORDINGS_DIR
        logs_path = fallback_path / LOGS_DIR
        recordings_path.mkdir(parents=True, exist_ok=True)
        logs_path.mkdir(parents=True, exist_ok=True)
        root = fallback_path
        # Log do fallback (sem importar logger aqui para evitar circular)
        import logging
        logging.getLogger(__name__).warning(f"Usando fallback path: {fallback_path}")
    
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

