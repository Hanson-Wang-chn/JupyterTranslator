import json


def read_ipynb(file_path):
    # 打开并读取.ipynb文件
    with open(file_path, 'r', encoding='utf-8') as f:
        # 解析JSON数据
        notebook = json.load(f)

    # 初始化Markdown和代码块列表
    markdown_blocks = []
    code_blocks = []

    # 遍历笔记本中的每个单元格
    for cell in notebook['cells']:
        if cell['cell_type'] == 'markdown':
            # 将Markdown单元格的内容添加到列表中
            markdown_blocks.append(''.join(cell['source']))
        elif cell['cell_type'] == 'code':
            # 将代码单元格的内容添加到列表中
            code_blocks.append(''.join(cell['source']))

    return markdown_blocks, code_blocks


# 示例使用
file_path = 'example.ipynb'
markdowns, codes = read_ipynb(file_path)

print(len(markdowns))
