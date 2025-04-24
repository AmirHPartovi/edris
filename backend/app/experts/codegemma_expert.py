# backend/app/experts/codegemma_expert.py
import requests


class CodegemmaExpert:
    def run(self, prompt, context, **kwargs):
        full = f"# Context:\n{context}\n# Code request:\n{prompt}\n# Solution:"
        return requests.post("http://localhost:11434/api/generate", json={"model":"codegemma","prompt":full,**kwargs}).json().get("response","")