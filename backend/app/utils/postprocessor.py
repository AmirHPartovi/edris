import re
from app.utils.formatter import format_table, to_latex, to_mermaid


def post_process(text: str, original_prompt: str) -> str:
    """Post-process the model response"""
    try:
        # Preserve code blocks
        code_blocks = re.findall(r"```[\s\S]*?```", text)

        # Handle LaTeX expressions: wrap inline $...$
        text = re.sub(r"\[(.*?)\]latex:(.*?)\\n",
                      lambda m: to_latex(m.group(2)), text)

        # Handle tables: detect placeholder TABLE and replace
        if "[TABLE]" in text:
            table_data = [["Example", "Data"], [
                "Row1", "Value1"], ["Row2", "Value2"]]
            headers = ["Header1", "Header2"]
            formatted_table = format_table(table_data, headers)
            text = text.replace("[TABLE]", formatted_table)

        # Handle flowcharts: detect placeholder MERMAID and replace
        if "[MERMAID]" in text:
            steps = ["Start", "Process", "End"]
            mermaid_diagram = to_mermaid(steps)
            text = text.replace("[MERMAID]", mermaid_diagram)

        # Handle special formatting
        text = text.replace("[DONE]", "✅")
        text = text.replace("[ERROR]", "❌")

        # Reintegrate code blocks
        for block in code_blocks:
            text = text.replace(block, f"\n{block}\n")

        return text
    except Exception as e:
        print(f"Post-processing error: {e}")
        return text
