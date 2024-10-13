# Create Rerank model
# https://docs.llamaindex.ai/en/stable/examples/node_postprocessor/SentenceTransformerRerank/
import os
from llama_index.core.postprocessor import SentenceTransformerRerank
from config import DEFAULT_RERANKER_MODEL, RERANKER_MODEL_TOP_N, RERANKER_MODEL_PATH, MODEL_DIR
from server.utils.hf_mirror import use_hf_mirror

def create_reranker_model(model_name = DEFAULT_RERANKER_MODEL, top_n = RERANKER_MODEL_TOP_N) -> SentenceTransformerRerank:
    try:
        use_hf_mirror()
        model_path = RERANKER_MODEL_PATH[model_name]
        if MODEL_DIR is not None:
            path = f"./{MODEL_DIR}/{model_path}"
            if os.path.exists(path): # Use local models if the path exists
                model_path = path
        rerank_model = SentenceTransformerRerank(model=model_path, top_n=top_n)
        print(f"created rerank model: {model_name}")
        return rerank_model
    except Exception as e:
        return None