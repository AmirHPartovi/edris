import requests
from utils.router import OLLAMA_API_URL, EXPERTS_CONFIG


class TranslatorExpert:
    """Handles translation tasks using Ollama API."""

    P2E_MODEL = EXPERTS_CONFIG['translator']['p2e_model']
    E2P_MODEL = EXPERTS_CONFIG['translator']['e2p_model']
    API = OLLAMA_API_URL

    def translate(self, text: str, model: str) -> str:
        """Send a translation request to the Ollama API."""
        try:
            response = requests.post(
                self.API,
                json={"model": model, "prompt": text, "stream": False}
            )
            response.raise_for_status()
            return response.json().get("response", text)
        except requests.exceptions.RequestException as e:
            print(f"Translation error: {e}")
            return text

    def translate_input(self, text: str) -> str:
        """Translate Persian input to English if needed."""
        if any("\u0600" <= ch <= "\u06FF" for ch in text):  # Check for Persian characters
            return self.translate(text, self.P2E_MODEL)
        return text

    def translate_output(self, text: str, original_prompt: str = "") -> str:
        """Translate English output back to Persian if needed."""
        if any("\u0600" <= ch <= "\u06FF" for ch in original_prompt):  # Check for Persian characters
            return self.translate(text, self.E2P_MODEL)
        return text
