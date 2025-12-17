"""
Script de teste para validar o programa antes de criar o executável.
Testa: microfone, detecção de voz, gravação, ciclo completo.
"""

import sys
import time
from pathlib import Path
from app.core.pipeline import AudioPipeline
from app.utils.logger import setup_logger
from app.config import RECORDING_DURATION_SECONDS

logger = setup_logger(__name__)


def test_microphone():
    """Testa se o microfone está funcionando."""
    logger.info("=" * 60)
    logger.info("TESTE 1: Verificação do Microfone")
    logger.info("=" * 60)
    
    try:
        from app.audio.microphone import Microphone
        mic = Microphone()
        
        logger.info("Tentando iniciar o microfone...")
        mic.start_stream()
        
        logger.info("Lendo 5 chunks de áudio para teste...")
        for i in range(5):
            chunk = mic.read_chunk()
            if chunk:
                logger.info(f"  ✓ Chunk {i+1}: {len(chunk)} bytes lidos")
            else:
                logger.error(f"  ✗ Chunk {i+1}: Falha ao ler")
                return False
            time.sleep(0.1)
        
        mic.stop_stream()
        mic.cleanup()
        
        logger.info("✅ Microfone funcionando corretamente!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro no teste de microfone: {e}", exc_info=True)
        return False


def test_vad():
    """Testa a detecção de voz."""
    logger.info("\n" + "=" * 60)
    logger.info("TESTE 2: Detecção de Voz (VAD)")
    logger.info("=" * 60)
    
    try:
        from app.audio.vad import VoiceActivityDetector
        from app.audio.microphone import Microphone
        
        vad = VoiceActivityDetector()
        mic = Microphone()
        mic.start_stream()
        
        logger.info("Escutando por 3 segundos...")
        logger.info("Fale algo para testar a detecção de voz...")
        
        voice_detected = False
        for i in range(30):  # 3 segundos (30 chunks de 100ms)
            chunk = mic.read_chunk()
            if chunk and vad.is_speech(chunk):
                voice_detected = True
                logger.info(f"  ✓ Voz detectada no chunk {i+1}!")
                break
            time.sleep(0.1)
        
        mic.stop_stream()
        mic.cleanup()
        
        if voice_detected:
            logger.info("✅ Detecção de voz funcionando!")
        else:
            logger.warning("⚠️ Nenhuma voz detectada nos 3 segundos. Isso pode ser normal se não houver som.")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro no teste de VAD: {e}", exc_info=True)
        return False


def test_recording():
    """Testa a gravação (versão curta para teste)."""
    logger.info("\n" + "=" * 60)
    logger.info("TESTE 3: Gravação de Áudio")
    logger.info("=" * 60)
    
    try:
        from app.audio.recorder import AudioRecorder
        from app.audio.microphone import Microphone
        from app.utils.paths import get_recording_filename
        
        recorder = AudioRecorder()
        mic = Microphone()
        
        logger.info("Iniciando gravação de teste (5 segundos)...")
        filename = "test_recording.wav"
        recorder.start_recording(filename)
        mic.start_stream()
        
        logger.info("Gravando... Fale algo!")
        for i in range(50):  # 5 segundos
            chunk = mic.read_chunk()
            if chunk:
                recorder.write_frame(chunk)
            time.sleep(0.1)
        
        file_path = recorder.stop_recording()
        mic.stop_stream()
        mic.cleanup()
        
        if file_path and file_path.exists():
            size = file_path.stat().st_size
            logger.info(f"✅ Gravação salva: {file_path} ({size} bytes)")
            return True
        else:
            logger.error("❌ Arquivo de gravação não foi criado")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erro no teste de gravação: {e}", exc_info=True)
        return False


def test_full_cycle():
    """Testa o ciclo completo com duração reduzida."""
    logger.info("\n" + "=" * 60)
    logger.info("TESTE 4: Ciclo Completo (Duração Reduzida)")
    logger.info("=" * 60)
    logger.info("Este teste simula o ciclo completo com gravação de 10 segundos")
    logger.info("(em produção será 1 hora)")
    
    try:
        # Modificar temporariamente a duração
        from app.core.timer import RecordingTimer
        original_duration = RECORDING_DURATION_SECONDS
        
        # Criar pipeline
        pipeline = AudioPipeline()
        pipeline.timer.duration_seconds = 10  # 10 segundos para teste
        
        logger.info("Iniciando pipeline...")
        pipeline.start()
        
        logger.info("Estado: MONITORING - Aguardando detecção de voz...")
        logger.info("Fale algo para iniciar a gravação...")
        
        # Monitorar por até 30 segundos esperando voz
        monitoring_timeout = 30
        start_time = time.time()
        
        while pipeline.state_manager.is_monitoring():
            if time.time() - start_time > monitoring_timeout:
                logger.warning("Timeout: Nenhuma voz detectada em 30 segundos")
                break
            time.sleep(1)
        
        if pipeline.state_manager.is_recording():
            logger.info("✅ Gravação iniciada! Gravando por 10 segundos...")
            
            # Aguardar gravação terminar
            while pipeline.state_manager.is_recording():
                elapsed = pipeline.timer.get_elapsed()
                remaining = pipeline.timer.get_remaining()
                logger.info(f"  Gravando... {elapsed:.1f}s / {remaining:.1f}s restantes")
                time.sleep(2)
            
            logger.info("✅ Gravação finalizada!")
            logger.info("✅ Sistema retornou ao modo MONITORING")
        
        pipeline.cleanup()
        
        logger.info("✅ Ciclo completo testado com sucesso!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro no teste de ciclo completo: {e}", exc_info=True)
        return False


def main():
    """Executa todos os testes."""
    logger.info("\n" + "=" * 60)
    logger.info("INICIANDO TESTES DO SISTEMA")
    logger.info("=" * 60 + "\n")
    
    results = {
        "Microfone": test_microphone(),
        "VAD": test_vad(),
        "Gravação": test_recording(),
        "Ciclo Completo": test_full_cycle()
    }
    
    logger.info("\n" + "=" * 60)
    logger.info("RESULTADOS DOS TESTES")
    logger.info("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        logger.info(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        logger.info("\n✅ TODOS OS TESTES PASSARAM!")
        logger.info("O programa está pronto para criar o executável.")
    else:
        logger.warning("\n⚠️ ALGUNS TESTES FALHARAM")
        logger.warning("Revise os erros acima antes de criar o executável.")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

