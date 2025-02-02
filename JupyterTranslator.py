import json
import os
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI

class JupyterTranslator:
    def __init__(self, origin_language, target_language, model_name):
        self.origin_language = origin_language
        self.target_language = target_language
        self.model_name = model_name
        self.notebook = None

    def read_ipynb(self, input_file_path):
        with open(input_file_path, 'r', encoding='utf-8') as f:
            self.notebook = json.load(f)

    def translate(self):
        if not self.notebook:
            raise ValueError("Notebook content is empty. Please run read_ipynb() first.")

        cells = self.notebook.get("cells", [])
        tasks = []

        with ThreadPoolExecutor(max_workers=50) as executor:
            for cell in cells:
                if cell.get("cell_type") == "markdown":
                    original_source = cell.get("source", "")
                    # 如果 source 为列表，则先合并为字符串
                    if isinstance(original_source, list):
                        text_to_translate = "".join(original_source)
                    else:
                        text_to_translate = original_source

                    future = executor.submit(
                        self.call_api_qwen,
                        text_to_translate,
                        self.origin_language,
                        self.target_language,
                        self.model_name
                    )
                    tasks.append((future, cell))

            for future, cell in tasks:
                translated_text = future.result()
                if isinstance(cell.get("source"), list):
                    cell['source'] = translated_text.splitlines(keepends=True)
                else:
                    cell['source'] = translated_text

    def generate_ipynb(self, output_file_path):
        if not self.notebook:
            raise ValueError("Notebook content is empty. Please run read_ipynb() and translate() first.")

        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.notebook, f, ensure_ascii=False, indent=1)

    def call_api_qwen(self, text, origin_language, target_language, model_name):
        client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

        prompt = (
            f"Please provide a proficient and precise translation from {origin_language} to {target_language}. "
            f"You should use artificial intelligence tools, such as natural language processing, "
            f"and rhetorical knowledge and experience about effective writing techniques to reply. "
            f"Make the reply looks like a native speaker. "
            f"Some specific terms such as name do not need to be translated. "
            f"The text is as follows: "
            f"\n\n{text}\n\n"
            f"Please provide the translated result without any additional explanation and remove. "
            f"If translation is unnecessary (e.g. proper nouns, codes, etc.), "
            f"return the original text. NO explanations. NO notes. "
            f"Make sure the output format is exactly the same as the input format. "
        )

        max_retries = 10
        for attempt in range(max_retries):
            try:
                completion = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {
                            'role': 'system',
                            'content': 'You are an academic expert with specialized knowledge in various fields.'
                        },
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ]
                )
                return completion.choices[0].message.content
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"请求失败，正在进行第 {attempt + 2} 次重试... 错误信息：{e}")
                else:
                    error_message = (
                        f"错误信息：{e}\n请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code"
                    )
                    print(error_message)
                    return str(e)
