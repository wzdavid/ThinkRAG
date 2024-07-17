# Configure the Streamlit Web Application
import streamlit as st
from server.models import ollama
from server.models.llm_api import create_openai_llm
from server.models.ollama import create_ollama_llm
from frontend.state import find_api_by_model

def handle_ollama_llm():
    model_name = st.session_state.ollama_model_name
    print(f"selected_option: {model_name}")
    create_ollama_llm(model_name)
    st.session_state.ollama_model_selected = model_name
    #st.session_state.query_engine = create_query_engine(st.session_state.index)

def handle_openai_llm():
    model_name = st.session_state.llm_api_model_name
    print(f"selected_option: {model_name}")
    api_object = find_api_by_model(model_name)
    create_openai_llm(model_name, api_object['api_base'], api_object['api_key'])
    st.session_state.llm_api_selected = model_name
    #st.session_state.query_engine = create_query_engine(st.session_state.index)    

def select_llm():    
    with st.sidebar:
        st.header('当前设置')

        if ollama.is_alive():
            ollama.get_model_list()
            options = ('本地大模型', '大模型API')
            options1 = st.session_state.ollama_models
        else:
            options = ['大模型API']

        if 'selected_radio_option' not in st.session_state or len(options) == 1:
            st.session_state.selected_radio_option = options[0]

        select_box = st.radio("选择模型来源", options, horizontal=True, label_visibility='collapsed', index=options.index(st.session_state.selected_radio_option))
        st.session_state.selected_radio_option = select_box
        
        options2 = st.session_state.llm_api_list
        if select_box == '本地大模型':
            index = None
            if st.session_state.ollama_model_selected is None:
                if len(st.session_state.ollama_models) > 0:
                    st.session_state.ollama_model_selected = st.session_state.ollama_models[0]
                    index=0
            else:
                index = st.session_state.ollama_models.index(st.session_state.ollama_model_selected)
            st.selectbox('选择本地大模型', options1,
                        index=index,
                        help='选择Ollama本地部署的LLM',
                        on_change=handle_ollama_llm,
                        key='ollama_model_name', # session_state key
            )
        elif select_box == '大模型API':
            st.selectbox('选择大模型API', options2,
                        index=st.session_state.llm_api_list.index(st.session_state.llm_api_selected),
                        help='选择大模型API服务',
                        on_change=handle_openai_llm,
                        key='llm_api_model_name', # session_state key
            )
        st.divider()

def footer():
    with st.sidebar:
        st.caption('ThinkRAG 本地大模型知识库问答系统')
        st.caption('©2024 wzdavid@gmail.com')
