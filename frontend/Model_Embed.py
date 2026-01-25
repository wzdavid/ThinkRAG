import streamlit as st
from config import EMBEDDING_MODEL_PATH
from server.stores.config_store import CONFIG_STORE
from server.stores.strage_context import STORAGE_CONTEXT
from server.models.embedding import create_embedding_model

st.header("Embedding Model")
st.caption("Configure embedding models",
    help="Embeddings are numerical representations of data, useful for tasks like document clustering and similarity detection when processing files, as they encode semantic meaning for efficient manipulation and retrieval.",
)

def change_embedding_model():
    st.session_state["current_llm_settings"]["embedding_model"] = st.session_state["selected_embedding_model"]
    CONFIG_STORE.put(key="current_llm_settings", val=st.session_state["current_llm_settings"])
    create_embedding_model(st.session_state["current_llm_settings"]["embedding_model"])

doc_store = STORAGE_CONTEXT.docstore

def _safe_doc_count(doc_store):
    try:
        return len(doc_store.docs)
    except Exception as e:
        st.error("Production mode 需要 Redis，但当前无法连接到 Redis（localhost:6379）。")
        st.code(str(e))
        st.info(
            "修复（WSL/Ubuntu）：\n"
            "1) sudo apt install -y redis-server redis-tools\n"
            "2) redis-server --daemonize yes\n"
            "3) redis-cli ping  （应返回 PONG）"
        )
        st.stop()


if _safe_doc_count(doc_store) > 0:
    disabled = True
else:
    disabled = False
embedding_settings = st.container(border=True)
with embedding_settings:
    embedding_model_list = list(EMBEDDING_MODEL_PATH.keys())
    embedding_model = st.selectbox(
        "Embedding models", 
        embedding_model_list,
        key="selected_embedding_model",
        index=embedding_model_list.index(st.session_state["current_llm_settings"]["embedding_model"]),
        disabled=disabled,
        on_change=change_embedding_model,
    )
    if disabled:
        st.info("You cannot change embedding model once you add documents in the knowledge base.")
    st.caption("ThinkRAG supports most reranking models from `Hugging Face`. You may specify the models you want to use in the `config.py` file.")
    st.caption("It is recommended to download the models to the `localmodels` directory, in case you need run the system without an Internet connection. Plase refer to the instructions in `docs` directory.")
