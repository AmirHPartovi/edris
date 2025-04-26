# backend/app/utils/config.py

import yaml
from pathlib import Path

# مسیر فایل پیکربندی در کانتینر
_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.yaml"

def _load_config() -> dict:
    text = _CONFIG_PATH.read_text(encoding="utf-8")
    return yaml.safe_load(text)

# بارگذاری یک‌باره‌ی کانفیگ
config = _load_config()

# مقادیر کلیدی
BACKEND_HOST = config["backend"]["host"]
BACKEND_PORT = config["backend"]["port"]
FRONTEND_ORIGINS = config["backend"]["frontend_origins"]

DOCS_PATH = Path(config["vectorstore"]["docs_path"])
VECTORSTORE_PATH = Path(config["vectorstore"]["store_path"])

OLLAMA_URL = config["ollama"]["api_url"]
OLLAMA_MODEL = config["ollama"]["model"]

LOGGING_LEVEL = config["logging"]["level"]
LOGGING_FORMAT = config["logging"]["format"]
