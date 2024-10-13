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
if len(doc_store.docs) > 0:
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