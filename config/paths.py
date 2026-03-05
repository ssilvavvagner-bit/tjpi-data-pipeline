from pathlib import Path

# Diretório raiz do projeto
BASE_DIR = Path(__file__).resolve().parents[1]

# Pastas principais
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# Garantir que as pastas existem
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)