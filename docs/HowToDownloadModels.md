# Download embedding models from HuggingFace
### 1. install or upgrade the huggingface_hub package
```bash
>>>pip install -U huggingface_hub
```
### 2. Use HF-Mirror to help downloading required models
```bash
>>>export HF_ENDPOINT=https://hf-mirror.com
```
### 3. Create and change the current working directory to ~/ThinkRAG/localmodels
```bash
>>>mkdir localmodels && cd localmodels
```
### 4. Create and change the current working directory to ~/ThinkRAG/localmodels/BAAI
```bash
>>>mkdir BAAI && cd BAAI
```
### 5. Download required models
```bash
>>>huggingface-cli download --resume-download BAAI/bge-small-zh-v1.5 --local-dir bge-small-zh-v1.5
```
```bash
>>>huggingface-cli download --resume-download BAAI/bge-reranker-base --local-dir bge-reranker-base
```