"""
Detecção de atividade de voz (Voice Activity Detection).
"""

import webrtcvad
from typing import Optional
from app.config import SAMPLE_RATE, VAD_AGGRESSIVENESS, VAD_FRAME_DURATION_MS
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class VoiceActivityDetector:
    """Detector de atividade de voz usando WebRTC VAD."""
    
    def __init__(self):
        try:
            self.vad = webrtcvad.Vad(VAD_AGGRESSIVENESS)
            logger.info(f"VAD inicializado com agressividade {VAD_AGGRESSIVENESS}")
        except Exception as e:
            logger.error(f"Erro ao inicializar VAD: {e}")
            raise
    
    def is_speech(self, audio_frame: bytes) -> bool:
        """
        Verifica se um frame de áudio contém voz.
        
        Args:
            audio_frame: Frame de áudio em bytes (deve ter tamanho correto)
            
        Returns:
            True se detectar voz, False caso contrário
        """
        try:
            # WebRTC VAD requer frames de 10ms, 20ms ou 30ms
            # Para 16kHz: 10ms=160, 20ms=320, 30ms=480 samples
            frame_size = len(audio_frame) // 2  # 2 bytes por sample (int16)
            
            if frame_size not in [160, 320, 480]:
                # Se o frame não tem tamanho compatível, dividir em chunks de 30ms
                if frame_size >= 480:
                    # Dividir em chunks de 480 samples (30ms)
                    chunk_size = 480 * 2  # 2 bytes por sample
                    for i in range(0, len(audio_frame), chunk_size):
                        chunk = audio_frame[i:i+chunk_size]
                        if len(chunk) == chunk_size:
                            if self.vad.is_speech(chunk, SAMPLE_RATE):
                                return True
                    return False
                else:
                    # Frame muito pequeno, não pode processar
                    return False
            
            return self.vad.is_speech(audio_frame, SAMPLE_RATE)
            
        except Exception as e:
            logger.debug(f"Erro ao processar frame VAD: {e}")
            return False
    
    def has_voice_activity(self, audio_frames: list[bytes], threshold: float = 0.5) -> bool:
        """
        Verifica se há atividade de voz em uma sequência de frames.
        
        Args:
            audio_frames: Lista de frames de áudio
            threshold: Percentual mínimo de frames com voz (0.0 a 1.0)
            
        Returns:
            True se a porcentagem de frames com voz for >= threshold
        """
        if not audio_frames:
            return False
        
        speech_frames = sum(1 for frame in audio_frames if self.is_speech(frame))
        voice_ratio = speech_frames / len(audio_frames)
        
        return voice_ratio >= threshold

