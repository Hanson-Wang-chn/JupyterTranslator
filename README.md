# Jupyter Translator

## Description

This is an end-to-end tool that can read `.ipynb` files and translate all Markdown blocks via LLMs, say `qwen-max-latest`.

**Input**: A directory inside which `.ipynb` files will be translated asynchronously, origin language, target language.

**Output**: Tranlated `.ipynb` files added to the input directory.

## How to Use

First, you should configure the API Key for the LLM. Official instructions are [here](https://help.aliyun.com/zh/model-studio/developer-reference/configure-api-key-through-environment-variables?spm=0.0.0.i0).

Then, run the following commands.

```bash
  conda create -n jupyter-translator python=3.10 -y
  conda activate jupyter-translator
  pip install -r requirements.txt
  cd /path/to/JupyterTranslator
  python main.py /path/to/the/input/directory
```
