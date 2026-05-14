import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# DeepSeek API 配置（完全沿用你成功的格式）
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
MODEL_NAME = "deepseek-chat"

# 本地文件夹路径（自动创建）
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PAPER_FOLDER = os.path.join(BASE_DIR, "references")       # 参考文献（对应你原来的references文件夹）
TOP_CONF_FOLDER = os.path.join(BASE_DIR, "top_conferences")# 顶会文献
REVIEW_EXAMPLE_FOLDER = os.path.join(BASE_DIR, "review_examples") # 评审样例
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")           # 输出论文（对应你原来的output文件夹）
INPUT_FOLDER = os.path.join(BASE_DIR, "input")             # 输入文档（对应你原来的input文件夹）
TEMPLATE_FOLDER = os.path.join(BASE_DIR, "latex_templates")# LaTeX模板（对应你原来的latex_templates文件夹）

# 自动创建文件夹
for folder in [PAPER_FOLDER, TOP_CONF_FOLDER, REVIEW_EXAMPLE_FOLDER, OUTPUT_FOLDER, INPUT_FOLDER, TEMPLATE_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# 系统参数
MAX_ITERATION = 3  # 最大迭代修改次数
PASS_SCORE = 80    # 达标分数