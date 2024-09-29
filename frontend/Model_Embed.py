import streamlit as st
from config import EMBEDDING_MODEL_PATH

st.header("Embedding Model")
st.caption("Configure embedding models",
    help="Embeddings are numerical representations of data, useful for tasks like document clustering and similarity detection when processing files, as they encode semantic meaning for efficient manipulation and retrieval.",
)

embedding_settings = st.container(border=True)
with embedding_settings:
    embedding_model_list = list(EMBEDDING_MODEL_PATH.keys())
    embedding_model = st.selectbox(
        "Embedding models", 
        embedding_model_list,
        key="selected_embedding_model",
        index=embedding_model_list.index(st.session_state["embedding_model"]),
    )
    st.session_state["embedding_model"] = embedding_model