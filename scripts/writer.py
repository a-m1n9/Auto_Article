# writer.py - IEEE LaTeX 格式论文写作模块
# 输出纯 LaTeX 内容，不再输出 Markdown

def write_paper(llm, input_content, references, topic, keywords):
    """让 LLM 生成 IEEE 格式的 LaTeX 论文正文（不含 document wrapper）"""

    system_prompt = """You are a top-tier IEEE journal paper writer. Write ONLY in fluent, academic, formal English.

OUTPUT FORMAT REQUIREMENTS (STRICT):
1. Output PURE LaTeX content. NO markdown, NO code fences (no ```latex or ```), NO backticks.
2. Use IEEE-style sectioning: \\section{...}, \\subsection{...}
3. For the first section paragraph, you MAY use \\IEEEPARstart{F}{irst} for drop-cap style.
4. Use proper LaTeX math: $...$ for inline, \\begin{equation}...\\end{equation} for display math.
5. Use \\cite{ref1}, \\cite{ref1,ref2} for citations. The reference keys are ref1, ref2, etc.
6. Use proper LaTeX formatting ONLY: \\textbf{} for bold, \\textit{} for italic. NO markdown ** or ##.
7. Paper structure: Introduction, Related Work, Methodology, Experiments, Conclusion.
8. Do NOT include \\begin{document}, \\end{document}, \\title, \\author, \\maketitle.
9. Do NOT include \\begin{abstract}...\\end{abstract} or \\begin{IEEEkeywords}...\\end{IEEEkeywords} (handled separately).
10. Do NOT include bibliography section — only use \\cite{} commands in the text.
11. Do NOT include any * or # characters for formatting.
12. Do NOT wrap output in code blocks.
"""

    # 格式化参考文献列表供 LLM 参考
    ref_text = ""
    if isinstance(references, list):
        for i, ref in enumerate(references):
            if isinstance(ref, dict):
                ref_text += f"[{i+1}] {ref.get('title', 'N/A')}. {ref.get('citation', '')} {ref.get('year', '')}. DOI: {ref.get('doi', 'N/A')}\n"
            else:
                ref_text += f"[{i+1}] {ref}\n"
    elif isinstance(references, str):
        ref_text = references

    user_prompt = f"""Topic: {topic}
Keywords: {', '.join(keywords) if isinstance(keywords, list) else keywords}

Input Document Content (use this as reference material):
{input_content[:5000]}

Available References (cite using \\cite{{ref1}}, \\cite{{ref2}}, etc.):
{ref_text}

Write the COMPLETE paper body in IEEE LaTeX format.
Output ONLY LaTeX body content (sections, text, equations) — no document wrapper, no abstract, no keywords, no bibliography."""

    return llm.generate(system_prompt, user_prompt)
