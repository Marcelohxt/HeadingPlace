"""
Configurações do sistema de gravação por detecção de voz.
"""

# Parâmetros de áudio
SAMPLE_RATE = 16000  # Taxa de amostragem (Hz) - requerido pelo WebRTC VAD
CHUNK_SIZE = 480  # Tamanho do chunk em frames (30ms a 16kHz)
CHANNELS = 1  # Mono
FORMAT = 'int16'  # Formato de áudio

# Parâmetros de VAD (Voice Activity Detection)
VAD_AGGRESSIVENESS = 2  # 0-3, onde 3 é mais agressivo
VAD_FRAME_DURATION_MS = 30  # Duração do frame em ms

# Parâmetros de gravação
#RECORDING_DURATION_SECONDS = 3600  # 1 hora em segundos
RECORDING_DURATION_SECONDS = 60   # 1 minuto (para teste rápido)
RECORDING_FORMAT = 'wav'  # Formato de saída

# Parâmetros de detecção
VOICE_DETECTION_THRESHOLD = 0.5  # Percentual de frames com voz para iniciar gravação
MIN_VOICE_FRAMES = 3  # Mínimo de frames consecutivos com voz para trigger

# Diretórios
RECORDINGS_DIR = 'recordings'
LOGS_DIR = 'logs'

# Configurações de logging
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

