"""Teste rápido do caminho de gravações."""
import sys
from pathlib import Path
from app.utils.paths import get_project_root

root = get_project_root()
recordings_path = root / "recordings"

print("=" * 60)
print("TESTE DE CAMINHOS")
print("=" * 60)
print(f"Modo executável: {getattr(sys, 'frozen', False)}")
print(f"Diretório raiz: {root.absolute()}")
print(f"Gravações serão salvas em: {recordings_path.absolute()}")
print("=" * 60)

