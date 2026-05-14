# 完全按照你成功调用的 API 格式编写
from openai import OpenAI

class LLM:
    def __init__(self, cfg):
        # 这里严格使用你截图里成功的格式
        self.client = OpenAI(
            api_key=cfg["llm"]["api_key"],
            base_url=cfg["llm"]["base_url"]
        )
        self.model = cfg["llm"]["model"]

    def generate(self, system_prompt, user_prompt):
        # 全英文论文生成，温度 0.1 保证学术严谨
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1
        )
        return response.choices[0].message.content