---
name: auto-article-pipeline
description: |
  自动运行项目，执行 scripts/run_pipeline.py 生成英文论文。
  实时向用户报告运行进度，运行完成后清理格式符号、编译 LaTeX 生成 PDF、打开 PDF 和评审意见。
  使用场景：
  (1) 用户说"运行项目"、"生成论文"、"执行 pipeline"时触发
  (2) 需要自动执行自动化论文生成流程时
---

# Auto Article Pipeline Skill

## 项目结构

```
.
├── scripts/          # 脚本目录
│   └── run_pipeline.py  # 主入口
├── input/           # 输入 DOCX 文件
├── output/          # 输出结果
├── latex_templates/
├── references/
├── config.yaml      # 配置文件
└── .env.example     # 环境变量示例
```

## 配置说明

编辑 `config.yaml` 可调整：

```yaml
paper:
  title: "论文标题"
  keywords: ["关键词1", "关键词2"]
  iterations: 3  # 迭代次数
```

## 输入输出

- **输入**: 将 DOCX 文件放入 `input/` 目录
- **输出**:
  - `output/final_paper.md` - 最终论文
  - `output/final_paper.tex` - LaTeX 源码
  - `output/final_paper.pdf` - 生成的 PDF
  - `output/review_*.txt` - 每次迭代的评审

## 完整执行流程

### 1. 运行 Pipeline（实时报告进度）

```powershell
$env:PYTHONIOENCODING="utf-8"; python -u scripts/run_pipeline.py 2>&1
```

使用 `exec` + `process` 实时获取输出，向用户报告进度。

### 2. 清理格式符号（星号和井号）

**必须清理所有三类文件：`.md`、`.tex`、以及 `review_*.txt`。**

> ⚠️ 重要：pipeline 生成的 `.tex` 文件同样包含星号和井号，只清理 `.md` 是不够的。

```powershell
# 清理 final_paper.md
$content = Get-Content "output/final_paper.md" -Raw
$content = $content -replace '[*#]', ''
$content | Set-Content "output/final_paper.md" -Encoding UTF8

# 清理 final_paper.tex（必须！否则 PDF 编译后仍有星号）
$content = Get-Content "output/final_paper.tex" -Raw
$content = $content -replace '[*#]', ''
$content | Set-Content "output/final_paper.tex" -Encoding UTF8

# 清理所有 review_*.txt
Get-ChildItem "output/review_*.txt" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $content = $content -replace '[*#]', ''
    $content | Set-Content $_.FullName -Encoding UTF8
}
```

### 3. 修复 .tex 文件中的特殊 Unicode 字符

> ⚠️ pipeline 生成的 `.tex` 文件中，em-dash (`---`) 有时被错误编码为 CJK 扩展区字符（如 `鈥攕`、`鈥攚`、`鈥攁`、`鈥攆`、`鈥斺`），直接编译会导致 LaTeX 报错。**必须先替换，再编译。**

```powershell
$content = Get-Content "output/final_paper.tex" -Raw
$content = $content -replace '鈥攕', '---'
$content = $content -replace '鈥攚', '---'
$content = $content -replace '鈥攁', '---'
$content = $content -replace '鈥攆', '---'
$content = $content -replace '鈥斺', '---'
$content | Set-Content "output/final_paper.tex" -Encoding UTF8
```

### 4. 编译 LaTeX 生成 PDF

> ⚠️ 注意：pipeline 有时会输出"LaTeX 未安装或模板异常，跳过PDF生成"，这不代表不需要编译。
> **无论 pipeline 是否生成 PDF，都应手动执行以下命令尝试编译。**

```powershell
pdflatex -interaction=nonstopmode "output/final_paper.tex" 2>&1
```

### 5. 打开结果文件

```powershell
# 打开 PDF
Start-Process "output/final_paper.pdf"

# 打开 Markdown 论文
Start-Process "output/final_paper.md"

# 打开所有评审意见
Get-ChildItem "output/review_*.txt" | ForEach-Object { Start-Process $_.FullName }
```

### 6. 向用户报告结果

展示论文标题和摘要。

---

## 工作流总结

```
用户说"生成论文"
    ↓
1. 运行 run_pipeline.py（实时报告进度）
    ↓
2. 清理所有文件中的 * 和 # 符号（.md + .tex + review_*.txt）
    ↓
3. 修复 .tex 中的特殊 Unicode 字符（鈥攕/鈥攚/鈥攁/鈥攆/鈥斺 → ---）
    ↓
4. 手动执行 pdflatex 编译（无论 pipeline 是否跳过）
    ↓
5. 打开 final_paper.pdf
    ↓
6. 打开 final_paper.md
    ↓
7. 打开所有 review_*.txt 评审意见
    ↓
8. 展示论文摘要给用户
```
