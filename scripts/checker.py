# checker.py - 论文校验模块（适配 IEEE LaTeX 格式）

def check_paper(llm, draft, references):
    """校验并清理 LaTeX 论文内容"""

    system_prompt = """You are a strict academic proofreader specializing in IEEE journal papers.

The input is LaTeX-formatted paper content. Your job:
- Remove vague or unsupported sentences
- Check citation consistency: \\cite{ref1}, \\cite{ref2}, etc. should reference valid ref numbers
- Ensure LaTeX formatting is correct and complete
- Fix any broken LaTeX commands
- Do NOT add markdown formatting (no **, ##, * for emphasis)
- Preserve all valid LaTeX commands and environments
- Output ONLY cleaned LaTeX content, nothing else
- Do NOT wrap output in code blocks (no ```latex)
- Do NOT include abstract, keywords, bibliography, or document wrapper"""

    # 格式化参考文献供校验参考
    ref_text = ""
    if isinstance(references, list):
        for i, ref in enumerate(references):
            if isinstance(ref, dict):
                ref_text += f"[{i+1}] {ref.get('title', 'N/A')}. {ref.get('citation', '')} {ref.get('year', '')}\n"
            else:
                ref_text += f"[{i+1}] {ref}\n"
    elif isinstance(references, str):
        ref_text = references

    user_prompt = f"""Paper (LaTeX content):\n{draft}\n\nValid References (cite as \\cite{{ref1}}, \\cite{{ref2}}, etc.):\n{ref_text}\n\nOutput the cleaned LaTeX paper body only."""

    return llm.generate(system_prompt, user_prompt)
