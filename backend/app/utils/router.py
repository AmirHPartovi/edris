# utils/router.py

from app.config import DOCS_PATH, VECTORSTORE_PATH
from typing import Optional

from app.knowledge.loader import search_knowledge
import yaml
from pathlib import Path

# مسیر پایه پروژه
BASE_DIR = Path(__file__).resolve().parent.parent.parent


def load_config() -> dict:
    cfg = BASE_DIR / "config.yaml"
    if not cfg.exists():
        raise FileNotFoundError(f"Missing config file: {cfg}")
    return yaml.safe_load(cfg.read_text(encoding="utf-8"))


# بارگذاری تنظیمات
config = load_config()

# استخراج مسیرها از config
DOCS_PATH = Path(config['vectorstore']['docs_path'])
VECTORSTORE_PATH = Path(config['vectorstore']['store_path'])
# سایر تنظیمات...


def route_query(prompt: str, input_type: str = "text") -> str:
    """
    مسیر‌یابی پرسش به هر Expert
    واردسازی Lazy (درون تابع) برای جلوگیری از circular import
    """
    # مثال: اگر نیاز به Expert ترجمه بود
    if input_type == "translate":
        from app.experts.translator import TranslatorExpert
        expert = TranslatorExpert()
        return expert.translate_input(prompt)

    # بارگذاری دانش
    docs = search_knowledge(prompt, k=5)  # از ماژول مستقل loader
    context = "\n---\n".join(docs or [])

    # تصمیم‌گیری براساس کلیدواژه
    if any(kw in prompt.lower() for kw in ["code", "function", "algorithm"]):
        from app.experts.codegemma_expert import CodegemmaExpert
        return CodegemmaExpert().run(prompt, context)

    if input_type == "image":
        from app.experts.llava_expert import LlavaExpert
        return LlavaExpert().run(prompt, context)

    # پیش‌فرض Deepseek
    from app.experts.deepseek_expert import DeepseekExpert
    return DeepseekExpert().run(prompt, context)
