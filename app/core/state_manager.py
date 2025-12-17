"""
Gerenciador de estados do sistema.
"""

from enum import Enum
from typing import Optional
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class SystemState(Enum):
    """Estados do sistema."""
    MONITORING = "MONITORING"  # Escutando ambiente (VAD ativo)
    RECORDING = "RECORDING"    # Gravando áudio por tempo fixo (1h)


class StateManager:
    """Gerenciador de estados do sistema."""
    
    def __init__(self):
        self.current_state = SystemState.MONITORING
        self.state_history: list[tuple[SystemState, float]] = []
        logger.info(f"StateManager inicializado: estado {self.current_state.value}")
    
    def get_state(self) -> SystemState:
        """Retorna o estado atual."""
        return self.current_state
    
    def set_state(self, new_state: SystemState):
        """
        Altera o estado do sistema.
        
        Args:
            new_state: Novo estado
        """
        if new_state != self.current_state:
            old_state = self.current_state
            self.current_state = new_state
            logger.info(f"Estado alterado: {old_state.value} -> {new_state.value}")
    
    def is_monitoring(self) -> bool:
        """Verifica se está no estado MONITORING."""
        return self.current_state == SystemState.MONITORING
    
    def is_recording(self) -> bool:
        """Verifica se está no estado RECORDING."""
        return self.current_state == SystemState.RECORDING

