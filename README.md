# Jupyter Translator

## Description

This is an end-to-end tool that can read `.ipynb` files and translate all Markdown blocks via LLMs, say `qwen-max-latest`.

**Input**: A directory inside which `.ipynb` files will be translated asynchronously, origin language, target language.

**Output**: Tranlated `.ipynb` files added to the input directory.

## How to Use

```bash
  conda create -n jupyter-translator python=3.10 -y
  conda activate jupyter-translator
  pip install -r requirements.txt
  cd /path/to/JupyterTranslator
  python main.py /path/to/the/input/directory
```
