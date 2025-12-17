"""Teste do caminho AppData quando executado como .exe."""
import os
import sys
from pathlib import Path

# Simular modo executável
sys.frozen = True

# Importar após simular frozen
from app.utils.paths import get_project_root, ensure_directories

print("=" * 60)
print("TESTE DE CAMINHOS (Modo Executável Simulado)")
print("=" * 60)

root = get_project_root()
recordings_path, logs_path = ensure_directories()

print(f"Modo executável: {getattr(sys, 'frozen', False)}")
print(f"AppData: {Path(os.getenv('APPDATA', ''))}")
print(f"Diretório raiz: {root.absolute()}")
print(f"Gravações serão salvas em: {recordings_path.absolute()}")
print(f"Logs serão salvos em: {logs_path.absolute()}")
print("=" * 60)
print("✅ Pastas criadas com sucesso!")

