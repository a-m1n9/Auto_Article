from openai import OpenAI
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, MODEL_NAME

class DeepSeekClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL
        )

    def chat(self, prompt, system_prompt="你是专业的学术论文助手，严格遵循要求，不编造内容"):
        """调用 DeepSeek V3.2 API"""
        try:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1  # 低温度，保证严谨性
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"API调用失败：{str(e)}"

# 全局实例
llm = DeepSeekClient()