# backend/app/utils/formatter.py

import matplotlib.pyplot as plt
from io import BytesIO
import base64
import re
import json
import jsonschema


def format_table(data, headers):
    hdr = "| "+" | ".join(headers)+" |"
    sep = "| "+" | ".join(["---"]*len(headers))+" |"
    body = "\n".join(["| "+" | ".join(r)+" |" for r in data])
    return f"{hdr}\n{sep}\n{body}"


def to_latex(expr): return f"$$ {expr} $$"


def to_mermaid(steps: list[str], theme: str = "default") -> str:
    header = f"```mermaid\ntheme {theme}\nflowchart TD\n"
    body = "".join([f'  A{i}["{s}"] --> A{i+1}["{steps[i+1] if i+1<len(steps) else "End"}"]\n' for i,s in enumerate(steps)])
    return header + body + "```" 


def chart_to_base64(data: list[float]) -> str:
    plt.figure()
    plt.plot(data)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    return base64.b64encode(buf.getvalue()).decode()


def to_base64_image_tag(data: list[float]) -> str:
    b64 = chart_to_base64(data)
    return f"![chart](data:image/png;base64,{b64})"

def replace_footnotes(text: str) -> str:
    # [^1]: footnote text
    notes = re.findall(r'\[\^(\d+)\]:\s*(.*?)$', text, re.MULTILINE)
    for num, note in notes:
        text = text.replace(f'[^{num}]: {note}', f"<sup id='fnref{num}'><a href='#fn{num}'>[{num}]</a></sup>\n<div id='fn{num}' class='footnote'>{note}</div>")
    return text


def generate_toc(text: str) -> str:
    headers = re.findall(r"^(#{2,6})\\s*(.+)$", text, flags=re.MULTILINE)
    toc = "## Table of Contents\n"
    for lvl, title in headers:
        indent = "  " * (len(lvl)-2)
        anchor = title.strip().lower().replace(' ','-')
        toc += f"{indent}- [{title}](#{anchor})\n"
    return toc


def highlight_code_blocks(text: str) -> str:
    # اضافه کردن کلاس برای Prism.js
    return re.sub(r"```(\\w+)?\\n([\\s\\S]*?)```",
                  lambda m: f"<pre><code class='language-{m.group(1) or 'plaintext'}'>{m.group(2)}</code></pre>",
                  text)


def replace_admonitions(text: str) -> str:
    # تبدیل >>! note: … به بلوک admonition
    text = re.sub(r">>!\\s*(\\w+):([\\s\\S]*?)(?=\\n\\n|$)",
                  lambda m: f"```admonition\n{m.group(1).upper()}\n{m.group(2).strip()}\n```",
                  text)
    return text


def extract_and_validate_json(text: str) -> str:
    def _validate(m):
        block = m.group(1)
        try:
            data = json.loads(block)
            jsonschema.validate(instance=data, schema={"type": "object"})
            return f"```json\n{block}\n```"
        except Exception as e:
            return f"```text\nINVALID JSON: {e}\n{block}\n```"
    return re.sub(r"```json\n([\s\S]*?)\n```", lambda m: _validate(m), text)
