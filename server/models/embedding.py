# 创建嵌入模型
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from config import DEFAULT_EMBEDDING_MODEL, EMBEDDING_MODEL_PATH, MODEL_DIR
from server.utils.hf_mirror import use_hf_mirror

def create_embedding_model(model_name = DEFAULT_EMBEDDING_MODEL) -> HuggingFaceEmbedding:
    try:
        use_hf_mirror()
        model_path = EMBEDDING_MODEL_PATH[model_name]
        if MODEL_DIR is not None:
            model_path = f"./{MODEL_DIR}/{model_path}"
        embed_model = HuggingFaceEmbedding(model_name=model_path)
        Settings.embed_model = embed_model
        print(f"created embed model: {model_name}")
        return embed_model
    except Exception as e:
        return None

Settings.embed_model = create_embedding_model()