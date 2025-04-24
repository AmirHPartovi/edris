import re
from app.utils.formatter import format_table, to_latex, to_mermaid , to_base64_image_tag
from app.utils.formatter import chart_to_base64 ,highlight_code_blocks
from app.utils.formatter import replace_footnotes, generate_toc
from app.utils.formatter import replace_admonitions ,extract_and_validate_json


def post_process(text: str, original_prompt: str) -> str:
    try:
        text = highlight_code_blocks(text)
        text = replace_admonitions(text)
        text = extract_and_validate_json(text)
        text = replace_footnotes(text)
        # handle LaTeX
        text = re.sub(
            r"\[LATEX\](.*?)\[/LATEX\]",
            lambda m: to_latex(m.group(1)),
            text,
            flags=re.DOTALL
        )
        # handle TABLE
        if "[TABLE]" in text:
            # placeholder example, real data should be passed
            text = text.replace("[TABLE]", format_table(
                [["H1", "H2"], ["A", "B"]], ["H1", "H2"]))
        # handle MERMAID
        text = re.sub(
            r"\[MERMAID\](.*?)\[/MERMAID\]",
            lambda m: to_mermaid(m.group(1).split(";")),
            text,
            flags=re.DOTALL
        )
        return text
    except Exception as e:
        # fallback: return original text with error note
        return f"<div class='postprocess-error'>Error: {e}</div>\n" + text
