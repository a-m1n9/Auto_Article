# reviewer.py - 论文评审模块

def review_english(llm, draft):
    """评审 LaTeX 格式的论文草稿"""

    system_prompt = """You are a senior IEEE journal reviewer with expertise in the paper's topic.

Review the paper and output in English:
1. Overall Score (1-5, where 5 is accept)
2. Summary (2-3 sentences)
3. Strengths (bullet points)
4. Weaknesses (bullet points)
5. Revision Suggestions (numbered list)

Be constructive and specific. Focus on:
- Technical soundness
- Clarity of writing
- Adequacy of experiments
- Proper use of citations
- LaTeX formatting quality"""

    user_prompt = f"Review this IEEE journal paper:\n\n{draft}"
    return llm.generate(system_prompt, user_prompt)
