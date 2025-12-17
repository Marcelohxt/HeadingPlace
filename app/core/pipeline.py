"""
Pipeline de processamento de áudio.
"""

import threading
from typing import Optional
from app.audio.microphone import Microphone
from app.audio.vad import VoiceActivityDetector
from app.audio.recorder import AudioRecorder
from app.core.state_manager import SystemState, StateManager
from app.core.timer import RecordingTimer
from app.config import MIN_VOICE_FRAMES, VOICE_DETECTION_THRESHOLD
from app.utils.logger import setup_logger
from app.utils.paths import get_recording_filename

logger = setup_logger(__name__)


class AudioPipeline:
    """Pipeline principal de processamento de áudio."""
    
    def __init__(self):
        self.microphone = Microphone()
        self.vad = VoiceActivityDetector()
        self.recorder = AudioRecorder()
        self.state_manager = StateManager()
        self.timer = RecordingTimer()
        
        self.processing_thread: Optional[threading.Thread] = None
        self.is_running = False
        
        # Buffer para detecção de voz
        self.voice_buffer: list[bytes] = []
        self.voice_frame_count = 0
    
    def _process_audio(self):
        """Thread de processamento de áudio."""
        logger.info("Thread de processamento iniciada")
        
        while self.is_running:
            try:
                # Ler frame de áudio diretamente do microfone
                audio_frame = self.microphone.read_chunk()
                
                if audio_frame is None:
                    continue
                
                state = self.state_manager.get_state()
                
                if state == SystemState.MONITORING:
                    self._handle_monitoring(audio_frame)
                elif state == SystemState.RECORDING:
                    self._handle_recording(audio_frame)
                    
            except Exception as e:
                logger.error(f"Erro no processamento de áudio: {e}")
                # Continuar processamento mesmo em caso de erro
                import time
                time.sleep(0.01)  # Pequena pausa para evitar loop infinito de erros
        
        logger.info("Thread de processamento finalizada")
    
    def _handle_monitoring(self, audio_frame: bytes):
        """Processa áudio no estado MONITORING."""
        # Verificar se há voz no frame
        if self.vad.is_speech(audio_frame):
            self.voice_frame_count += 1
            self.voice_buffer.append(audio_frame)
            
            # Se detectou voz suficiente, iniciar gravação
            if self.voice_frame_count >= MIN_VOICE_FRAMES:
                logger.info(f"Voz detectada! Iniciando gravação...")
                self._start_recording()
        else:
            # Resetar contador se não há voz
            if self.voice_frame_count > 0:
                self.voice_frame_count = 0
                self.voice_buffer.clear()
    
    def _handle_recording(self, audio_frame: bytes):
        """Processa áudio no estado RECORDING."""
        # Gravar frame
        self.recorder.write_frame(audio_frame)
        
        # Verificar se o tempo expirou
        if self.timer.is_expired():
            logger.info("Tempo de gravação expirado")
            self._stop_recording()
    
    def _start_recording(self):
        """Inicia uma nova gravação."""
        try:
            # Mudar para estado RECORDING
            self.state_manager.set_state(SystemState.RECORDING)
            
            # Gerar nome do arquivo
            filename = get_recording_filename()
            
            # Iniciar gravação
            self.recorder.start_recording(filename)
            
            # Iniciar timer
            self.timer.start()
            
            # Limpar buffer de voz
            self.voice_frame_count = 0
            self.voice_buffer.clear()
            
            logger.info(f"Gravação iniciada: {filename}")
            
        except Exception as e:
            logger.error(f"Erro ao iniciar gravação: {e}")
            # Retornar ao estado MONITORING em caso de erro
            self.state_manager.set_state(SystemState.MONITORING)
    
    def _stop_recording(self):
        """Para a gravação atual."""
        try:
            # Parar gravação
            file_path = self.recorder.stop_recording()
            
            # Parar timer
            self.timer.stop()
            
            # Retornar ao estado MONITORING
            self.state_manager.set_state(SystemState.MONITORING)
            
            logger.info("Sistema retornou ao modo de monitoramento")
            
        except Exception as e:
            logger.error(f"Erro ao parar gravação: {e}")
            self.state_manager.set_state(SystemState.MONITORING)
    
    def start(self):
        """Inicia o pipeline."""
        if self.is_running:
            logger.warning("Pipeline já está em execução")
            return
        
        try:
            # Garantir diretórios
            from app.utils.paths import ensure_directories
            ensure_directories()
            
            # Iniciar microfone (sem callback, leitura direta)
            self.microphone.start_stream()
            
            # Iniciar thread de processamento
            self.is_running = True
            self.processing_thread = threading.Thread(target=self._process_audio, daemon=True)
            self.processing_thread.start()
            
            logger.info("Pipeline iniciado")
            
        except Exception as e:
            logger.error(f"Erro ao iniciar pipeline: {e}")
            raise
    
    def stop(self):
        """Para o pipeline."""
        if not self.is_running:
            return
        
        try:
            # Parar processamento
            self.is_running = False
            
            # Se estiver gravando, parar gravação
            if self.state_manager.is_recording():
                self._stop_recording()
            
            # Aguardar thread finalizar
            if self.processing_thread:
                self.processing_thread.join(timeout=2.0)
            
            # Parar microfone
            self.microphone.stop_stream()
            
            logger.info("Pipeline parado")
            
        except Exception as e:
            logger.error(f"Erro ao parar pipeline: {e}")
    
    def cleanup(self):
        """Libera recursos."""
        self.stop()
        self.microphone.cleanup()
        logger.info("Recursos liberados")

