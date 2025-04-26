import yaml
from pathlib import Path

# مسیر فایل پیکربندی در کانتینر
_CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.yaml"

# بارگذاری کانفیگ
def _load_config() -> dict:
    return yaml.safe_load(_CONFIG_PATH.read_text(encoding="utf-8"))

config = _load_config()

# Backend
BACKEND_HOST = config["backend"]["host"]
BACKEND_PORT = config["backend"]["port"]
FRONTEND_ORIGINS = config["backend"]["frontend_origins"]

# Vectorstore
DOCS_PATH = Path(config["vectorstore"]["docs_path"])
VECTORSTORE_PATH = Path(config["vectorstore"]["store_path"])
ALGOS_PATH = Path(config["vectorstore"]["algos_path"])

# Ollama
OLLAMA_URL = config["ollama"]["api_url"]
OLLAMA_MODEL = config["ollama"]["model"]

# Logging
LOGGING_LEVEL = config["logging"]["level"]
LOGGING_FORMAT = config["logging"]["format"]

# Custom Paths
SPACES_DIR = Path(config["paths"]["spaces_dir"])
MEDIA_DIR = Path(config["paths"]["media_dir"])