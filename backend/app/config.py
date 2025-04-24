import yaml
from pathlib import Path

# Define shared paths
BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_PATH = BASE_DIR / "app/knowledge/docs"
VECTORSTORE_PATH = BASE_DIR / "app/knowledge/vectorstore"

# بارگذاری تنظیمات از config.yaml
with open(BASE_DIR / "config.yaml", encoding="utf-8") as f:
    _cfg = yaml.safe_load(f)

OLLAMA_API_URL = _cfg['ollama']['api_url']
EXPERTS_CONFIG = _cfg['experts']
BACKEND_PORT = _cfg['backend']['port']
FRONTEND_ORIGINS = _cfg['backend']['frontend_origins']
