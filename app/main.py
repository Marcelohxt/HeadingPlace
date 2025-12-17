"""
Ponto de entrada principal do aplicativo.
Sistema de gravação automática por detecção de voz.
"""

import signal
import sys
from app.core.pipeline import AudioPipeline
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class VoiceRecorderApp:
    """Aplicativo principal de gravação por detecção de voz."""
    
    def __init__(self):
        self.pipeline = AudioPipeline()
        self.running = False
    
    def signal_handler(self, signum, frame):
        """Handler para sinais de interrupção (Ctrl+C)."""
        logger.info("Sinal de interrupção recebido. Encerrando...")
        self.stop()
        sys.exit(0)
    
    def start(self):
        """Inicia o aplicativo."""
        try:
            # Registrar handlers de sinal
            signal.signal(signal.SIGINT, self.signal_handler)
            signal.signal(signal.SIGTERM, self.signal_handler)
            
            logger.info("=" * 60)
            logger.info("Sistema de Gravação por Detecção de Voz")
            logger.info("=" * 60)
            logger.info("Estado inicial: MONITORING (aguardando voz)")
            logger.info("Pressione Ctrl+C para encerrar")
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
                    logger.warning("Pipeline parou inesperadamente")
                    break
                    
        except Exception as e:
            logger.error(f"Erro no loop principal: {e}")
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

