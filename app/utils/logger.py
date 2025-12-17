"""
Sistema de logging do aplicativo.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from app.config import LOG_LEVEL, LOG_FORMAT, LOGS_DIR
from app.utils.paths import get_project_root


def setup_logger(name: str = 'voice_recorder', no_console: bool = False) -> logging.Logger:
    """Configura e retorna um logger."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Evitar duplicação de handlers
    if logger.handlers:
        return logger
    
    # Handler para console (apenas se não estiver em modo sem console)
    if not no_console:
        try:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_formatter = logging.Formatter(LOG_FORMAT)
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
        except (OSError, AttributeError):
            # Se stdout não estiver disponível (modo noconsole), pular
            pass
    
    # Handler para arquivo (sempre)
    root = get_project_root()
    log_dir = root / LOGS_DIR
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / f"voice_recorder_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(file_formatter)
    
    logger.addHandler(file_handler)
    
    return logger

