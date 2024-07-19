import streamlit as st
from config import LLM_API_LIST, OLLAMA_API_URL, DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP, ZH_TITLE_ENHANCE, DEFAULT_EMBEDDING_MODEL, DEFAULT_RERANKER_MODEL, USE_RERANKER
from server.models import ollama
from server.models.llm_api import create_openai_llm
from server.models.ollama import create_ollama_llm
from server.index import IndexManager
from config import DEFAULT_INDEX_NAME

def find_api_by_model(model_name):
    for api_name, api_info in LLM_API_LIST.items():
        if model_name in api_info['models']:
            return api_info

# Initialize st.session_state
def init_keys():
    # Initialize index
    if "index_manager" not in st.session_state.keys():
        st.session_state.index_manager = IndexManager(DEFAULT_INDEX_NAME)

    # Initialize model selection
    if "ollama_api_url" not in st.session_state.keys():
        st.session_state.ollama_api_url = OLLAMA_API_URL

    if "ollama_models" not in st.session_state.keys():
        ollama.get_model_list()
        if (st.session_state.ollama_models is not None and len(st.session_state.ollama_models) > 0):
            st.session_state.ollama_model_selected = st.session_state.ollama_models[0]
            create_ollama_llm(st.session_state.ollama_model_selected)
    if "ollama_model_selected" not in st.session_state.keys():
        st.session_state.ollama_model_selected = None
    if "llm_api_list" not in st.session_state.keys():
        st.session_state.llm_api_list = [model for api in LLM_API_LIST.values() for model in api['models']]
    if "llm_api_selected" not in st.session_state.keys():
        st.session_state.llm_api_selected = st.session_state.llm_api_list[0]
        if st.session_state.ollama_model_selected is None:
            api_object = find_api_by_model(st.session_state.llm_api_selected)
            create_openai_llm(st.session_state.llm_api_selected, api_object['api_base'], api_object['api_key'])
    
    if "embedding_model" not in st.session_state.keys():
        st.session_state.embedding_model = DEFAULT_EMBEDDING_MODEL
    
    if "reranker_model" not in st.session_state.keys():
        st.session_state.reranker_model = DEFAULT_RERANKER_MODEL

    if "use_reranker" not in st.session_state.keys():
        st.session_state.use_reranker = USE_RERANKER

    # Initialize query engine
    if "query_engine" not in st.session_state.keys():
        st.session_state.query_engine = None

    # Initialize settings
    if "top_k" not in st.session_state.keys():
        st.session_state.top_k = 5

    if "system_prompt" not in st.session_state.keys():
        st.session_state.system_prompt = "Chat with me!"
    
    if "chat_mode" not in st.session_state.keys():
        st.session_state.chat_mode = "compact"
    
    if "ollama_endpoint" not in st.session_state.keys():
        st.session_state.ollama_endpoint = "http://localhost:11434"

    if "chunk_size" not in st.session_state.keys():
        st.session_state.chunk_size = DEFAULT_CHUNK_SIZE
    
    if "chunk_overlap" not in st.session_state.keys():
        st.session_state.chunk_overlap = DEFAULT_CHUNK_OVERLAP

    if "zh_title_enhance" not in st.session_state.keys():
        st.session_state.zh_title_enhance = ZH_TITLE_ENHANCE

    if "max_tokens" not in st.session_state.keys():
        st.session_state.max_tokens = 100

    if "temperature" not in st.session_state.keys():
        st.session_state.temperature = 0.5
    
    if "top_p" not in st.session_state.keys():
        st.session_state.top_p = 1.0

    # contents related to the knowledge base
    if "websites" not in st.session_state:
        st.session_state["websites"] = []

    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    if 'selected_files' not in st.session_state:
        st.session_state.selected_files = None

# Initialize user data
# TODO: supposed to be loaded from database
    st.session_state.user_id = "user_1"
    st.session_state.kb_id = "kb_1"
    st.session_state.kb_name = "My knowledge base"