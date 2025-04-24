# experts/translator.py

import requests
from app.config import OLLAMA_API_URL, EXPERTS_CONFIG


class TranslatorExpert:
    """Handles translation tasks using Ollama API."""

    P2E_MODEL = EXPERTS_CONFIG['translator']['p2e_model']
    E2P_MODEL = EXPERTS_CONFIG['translator']['e2p_model']
    API = OLLAMA_API_URL

    def translate(self, text: str, model: str) -> str:
        resp = requests.post(
            self.API,
            json={"model": model, "prompt": text, "stream": False}
        )
        resp.raise_for_status()
        return resp.json().get("response", text)

    def translate_input(self, text: str) -> str:
        if any("\u0600" <= ch <= "\u06FF" for ch in text):
            return self.translate(text, self.P2E_MODEL)
        return text

    def translate_output(self, text: str, original_prompt: str = "") -> str:
        if any("\u0600" <= ch <= "\u06FF" for ch in original_prompt):
            return self.translate(text, self.E2P_MODEL)
        return text
