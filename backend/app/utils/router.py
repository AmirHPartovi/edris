# utils/router.py

from app.config import EXPERTS_CONFIG, DOCS_PATH, STORE_PATH
from typing import Optional

from app.knowledge.loader import search_knowledge


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
