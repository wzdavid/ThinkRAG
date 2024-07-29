# Download embedding models from HuggingFace
### 1. Install or upgrade the huggingface_hub package
```zsh
>>>pip install -U huggingface_hub
```
### 2. Use HF-Mirror to help downloading required models
```zsh
>>>export HF_ENDPOINT=https://hf-mirror.com
```
### 3. Create and change the current working directory to ~/ThinkRAG/localmodels
```zsh
>>>mkdir localmodels && cd localmodels
```
### 4. Create and change the current working directory to ~/ThinkRAG/localmodels/BAAI
```zsh
>>>mkdir BAAI && cd BAAI
```
### 5. Download required models
```zsh
>>>huggingface-cli download --resume-download BAAI/bge-small-zh-v1.5 --local-dir bge-small-zh-v1.5
```
```zsh
>>>huggingface-cli download --resume-download BAAI/bge-reranker-base --local-dir bge-reranker-base
```