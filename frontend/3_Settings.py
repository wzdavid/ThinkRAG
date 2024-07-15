import streamlit as st
import server.models.ollama as ollama
from frontend.sidebar import footer
from frontend.state import init_keys
from config import EMBEDDING_MODEL_PATH, RERANKER_MODEL_PATH, RERANKER_MODEL_TOP_N

def change_ollama_endpoint():
    st.session_state.ollama_api_url = st.session_state.ollama_endpoint

def settings():
    st.header("设置")
    st.caption("设置模型与参数")

    st.subheader(
        "Ollama",
        help="Ollama is a lightweight, fast, and scalable large language model (LLM) server that provides a RESTful API for interacting with LLMs. Ollama can run on a single machine or in a distributed environment, and can be easily deployed on-premises or in the cloud.",
        )
    chat_settings = st.container(border=True)
    with chat_settings:
        st.text_input(
            "设置Ollama API服务地址",
            key="ollama_endpoint",
            value=st.session_state.ollama_api_url,
            on_change=change_ollama_endpoint,
        )
        if ollama.is_alive():
            ollama.get_model_list()
            st.write("🟢 Ollama运行中")
            with st.expander("当前可用的模型"):
                st.write(st.session_state.ollama_models)
        else:
            st.write("🔴 Ollama未运行")

        st.button(
            "刷新",
            on_click=ollama.get_model_list,
        )

    st.subheader(
        "大模型API",
        help="Large language models (LLMs) are powerful models that can generate human-like text based on the input they receive. LLMs can be used for a wide range of natural language processing tasks, including text generation, question answering, and summarization.",
    )
    llm_api_settings = st.container(border=True)
    with llm_api_settings:
        with st.expander("当前可用的模型"):
            st.write(st.session_state.llm_api_list)

    st.subheader(
        "嵌入模型",
        help="Embeddings are numerical representations of data, useful for tasks like document clustering and similarity detection when processing files, as they encode semantic meaning for efficient manipulation and retrieval.",
    )
    embedding_settings = st.container(border=True)
    with embedding_settings:
        embedding_model_list = list(EMBEDDING_MODEL_PATH.keys())
        embedding_model = st.selectbox(
            "嵌入模型", 
            embedding_model_list,
            key="selected_embedding_model",
            index=embedding_model_list.index(st.session_state["embedding_model"]),
        )
        st.session_state["embedding_model"] = embedding_model

        st.toggle("启用重排", key="selected_use_reranker", value= st.session_state.use_reranker) # 默认关闭
        st.session_state.use_reranker = st.session_state["selected_use_reranker"]
        if st.session_state.use_reranker == True:
            reranker_model_list = list(RERANKER_MODEL_PATH.keys())
            reranker_model = st.selectbox(
                "重排模型", 
                reranker_model_list,
                key="selected_reranker_model",
                index=reranker_model_list.index(st.session_state["reranker_model"]),
            )
            st.session_state["reranker_model"] = reranker_model

    st.toggle("显示高级设置", key="advanced", value= False) # 默认关闭

    if st.session_state["advanced"] == True:
        st.subheader("高级设置")
        advanced_settings = st.container(border=True)
        with advanced_settings:
            st.select_slider(
                "Top K",
                options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                help="The number of most similar documents to retrieve in response to a query.",
                value=st.session_state["top_k"],
                key="top_k",
            )
            st.text_area(
                "System Prompt",
                value=st.session_state["system_prompt"],
                key="system_prompt",
            )
            st.selectbox(
                "Chat Mode",
                (
                    "compact",
                    "refine",
                    "tree_summarize",
                    "simple_summarize",
                    "accumulate",
                    "compact_accumulate",
                ),
                help="Sets the [Llama Index Query Engine chat mode](https://github.com/run-llama/llama_index/blob/main/docs/module_guides/deploying/query_engine/response_modes.md) used when creating the Query Engine. Default: `compact`.",
                key="chat_mode",
                disabled=True,
            )
            st.write("")
        with st.expander("当前应用参数列表"):
            state = dict(sorted(st.session_state.items()))
            st.write(state)

init_keys()

footer()

settings()