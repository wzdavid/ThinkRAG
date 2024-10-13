import streamlit as st
import config as config
from server.models import ollama
from server.models.llm_api import create_openai_llm, check_openai_llm
from server.models.ollama import create_ollama_llm
from server.models.embedding import create_embedding_model
from server.index import IndexManager
from server.stores.config_store import CONFIG_STORE

def find_api_by_model(model_name):
    for api_name, api_info in config.LLM_API_LIST.items():
        if model_name in api_info['models']:
            return api_info

# Initialize st.session_state
def init_keys():

    # Initialize LLM
    if "llm" not in st.session_state.keys():
        st.session_state.llm = None

    # Initialize index
    if "index_manager" not in st.session_state.keys():
        st.session_state.index_manager = IndexManager(config.DEFAULT_INDEX_NAME)

    # Initialize model selection
    if "ollama_api_url" not in st.session_state.keys():
        st.session_state.ollama_api_url = config.OLLAMA_API_URL

    if "ollama_models" not in st.session_state.keys():
        ollama.get_model_list()
        if (st.session_state.ollama_models is not None and len(st.session_state.ollama_models) > 0):
            st.session_state.ollama_model_selected = st.session_state.ollama_models[0]
            create_ollama_llm(st.session_state.ollama_model_selected)
    if "ollama_model_selected" not in st.session_state.keys():
        st.session_state.ollama_model_selected = None
    if "llm_api_list" not in st.session_state.keys():
        st.session_state.llm_api_list = [model for api in config.LLM_API_LIST.values() for model in api['models']]
    if "llm_api_selected" not in st.session_state.keys():
        st.session_state.llm_api_selected = st.session_state.llm_api_list[0]
        if st.session_state.ollama_model_selected is None:
            api_object = find_api_by_model(st.session_state.llm_api_selected)
            create_openai_llm(st.session_state.llm_api_selected, api_object['api_base'], api_object['api_key'])
    
    # Initialize query engine
    if "query_engine" not in st.session_state.keys():
        st.session_state.query_engine = None

    if "system_prompt" not in st.session_state.keys():
        st.session_state.system_prompt = "Chat with me!"
        
    if "response_mode" not in st.session_state.keys():
        response_mode_result = CONFIG_STORE.get(key="response_mode")
        if response_mode_result is not None:
            st.session_state.response_mode = response_mode_result["response_mode"]
        else:
            st.session_state.response_mode = config.DEFAULT_RESPONSE_MODE

    if "ollama_endpoint" not in st.session_state.keys():
        st.session_state.ollama_endpoint = "http://localhost:11434"

    if "chunk_size" not in st.session_state.keys():
        st.session_state.chunk_size = config.DEFAULT_CHUNK_SIZE
    
    if "chunk_overlap" not in st.session_state.keys():
        st.session_state.chunk_overlap = config.DEFAULT_CHUNK_OVERLAP

    if "zh_title_enhance" not in st.session_state.keys():
        st.session_state.zh_title_enhance = config.ZH_TITLE_ENHANCE

    if "max_tokens" not in st.session_state.keys():
        st.session_state.max_tokens = 100
    
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

def init_llm_sp():

    llm_options = list(config.LLM_API_LIST.keys())

    # LLM service provider selection
    if "llm_service_provider_selected" not in st.session_state:
        sp = CONFIG_STORE.get(key="llm_service_provider_selected")
        if sp:
            st.session_state.llm_service_provider_selected = sp["llm_service_provider_selected"]
        else:
            st.session_state.llm_service_provider_selected = llm_options[0]

def init_ollama_endpoint():
    # Initialize Ollama endpoint
    if "ollama_api_url" not in st.session_state.keys():
        ollama_api_url = CONFIG_STORE.get(key="Ollama_api_url")
        if ollama_api_url:
            st.session_state.ollama_api_url = ollama_api_url["Ollama_api_url"]
        else:
            st.session_state.ollama_api_url = config.LLM_API_LIST["Ollama"]["api_base"]

# Initialize llm api model
def init_api_model(sp):
    if sp != "Ollama":
        model_key = sp + "_model_selected"
        if model_key not in st.session_state.keys():
            model_result = CONFIG_STORE.get(key=model_key)
            if model_result:
                st.session_state[model_key] = model_result[model_key]
            else:
                st.session_state[model_key] = config.LLM_API_LIST[sp]["models"][0]


# Initialize llm api base
def init_api_base(sp):
    if sp != "Ollama":
        api_base = sp + "_api_base"
        if api_base not in st.session_state.keys():
            api_key_result = CONFIG_STORE.get(key=api_base)
            if api_key_result is not None:
                st.session_state[api_base] = api_key_result[api_base]
            else:
                st.session_state[api_base] = config.LLM_API_LIST[sp]["api_base"]

# Initialize llm api key
def init_api_key(sp):
    if sp != "Ollama":
        api_key = sp + "_api_key"
        if api_key not in st.session_state.keys():
            api_key_result = CONFIG_STORE.get(key=api_key)
            if api_key_result is not None:
                st.session_state[api_key] = api_key_result[api_key]
            else:
                st.session_state[api_key] = config.LLM_API_LIST[sp]["api_key"]
        
        valid_key = api_key + "_valid"
        if valid_key not in st.session_state.keys():
            valid_result = CONFIG_STORE.get(key=valid_key)
            if valid_result is None and st.session_state[api_key] is not None:
                is_valid = check_openai_llm(st.session_state[sp + "_model_selected"], config.LLM_API_LIST[sp]["api_base"], st.session_state[api_key])
                CONFIG_STORE.put(key=valid_key, val={valid_key: is_valid})
                st.session_state[valid_key] = is_valid
            else:
                st.session_state[valid_key] = valid_result[valid_key]

# Initialize LLM settings, like temperature, system prompt, etc.
def init_llm_settings():
    if "current_llm_settings" not in st.session_state.keys():
        current_llm_settings = CONFIG_STORE.get(key="current_llm_settings")
        if current_llm_settings:
            st.session_state.current_llm_settings = current_llm_settings
        else:
            st.session_state.current_llm_settings = {
                "temperature": config.TEMPERATURE,
                "system_prompt": config.SYSTEM_PROMPT,
                "top_k": config.TOP_K,
                "response_mode": config.DEFAULT_RESPONSE_MODE,
                "use_reranker": config.USE_RERANKER,
                "top_n": config.RERANKER_MODEL_TOP_N,
                "embedding_model": config.DEFAULT_EMBEDDING_MODEL,
                "reranker_model": config.DEFAULT_RERANKER_MODEL,
            }
            CONFIG_STORE.put(key="current_llm_settings", val=st.session_state.current_llm_settings)


# Create LLM instance if there is related information
def create_llm_instance():
    current_llm_info = CONFIG_STORE.get(key="current_llm_info")
    if current_llm_info is not None:
        print("Current LLM info: ", current_llm_info)
        if current_llm_info["service_provider"] == "Ollama":
            if ollama.is_alive():
                model_name = current_llm_info["model"]
                st.session_state.llm = ollama.create_ollama_llm(
                    model=model_name, 
                    temperature=st.session_state.current_llm_settings["temperature"],
                    system_prompt=st.session_state.current_llm_settings["system_prompt"],
                )
        else:
            model_name = current_llm_info["model"]
            api_base = current_llm_info["api_base"]
            api_key = current_llm_info["api_key"]
            api_key_valid = current_llm_info["api_key_valid"]
            if api_key_valid:
                st.session_state.llm = create_openai_llm(
                    model_name=model_name, 
                    api_base=api_base, 
                    api_key=api_key,
                    temperature=st.session_state.current_llm_settings["temperature"],
                    system_prompt=st.session_state.current_llm_settings["system_prompt"],
                )
            else:
                print("API key is invalid")
                st.session_state.llm = None
    else:
        print("No current LLM infomation")
        st.session_state.llm = None

def init_state():
    init_keys()
    init_llm_sp()
    init_llm_settings()
    init_ollama_endpoint()
    sp = st.session_state.llm_service_provider_selected
    init_api_model(sp)
    init_api_key(sp)
    create_embedding_model(st.session_state["current_llm_settings"]["embedding_model"])
    create_llm_instance()