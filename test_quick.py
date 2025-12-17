"""
Teste rápido - apenas verifica se os componentes básicos funcionam.
"""

import sys
import time

print("=" * 60)
print("TESTE RÁPIDO DO SISTEMA")
print("=" * 60)

# Teste 1: Importações
print("\n1. Testando importações...")
try:
    from app.audio.microphone import Microphone
    from app.audio.vad import VoiceActivityDetector
    from app.audio.recorder import AudioRecorder
    from app.core.pipeline import AudioPipeline
    print("   ✅ Todas as importações funcionaram")
except Exception as e:
    print(f"   ❌ Erro nas importações: {e}")
    sys.exit(1)

# Teste 2: Microfone
print("\n2. Testando microfone...")
try:
    mic = Microphone()
    mic.start_stream()
    chunk = mic.read_chunk()
    if chunk:
        print(f"   ✅ Microfone funcionando ({len(chunk)} bytes lidos)")
    else:
        print("   ⚠️ Microfone não retornou dados")
    mic.stop_stream()
    mic.cleanup()
except Exception as e:
    print(f"   ❌ Erro no microfone: {e}")

# Teste 3: VAD
print("\n3. Testando detecção de voz (VAD)...")
try:
    vad = VoiceActivityDetector()
    print("   ✅ VAD inicializado")
except Exception as e:
    print(f"   ❌ Erro no VAD: {e}")

# Teste 4: Recorder
print("\n4. Testando gravador...")
try:
    recorder = AudioRecorder()
    print("   ✅ Gravador inicializado")
except Exception as e:
    print(f"   ❌ Erro no gravador: {e}")

# Teste 5: Pipeline
print("\n5. Testando pipeline...")
try:
    pipeline = AudioPipeline()
    print("   ✅ Pipeline inicializado")
    print("   Estado inicial:", pipeline.state_manager.get_state().value)
except Exception as e:
    print(f"   ❌ Erro no pipeline: {e}")

print("\n" + "=" * 60)
print("TESTE RÁPIDO CONCLUÍDO")
print("=" * 60)
print("\nPara teste completo, execute: python test_program.py")

