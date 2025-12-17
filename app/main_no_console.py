"""
Ponto de entrada principal do aplicativo (modo sem console).
Sistema de gravação automática por detecção de voz.
"""

import signal
import sys
import os
from app.core.pipeline import AudioPipeline
from app.utils.logger import setup_logger

# Configurar para modo sem console
if sys.platform == 'win32':
    # Redirecionar stdout/stderr para evitar erros em modo noconsole
    try:
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
    except:
        pass

logger = setup_logger(__name__, no_console=True)


class VoiceRecorderApp:
    """Aplicativo principal de gravação por detecção de voz."""
    
    def __init__(self):
        self.pipeline = AudioPipeline()
        self.running = False
    
    def signal_handler(self, signum, frame):
        """Handler para sinais de interrupção."""
        logger.info("Sinal de interrupção recebido. Encerrando...")
        self.stop()
        sys.exit(0)
    
    def start(self):
        """Inicia o aplicativo."""
        try:
            # Registrar handlers de sinal (apenas se suportado)
            if hasattr(signal, 'SIGINT'):
                signal.signal(signal.SIGINT, self.signal_handler)
            if hasattr(signal, 'SIGTERM'):
                signal.signal(signal.SIGTERM, self.signal_handler)
            
            logger.info("=" * 60)
            logger.info("Sistema de Gravação por Detecção de Voz")
            logger.info("Modo: Sem Console (Background)")
            logger.info("=" * 60)
            logger.info("Estado inicial: MONITORING (aguardando voz)")
            logger.info("Logs salvos em: logs/")
            logger.info("Gravações salvas em: recordings/")
            logger.info("=" * 60)
            
            # Iniciar pipeline
            self.pipeline.start()
            self.running = True
            
            # Loop principal
            self.run()
            
        except KeyboardInterrupt:
            logger.info("Interrupção do usuário")
            self.stop()
        except Exception as e:
            logger.error(f"Erro fatal: {e}", exc_info=True)
            self.stop()
            sys.exit(1)
    
    def run(self):
        """Loop principal do aplicativo."""
        try:
            while self.running:
                # Manter o aplicativo rodando
                # O processamento acontece em threads separadas
                import time
                time.sleep(1)
                
                # Verificar se o pipeline ainda está rodando
                if not self.pipeline.is_running:
                    logger.warning("Pipeline parou inesperadamente. Reiniciando...")
                    try:
                        self.pipeline.cleanup()
                        self.pipeline = AudioPipeline()
                        self.pipeline.start()
                        logger.info("Pipeline reiniciado com sucesso")
                    except Exception as e:
                        logger.error(f"Erro ao reiniciar pipeline: {e}")
                        break
                    
        except Exception as e:
            logger.error(f"Erro no loop principal: {e}", exc_info=True)
            # Tentar reiniciar
            try:
                self.pipeline.cleanup()
                self.pipeline = AudioPipeline()
                self.pipeline.start()
                self.running = True
            except:
                raise
    
    def stop(self):
        """Para o aplicativo."""
        if not self.running:
            return
        
        logger.info("Encerrando aplicativo...")
        self.running = False
        self.pipeline.cleanup()
        logger.info("Aplicativo encerrado")


def main():
    """Função principal."""
    app = VoiceRecorderApp()
    app.start()


if __name__ == "__main__":
    main()

