# utils/formatter.py

def format_table(data: list[list[str]], headers: list[str]) -> str:
    header_row = "| " + " | ".join(headers) + " |"
    sep_row = "| " + " | ".join(["---"]*len(headers)) + " |"
    body = "\n".join(["| " + " | ".join(row) + " |" for row in data])
    return f"{header_row}\n{sep_row}\n{body}"


def to_latex(expr: str) -> str:
    return f"$$ {expr} $$"


def to_mermaid(steps: list[str]) -> str:
    diagram = "```mermaid\nflowchart TD\n"
    for i, s in enumerate(steps):
        diagram += f"  A{i}[\"{s}\"] --> A{i+1}[\"{steps[i+1] if i+1 < len(steps) else 'End'}\"]\n"
    diagram += "```"
    return diagram
