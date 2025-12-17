"""
Gravação de áudio em arquivos.
"""

import wave
from pathlib import Path
from typing import Optional
from app.config import SAMPLE_RATE, CHANNELS, FORMAT
from app.utils.logger import setup_logger
from app.utils.paths import get_recording_path

logger = setup_logger(__name__)


class AudioRecorder:
    """Classe para gravação de áudio em arquivos WAV."""
    
    def __init__(self):
        self.wav_file: Optional[wave.Wave_write] = None
        self.file_path: Optional[Path] = None
        self.is_recording = False
    
    def start_recording(self, filename: str):
        """
        Inicia a gravação em um arquivo.
        
        Args:
            filename: Nome do arquivo de saída
        """
        if self.is_recording:
            logger.warning("Gravação já está ativa")
            return
        
        try:
            self.file_path = get_recording_path(filename)
            
            # Garantir que o diretório existe
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            
            self.wav_file = wave.open(str(self.file_path), 'wb')
            self.wav_file.setnchannels(CHANNELS)
            self.wav_file.setsampwidth(2)  # 16-bit = 2 bytes
            self.wav_file.setframerate(SAMPLE_RATE)
            
            self.is_recording = True
            logger.info(f"Gravação iniciada: {self.file_path}")
            
        except Exception as e:
            logger.error(f"Erro ao iniciar gravação: {e}")
            raise
    
    def write_frame(self, audio_data: bytes):
        """
        Escreve um frame de áudio no arquivo.
        
        Args:
            audio_data: Dados de áudio em bytes
        """
        if not self.is_recording or self.wav_file is None:
            return
        
        try:
            self.wav_file.writeframes(audio_data)
        except Exception as e:
            logger.error(f"Erro ao escrever frame: {e}")
    
    def stop_recording(self) -> Optional[Path]:
        """
        Para a gravação e fecha o arquivo.
        
        Returns:
            Caminho do arquivo gravado ou None em caso de erro
        """
        if not self.is_recording:
            return None
        
        try:
            if self.wav_file:
                self.wav_file.close()
                self.wav_file = None
            
            self.is_recording = False
            file_path = self.file_path
            self.file_path = None
            
            if file_path and file_path.exists():
                file_size = file_path.stat().st_size
                logger.info(f"Gravação finalizada: {file_path} ({file_size} bytes)")
                return file_path
            else:
                logger.warning("Arquivo de gravação não encontrado")
                return None
                
        except Exception as e:
            logger.error(f"Erro ao parar gravação: {e}")
            return None

