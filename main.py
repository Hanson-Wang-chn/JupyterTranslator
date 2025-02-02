import os
import argparse
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from JupyterTranslator import JupyterTranslator

def find_ipynb_files(root_dir):
    ipynb_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.ipynb'):
                ipynb_files.append(os.path.join(dirpath, filename))
    return ipynb_files

def process_file(file_path, origin_language="English", target_language="Chinese", model_name="qwen-max"):
    translator = JupyterTranslator(origin_language, target_language, model_name)
    try:
        translator.read_ipynb(file_path)
        translator.translate()
        dir_name = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)
        name_part, ext = os.path.splitext(base_name)
        output_file = os.path.join(dir_name, f"{name_part}_translated{ext}")
        translator.generate_ipynb(output_file)
        # print(f"已完成处理文件: {file_path}")
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")

def main():
    parser = argparse.ArgumentParser(description="遍历目录中的 .ipynb 文件，并使用 JupyterTranslator 进行翻译。")
    parser.add_argument("directory", help="要遍历的根目录路径")
    parser.add_argument("--origin", default="English", help="原始语言，默认为 English")
    parser.add_argument("--target", default="Chinese", help="目标语言，默认为 Chinese")
    args = parser.parse_args()

    root_dir = args.directory

    ipynb_files = find_ipynb_files(root_dir)
    if not ipynb_files:
        print("未找到任何 .ipynb 文件。")
        return

    print(f"共找到 {len(ipynb_files)} 个 .ipynb 文件，开始处理...")

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_file, file_path, origin_language=args.origin, target_language=args.target) for file_path in ipynb_files]
        for future in tqdm(futures, desc="Processing .ipynb files", unit="file"):
            future.result()

if __name__ == "__main__":
    main()