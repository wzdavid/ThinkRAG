import streamlit as st
from config import RERANKER_MODEL_PATH, RERANKER_MODEL_TOP_N

st.header("Reranking Model")
st.caption("Configure reranking models",
    help="Reranking is the process of reordering a list of items based on a set of criteria. In the context of search engines, reranking is used to improve the relevance of search results by taking into account additional information about the items being ranked.",
)

reranking_settings = st.container(border=True)
with reranking_settings:
    st.toggle("Enable reranking", key="selected_use_reranker", value= st.session_state.use_reranker) # closed by default
    st.session_state.use_reranker = st.session_state["selected_use_reranker"]
    if st.session_state.use_reranker == True:
        reranker_model_list = list(RERANKER_MODEL_PATH.keys())
        reranker_model = st.selectbox(
            "Reranking models", 
            reranker_model_list,
            key="selected_reranker_model",
            index=reranker_model_list.index(st.session_state["reranker_model"]),
        )
        st.session_state["reranker_model"] = reranker_model
