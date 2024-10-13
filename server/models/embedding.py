# Create embedding models
import os
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from config import DEFAULT_EMBEDDING_MODEL, EMBEDDING_MODEL_PATH, MODEL_DIR
from server.utils.hf_mirror import use_hf_mirror

def create_embedding_model(model_name = DEFAULT_EMBEDDING_MODEL) -> HuggingFaceEmbedding:
    try:
        use_hf_mirror()
        model_path = EMBEDDING_MODEL_PATH[model_name]
        if MODEL_DIR is not None:
            path = f"./{MODEL_DIR}/{model_path}"
            if os.path.exists(path): # Use local models if the path exists
                model_path = path
        embed_model = HuggingFaceEmbedding(model_name=model_path)
        Settings.embed_model = embed_model
        print(f"created embed model: {model_path}")
    except Exception as e:
        print(f"An error occurred while creating the embedding model: {type(e).__name__}: {e}")
        Settings.embed_model = None

    return Settings.embed_model