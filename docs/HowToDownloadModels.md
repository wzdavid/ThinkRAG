# Download embedding models from HuggingFace
>>>pip install -U huggingface_hub
>>>export HF_ENDPOINT=https://hf-mirror.com
>>>cd localmodels
>>>mkdir BAAI && cd BAAI
>>>huggingface-cli download --resume-download BAAI/bge-small-zh-v1.5 --local-dir bge-small-zh-v1.5
>>>huggingface-cli download --resume-download BAAI/bge-reranker-base --local-dir bge-reranker-base
