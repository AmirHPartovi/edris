# experts/translator.py
import requests
import re

OLLAMA_API = "http://localhost:11434/api/generate"
P2E_MODEL = "pe2en"
E2P_MODEL = "en2pe"


def translate_input(text: str) -> str:
    try:
        if any("\u0600" <= ch <= "\u06FF" for ch in text):
            resp = requests.post(
                OLLAMA_API, json={"model": P2E_MODEL,
                                  "prompt": text, "stream": False}
            )
            resp.raise_for_status()
            return resp.json().get("response", text)
        return text
    except requests.exceptions.RequestException as e:
        print(f"Translation error: {e}")
        return text


def translate_output(text: str, original_prompt: str = "") -> str:
    try:
        if any("\u0600" <= ch <= "\u06FF" for ch in original_prompt):
            resp = requests.post(
                OLLAMA_API, json={"model": E2P_MODEL,
                                  "prompt": text, "stream": False}
            )
            resp.raise_for_status()
            return resp.json().get("response", text)
        return text
    except requests.exceptions.RequestException as e:
        print(f"Translation error: {e}")
        return text
