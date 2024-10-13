import streamlit as st
from config import RERANKER_MODEL_PATH
from server.stores.config_store import CONFIG_STORE

st.header("Reranking Model")
st.caption("Configure reranking models",
    help="Reranking is the process of reordering a list of items based on a set of criteria. In the context of search engines, reranking is used to improve the relevance of search results by taking into account additional information about the items being ranked.",
)

def change_use_reranker():
    st.session_state["current_llm_settings"]["use_reranker"] = st.session_state["use_reranker"]
    CONFIG_STORE.put(key="current_llm_settings", val=st.session_state["current_llm_settings"])

def change_top_n():
    st.session_state["current_llm_settings"]["top_n"] = st.session_state["top_n"]
    CONFIG_STORE.put(key="current_llm_settings", val=st.session_state["current_llm_settings"])

def change_reranker_model():
    st.session_state["current_llm_settings"]["reranker_model"] = st.session_state["selected_reranker_model"]
    CONFIG_STORE.put(key="current_llm_settings", val=st.session_state["current_llm_settings"])

reranking_settings = st.container(border=True)
with reranking_settings:
    st.toggle("Use reranker", 
              key="use_reranker", 
              value= st.session_state["current_llm_settings"]["use_reranker"],
              on_change=change_use_reranker,
              )
    if st.session_state["current_llm_settings"]["use_reranker"] == True:
        st.number_input(
            "Top N",
            min_value=1,
            max_value=st.session_state["current_llm_settings"]["top_k"],
            help="The number of most similar documents to retrieve in response to a query.",
            value=st.session_state["current_llm_settings"]["top_n"],
            key="top_n",
            on_change=change_top_n,
        )
        
        reranker_model_list = list(RERANKER_MODEL_PATH.keys())
        reranker_model = st.selectbox(
            "Reranking models", 
            reranker_model_list,
            key="selected_reranker_model",
            index=reranker_model_list.index(st.session_state["current_llm_settings"]["reranker_model"]),
            on_change=change_reranker_model,
        )
    
        st.caption("ThinkRAG supports most reranking models from `Hugging Face`. You may specify the models you want to use in the `config.py` file.")
        st.caption("It is recommended to download the models to the `localmodels` directory, in case you need run the system without an Internet connection. Plase refer to the instructions in `docs` directory.")