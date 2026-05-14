# run_pipeline.py - IEEE 论文自动生成 Pipeline 主入口
import os
import yaml
import sys
import re

sys.path.append(os.path.dirname(__file__))

from doc_reader import read_input_docx
from qclaw_lite import QCLawLite
from llm_client import LLM
from writer import write_paper
from checker import check_paper
from reviewer import review_english
from latex_builder import build_ieee_tex, compile_pdf


def load_config():
    with open("config.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def clean_latex(text):
    """清理 LLM 输出中的 AI 格式残留符号"""
    # 移除 markdown 代码块标记
    text = re.sub(r"```latex\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    # markdown 加粗/斜体转 LaTeX
    text = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"\*([^*]+)\*", r"\\textit{\1}", text)
    # 移除 markdown 标题标记
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    # 移除游离的 * 和 #（非 LaTeX 命令部分）
    text = re.sub(r"(?<!\\)[*#](?![a-zA-Z])", "", text)
    return text.strip()


def extract_abstract(body):
    """从生成的正文中提取 abstract（如果 LLM 自带的话）"""
    match = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", body, re.DOTALL)
    if match:
        abstract = match.group(1).strip()
        body = body[:match.start()] + body[match.end():]
        return abstract, body
    return "", body


def generate_abstract(llm, title, body):
    """单独生成 IEEE 摘要（150-250 words）"""
    prompt = f"""Write a concise IEEE-style abstract (150-250 words) for this paper.

Topic: {title}

Paper body preview:
{body[:4000]}

Output ONLY the abstract text. No "Abstract:" label, no formatting, no LaTeX commands."""
    return llm.generate(
        "You write concise, professional IEEE journal abstracts.",
        prompt
    )


def main():
    print("========================================")
    print("  IEEE Journal Paper Generator (QCLaw)")
    print("========================================")

    cfg = load_config()

    # 切换到项目根目录
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    os.chdir(project_root)
    print(f"Project root: {project_root}")

    # 1. 读取输入文档
    input_text = read_input_docx()
    print("[1/6] Input DOCX loaded")

    # 2. 加载参考文献
    qclaw = QCLawLite()
    refs = qclaw.get_all_references(cfg["paper"]["keywords"])
    print(f"[2/6] Loaded {len(refs)} references")

    # 3. 初始化 LLM
    llm = LLM(cfg)
    draft = ""

    # 4. 迭代写作 + 校验 + 评审
    iterations = cfg["paper"].get("iterations", 1)
    for i in range(iterations):
        print(f"\n[3/6] Iteration {i + 1}/{iterations}")
        # 写作
        print("  Writing paper body...")
        draft = write_paper(llm, input_text, refs, cfg["paper"]["title"], cfg["paper"]["keywords"])
        draft = clean_latex(draft)
        # 校验
        print("  Checking paper...")
        draft = check_paper(llm, draft, refs)
        draft = clean_latex(draft)
        # 评审
        print("  Reviewing paper...")
        review = review_english(llm, draft)
        # 保存评审
        with open(f"output/review_{i + 1}.txt", "w", encoding="utf-8") as f:
            f.write(review)
        print(f"  Review saved: output/review_{i + 1}.txt")

    # 5. 构建 IEEE .tex 文件
    print("\n[4/6] Building IEEE LaTeX file...")

    # 提取或生成摘要
    abstract, body = extract_abstract(draft)
    if not abstract:
        print("  Generating abstract...")
        abstract = generate_abstract(llm, cfg["paper"]["title"], draft)

    # 准备参考文献列表
    ref_list = refs if isinstance(refs, list) else [refs]

    # 定位 IEEE 模板
    template_dir = cfg["paths"].get("template_dir", "latex_templates")
    template_path = os.path.join(
        template_dir,
        "IEEE-Transactions-LaTeX2e-templates-and-instructions",
        "bare_jrnl_new_sample4.tex"
    )

    # 获取作者信息
    author = cfg["paper"].get("author", "Author Name")

    # 构建 .tex
    tex_path = build_ieee_tex(
        title=cfg["paper"]["title"],
        keywords=cfg["paper"]["keywords"],
        abstract=abstract,
        body_sections=body,
        references=ref_list,
        template_path=template_path,
        output_path="output/final_paper.tex",
        author=author
    )

    # 保存 Markdown 备份
    md_content = f"# {cfg['paper']['title']}\n\n## Abstract\n{abstract}\n\n{body}"
    with open("output/final_paper.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    print("  Markdown backup saved: output/final_paper.md")

    # 6. 编译 PDF
    print("\n[5/6] Compiling PDF...")
    success, result = compile_pdf("output/final_paper.tex")
    if success:
        print(f"  PDF compiled successfully: {result}")
    else:
        print(f"  PDF compilation issue: {result}")
        print("  You can manually compile with pdflatex.")

    print("\n[6/6] Done!")
    print("========================================")
    print(f"  output/final_paper.tex  - IEEE LaTeX source")
    print(f"  output/final_paper.pdf  - compiled PDF")
    print(f"  output/final_paper.md   - Markdown backup")
    print(f"  output/review_*.txt     - review(s)")
    print("========================================")


if __name__ == "__main__":
    main()
