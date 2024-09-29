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
        st.header('Query settings')

        if ollama.is_alive():
            ollama.get_model_list()
            options = ('Local LLMs', 'LLMs API')
            options1 = st.session_state.ollama_models
        else:
            options = ['LLMs API']

        if 'selected_radio_option' not in st.session_state or len(options) == 1:
            st.session_state.selected_radio_option = options[0]

        select_box = st.radio("Select model source", options, horizontal=True, label_visibility='collapsed', index=options.index(st.session_state.selected_radio_option))
        st.session_state.selected_radio_option = select_box
        
        options2 = st.session_state.llm_api_list
        if select_box == 'Local LLMs':
            index = None
            if st.session_state.ollama_model_selected is None:
                if len(st.session_state.ollama_models) > 0:
                    st.session_state.ollama_model_selected = st.session_state.ollama_models[0]
                    index=0
            else:
                index = st.session_state.ollama_models.index(st.session_state.ollama_model_selected)
            st.selectbox('Choose local LLM', options1,
                        index=index,
                        help='Select locally deployed LLM from Ollama',
                        on_change=handle_ollama_llm,
                        key='ollama_model_name', # session_state key
            )
        elif select_box == 'LLMs API':
            st.selectbox('Choose LLM API', options2,
                        index=st.session_state.llm_api_list.index(st.session_state.llm_api_selected),
                        help='Choose LLMs API service',
                        on_change=handle_openai_llm,
                        key='llm_api_model_name', # session_state key
            )
        st.divider()

def footer():
    with st.sidebar:
        st.caption('©2024 wzdavid@gmail.com')
