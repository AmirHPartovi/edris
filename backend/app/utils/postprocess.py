# utils/postprocessor.py
import re
from utils.formatter import format_table, to_latex, to_mermaid


def post_process(text: str, original_prompt: str) -> str:
    # preserve code blocks
    code_blocks = re.findall(r"```[\s\S]*?```", text)
    # handle latex expressions: wrap inline $...$
    text = re.sub(r"\[(.*?)\]latex:(.*?)\\n",
                  lambda m: to_latex(m.group(2)), text)
    # handle tables: detect placeholder TABLE and replace
    # handle flowcharts: detect placeholder MERMAID and replace
    # reintegrate code blocks
    for cb in code_blocks:
        text = text.replace(cb, cb)
    return text
