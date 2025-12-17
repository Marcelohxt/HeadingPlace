"""
Controle de tempo para gravações.
"""

import time
from app.config import RECORDING_DURATION_SECONDS
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class RecordingTimer:
    """Timer para controlar a duração da gravação."""
    
    def __init__(self, duration_seconds: int = RECORDING_DURATION_SECONDS):
        self.duration_seconds = duration_seconds
        self.start_time: float = 0.0
        self.is_running = False
    
    def start(self):
        """Inicia o timer."""
        self.start_time = time.time()
        self.is_running = True
        logger.info(f"Timer iniciado: {self.duration_seconds}s")
    
    def stop(self):
        """Para o timer."""
        self.is_running = False
        elapsed = time.time() - self.start_time if self.start_time > 0 else 0
        logger.info(f"Timer parado: {elapsed:.2f}s decorridos")
    
    def is_expired(self) -> bool:
        """
        Verifica se o tempo de gravação expirou.
        
        Returns:
            True se o tempo expirou, False caso contrário
        """
        if not self.is_running:
            return False
        
        elapsed = time.time() - self.start_time
        return elapsed >= self.duration_seconds
    
    def get_elapsed(self) -> float:
        """
        Retorna o tempo decorrido em segundos.
        
        Returns:
            Tempo decorrido em segundos
        """
        if not self.is_running:
            return 0.0
        
        return time.time() - self.start_time
    
    def get_remaining(self) -> float:
        """
        Retorna o tempo restante em segundos.
        
        Returns:
            Tempo restante em segundos
        """
        if not self.is_running:
            return 0.0
        
        elapsed = self.get_elapsed()
        remaining = self.duration_seconds - elapsed
        return max(0.0, remaining)

