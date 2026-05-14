# 读取 input/ 下的 docx 文件
import os
from docx import Document

def read_input_docx():
    input_dir = "input"
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        return ""
    
    for f in os.listdir(input_dir):
        if f.endswith(".docx"):
            doc = Document(os.path.join(input_dir, f))
            return "\n".join([p.text for p in doc.paragraphs])
    return ""