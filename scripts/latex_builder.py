# latex_builder.py - IEEE 模板 LaTeX 论文构建与 PDF 编译模块
import os
import re
import subprocess
from datetime import datetime

# IEEE 模板路径（相对于项目根目录 D:\Auto_Article）
IEEE_TEMPLATE_NAME = "bare_jrnl_new_sample4.tex"
IEEE_TEMPLATE_SUBDIR = "IEEE-Transactions-LaTeX2e-templates-and-instructions"

# pdflatex 路径（自动查找，或设置环境变量 PDFLATEX_PATH）
import shutil
PDFLATEX_PATH = os.environ.get("PDFLATEX_PATH", shutil.which("pdflatex") or "pdflatex")


def read_template_preamble(template_path):
    """从 IEEE 模板 .tex 文件中提取 preamble（\\begin{document} 之前的内容）"""
    with open(template_path, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r"(.*?)\\begin\{document\}", content, re.DOTALL)
    if match:
        preamble = match.group(1).strip()
    else:
        preamble = _fallback_preamble()

    return preamble


def _fallback_preamble():
    """标准 IEEEtran fallback preamble"""
    return r"""\documentclass[lettersize,journal]{IEEEtran}
\usepackage{amsmath,amsfonts}
\usepackage{algorithmic}
\usepackage{algorithm}
\usepackage{array}
\usepackage[caption=false,font=normalsize,labelfont=sf,textfont=sf]{subfig}
\usepackage{textcomp}
\usepackage{stfloats}
\usepackage{url}
\usepackage{verbatim}
\usepackage{graphicx}
\usepackage{cite}"""


def format_bibitem(ref, index):
    """将参考文献格式化为 IEEE \\bibitem 格式"""
    if isinstance(ref, dict):
        title = ref.get("title", "N/A")
        citation = ref.get("citation", "")
        year = ref.get("year", "")
        doi = ref.get("doi", "")
        return f"\\bibitem{{ref{index}}}\n{title}, {citation} {year}. DOI: {doi}\n"
    else:
        return f"\\bibitem{{ref{index}}}\n{ref}\n"


def build_ieee_tex(title, keywords, abstract, body_sections, references,
                   template_path=None, output_path="output/final_paper.tex",
                   author="Author Name"):
    """
    构建完整的 IEEE 期刊格式 .tex 文件，严格遵循 bare_jrnl_new_sample4.tex 模板结构。

    包含所有标准 IEEE 元素：
    - \\IEEEpubid 出版标识
    - \\markboth 页眉（含卷号/期号）
    - \\thanks{Manuscript received...} 收稿日期
    - \\IEEEpubidadjcol 列间距调整
    - \\begin{IEEEbiography} 作者简介
    """

    # 读取模板 preamble
    if template_path and os.path.exists(template_path):
        preamble = read_template_preamble(template_path)
        print(f"  Using IEEE template: {template_path}")
    else:
        preamble = _fallback_preamble()
        print("  WARNING: IEEE template not found, using fallback preamble")

    # 格式化关键词
    kw_str = ", ".join(keywords) if isinstance(keywords, list) else keywords

    # 构建参考文献
    if isinstance(references, list):
        bib_count = len(references)
        bib_items = ""
        for i, ref in enumerate(references):
            bib_items += format_bibitem(ref, i + 1) + "\n"
    else:
        bib_count = 1
        bib_items = f"\\bibitem{{ref1}}\n{references}\n"

    # 生成日期信息
    today = datetime.now()
    months = ["January","February","March","April","May","June",
              "July","August","September","October","November","December"]
    month_str = months[today.month - 1]
    year_str = str(today.year)
    vol = today.year - 2020
    month_num = today.month

    # 在正文第一栏中插入 \\IEEEpubidadjcol（需要在第一页第一栏出现）
    # 找到第一个 \\section 后的第一段，在其后插入
    body_with_adj = _insert_pubidadjcol(body_sections)

    # 提取作者姓氏（用于页眉）
    author_parts = author.replace(",", " ").split()
    last_name = author_parts[-1] if author_parts else "Author"
    # 取 title 前几个词用于页眉
    title_short = title.split(",")[0] if "," in title else title[:60]

    # 组装完整 .tex 文件（严格遵循 IEEE 模板结构）
    tex_content = f"""{preamble}

\\begin{{document}}

\\title{{{title}}}

\\author{{{author}}~%
\\thanks{{{author} is with the Department of Computer Science, University.}}% <-this % stops a space
\\thanks{{Manuscript received {month_str} {today.day}, {year_str}; revised {month_str} {today.day}, {year_str}.}}

% The paper headers
\\markboth{{Journal of \\LaTeX\\ Class Files,~Vol.~{vol}, No.~{month_num}, {month_str}~{year_str}}}%
{{{last_name} \\MakeLowercase{{\\textit{{et al.}}}}: {title_short}}}

\\IEEEpubid{{0000--0000/00\\$00.00~\\copyright~{year_str} IEEE}}
% Remember, if you use this you must call \\IEEEpubidadjcol in the second
% column for its text to clear the IEEEpubid mark.

\\maketitle

\\begin{{abstract}}
{abstract}
\\end{{abstract}}

\\begin{{IEEEkeywords}}
{kw_str}
\\end{{IEEEkeywords}}

{body_with_adj}

\\section*{{Acknowledgments}}
The authors would like to thank the reviewers for their valuable comments and suggestions.

\\begin{{thebibliography}}{{{bib_count}}}
\\bibliographystyle{{IEEEtran}}

{bib_items}
\\end{{thebibliography}}

\\section{{Biography Section}}
\\vspace{{11pt}}

\\begin{{IEEEbiographynophoto}}{{{author}}}
{author} received the degree. His/her current research interests include machine learning, artificial intelligence, and natural language processing.
\\end{{IEEEbiographynophoto}}

\\vfill

\\end{{document}}
"""

    # 写入文件
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(tex_content)

    print(f"  Saved: {output_path}")
    return output_path


def _insert_pubidadjcol(body):
    """
    在正文第一个 \\section 之后、第一栏内容中插入 \\IEEEpubidadjcol。
    这是 IEEE 模板要求的，用于清除 IEEEpubid 标记的列间距。
    """
    # 找到第一个 \section 后面的第一个段落结束处（第一个空行或第二个 \section 之前）
    # 简单策略：在第一个 \section 后的第3-5段文本后插入
    pattern = r"(\\section\{[^}]+\})"
    match = re.search(pattern, body)
    if not match:
        return body

    insert_pos = match.end()

    # 从第一个 section 开始，找到合适的位置插入（大约在第一栏的中后段）
    # 统计 section 后的段落数，在第3段附近插入
    remaining = body[insert_pos:]
    paragraphs = re.split(r"\n\s*\n", remaining)

    if len(paragraphs) >= 2:
        # 在第二段之后插入
        insert_text = paragraphs[0] + "\n\n" + paragraphs[1] + "\n\n\\IEEEpubidadjcol\n\n"
        rest = "\n\n".join(paragraphs[2:])
        return body[:insert_pos] + insert_text + rest
    else:
        # 内容不够长，直接在 section 后插入
        return body[:insert_pos] + "\n\n\\IEEEpubidadjcol\n\n" + remaining


def compile_pdf(tex_path, output_dir=None, pdflatex_path=None):
    """
    使用 pdflatex 编译 .tex 文件为 PDF。
    运行两次以正确解析交叉引用。
    """
    if pdflatex_path is None:
        pdflatex_path = PDFLATEX_PATH

    if output_dir is None:
        output_dir = os.path.dirname(tex_path) or "."

    pdf_path = os.path.join(output_dir, os.path.basename(tex_path).replace(".tex", ".pdf"))

    if not os.path.exists(pdflatex_path):
        return False, f"pdflatex not found at: {pdflatex_path}"

    # 运行两次以解决交叉引用
    for run in range(2):
        print(f"  pdflatex run {run + 1}/2 ...")
        try:
            result = subprocess.run(
                [pdflatex_path, "-interaction=nonstopmode",
                 "-output-directory", output_dir, tex_path],
                capture_output=True, text=True,
                encoding="utf-8", errors="replace",
                cwd=os.path.dirname(tex_path) or "."
            )
        except Exception as e:
            return False, f"pdflatex execution failed: {str(e)}"

    if os.path.exists(pdf_path):
        return True, pdf_path
    else:
        return False, "PDF was not generated. Check the .log file for errors."
