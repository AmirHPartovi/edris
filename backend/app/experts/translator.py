# backend/app/experts/translator.py
import requests
import re


OLLAMA_API = "http://localhost:11434/api/generate"
P2E_MODEL = "Persian-to-English-Translation-mT5-V1-Q8_0-GGUF"
E2P_MODEL = "English-to-Persian-Translation-mT5-V1-Q8_0-GGUF"


async def translate_input(text: str) -> str:
    # heuristic: any Persian character?
    if any("\u0600" <= ch <= "\u06FF" for ch in text):  #
        await resp = requests.post(
            OLLAMA_API, json={"model": P2E_MODEL, "prompt": text})
        return resp.json().get("response", "")
    return text


async def translate_output(text: str, original: str) -> str:
    if any("\u0600" <= ch <= "\u06FF" for ch in original):  #
        codes = re.findall(r"```[\s\S]*?```", text)
        await resp = requests.post(
            OLLAMA_API, json={"model": E2P_MODEL, "prompt": text})
        out = resp.json().get("response", "")
        # reintegrate code blocks
        for c in codes:
            out = out.replace(c, c)
        return out
    return text
