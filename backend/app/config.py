import yaml
from pathlib import Path

# مسیر به ریشه پروژه
BASE_DIR = Path(__file__).resolve().parent.parent

# بارگذاری تنظیمات از config.yaml
with open(BASE_DIR / "config.yaml", encoding="utf-8") as f:
    _cfg = yaml.safe_load(f)

OLLAMA_API_URL = _cfg['ollama']['api_url']
EXPERTS_CONFIG = _cfg['experts']
BACKEND_PORT = _cfg['backend']['port']
FRONTEND_ORIGINS = _cfg['backend']['frontend_origins']
DOCS_PATH = BASE_DIR / _cfg['vectorstore']['docs_path']
STORE_PATH = BASE_DIR / _cfg['vectorstore']['store_path']
