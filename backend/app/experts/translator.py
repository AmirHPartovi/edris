# backend/app/experts/translator.py
import requests
import re
import detect


OLLAMA_API = "http://localhost:11434/api/generate"
P2E_MODEL = "Persian-to-English-Translation-mT5-V1-Q8_0-GGUF"
E2P_MODEL = "English-to-Persian-Translation-mT5-V1-Q8_0-GGUF"

__all__ = ["translate_persian_to_english", "translate_english_to_persian", "detect_language"]
# Translation functions
def translate_persian_to_english(text: str) -> str:
    """Translates Persian text to English using expert P2E function"""
    try:
        # Here you would call your actual P2E service/function
        # This is a placeholder - implement your actual translation method
        response = ollama.chat(model=P2E_MODEL, 
                              messages=[
                                  {"role": "system", "content": "You are an expert Persian to English translator. Translate the following Persian text to English."},
                                  {"role": "user", "content": text}
                              ])
        return response['message']['content']
    except Exception as e:
        logger.error(f"Translation P2E error: {str(e)}")
        # Return original text if translation fails
        return text

def translate_english_to_persian(text: str) -> str:
    """Translates English text to Persian using expert E2P function"""
    try:
        # Here you would call your actual E2P service/function
        # This is a placeholder - implement your actual translation method
        response = ollama.chat(model=E2P_MODEL, 
                              messages=[
                                  {"role": "system", "content": "You are an expert English to Persian translator. Translate the following English text to Persian."},
                                  {"role": "user", "content": text}
                              ])
        return response['message']['content']
    except Exception as e:
        logger.error(f"Translation E2P error: {str(e)}")
        # Return original text if translation fails
        return text

def detect_language(text: str) -> str:
    """Detect the language of input text"""
    try:
        # Persian language is detected as 'fa'
        lang = detect(text)
        return lang
    except:
        # Default to English if detection fails
        return "en"