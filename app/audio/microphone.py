"""
Captura de áudio do microfone.
"""

import pyaudio
from typing import Optional, Callable
from app.config import SAMPLE_RATE, CHUNK_SIZE, CHANNELS, FORMAT
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class Microphone:
    """Classe para captura de áudio do microfone."""
    
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream: Optional[pyaudio.Stream] = None
        self.is_streaming = False
        
    def start_stream(self, callback: Optional[Callable] = None):
        """Inicia o stream de áudio."""
        if self.is_streaming:
            logger.warning("Stream já está ativo")
            return
        
        try:
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=CHANNELS,
                rate=SAMPLE_RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE,
                stream_callback=callback
            )
            
            self.stream.start_stream()
            self.is_streaming = True
            logger.info("Stream de microfone iniciado")
            
        except Exception as e:
            logger.error(f"Erro ao iniciar stream: {e}")
            raise
    
    def stop_stream(self):
        """Para o stream de áudio."""
        if not self.is_streaming or self.stream is None:
            return
        
        try:
            self.stream.stop_stream()
            self.stream.close()
            self.is_streaming = False
            logger.info("Stream de microfone parado")
            
        except Exception as e:
            logger.error(f"Erro ao parar stream: {e}")
    
    def read_chunk(self) -> Optional[bytes]:
        """Lê um chunk de áudio do stream."""
        if not self.is_streaming or self.stream is None:
            return None
        
        try:
            data = self.stream.read(CHUNK_SIZE, exception_on_overflow=False)
            return data
        except Exception as e:
            logger.error(f"Erro ao ler chunk: {e}")
            return None
    
    def cleanup(self):
        """Libera recursos do microfone."""
        self.stop_stream()
        if self.audio:
            self.audio.terminate()
            logger.info("Recursos do microfone liberados")

