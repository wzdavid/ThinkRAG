# 设置HuggingFace镜像

def use_hf_mirror():
    import os
    from config import HF_ENDPOINT
    os.environ['HF_ENDPOINT'] = HF_ENDPOINT
    print(f"Use HF mirror: {os.environ['HF_ENDPOINT']}")
    return os.environ['HF_ENDPOINT']
