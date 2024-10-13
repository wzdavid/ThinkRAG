import streamlit as st
from config import LLM_API_LIST
import server.models.ollama as ollama
from server.stores.config_store import CONFIG_STORE
from server.models.llm_api import check_openai_llm
from frontend.state import init_llm_sp, init_ollama_endpoint, init_api_base, init_api_model, init_api_key, create_llm_instance

st.header("Large Language Model")
st.caption("Support local models from Ollama and OpenAI compatible LLM APIs.",
    help="Large language models (LLMs) are powerful models that can generate human-like text based on the input they receive. LLMs can be used for a wide range of natural language processing tasks, including text generation, question answering, and summarization.",
)

init_llm_sp()

sp = st.session_state.llm_service_provider_selected
llm = LLM_API_LIST[sp]

init_ollama_endpoint()
init_api_base(sp)
init_api_model(sp)
init_api_key(sp)

def save_current_llm_info():
    sp = st.session_state.llm_service_provider_selected
    if sp == "Ollama":
        if st.session_state.ollama_model_selected is not None:
            CONFIG_STORE.put(key="current_llm_info", val={
            "service_provider": sp,
            "model": st.session_state.ollama_model_selected,
            })
    else:
        api_key = sp + "_api_key"
        model_key = sp + "_model_selected"
        base_key = sp + "_api_base"
        if st.session_state[model_key] is not None and st.session_state[api_key] is not None and st.session_state[base_key] is not None:
            CONFIG_STORE.put(key="current_llm_info", val={
                "service_provider": sp,
                "model": st.session_state[model_key],
                "api_base": st.session_state[base_key],
                "api_key": st.session_state[api_key],
                "api_key_valid": st.session_state[api_key + "_valid"],
            })
        else:
            st.warning("Please fill in all the required fields")

def update_llm_service_provider():
    selected_option = st.session_state["llm_service_provider"]
    st.session_state.llm_service_provider_selected = selected_option
    CONFIG_STORE.put(key="llm_service_provider_selected", val={"llm_service_provider_selected": selected_option})
    if selected_option != "Ollama":
        init_api_base(selected_option)
        init_api_model(selected_option)
        init_api_key(selected_option)
    save_current_llm_info()

def init_llm_options():
    llm_options = list(LLM_API_LIST.keys())
    col1, _, col2 = st.columns([5, 4, 1], vertical_alignment="bottom")
    with col1:
        option = st.selectbox(
            "Please select one of the options.",
            llm_options,
            index=llm_options.index(st.session_state.llm_service_provider_selected),
            key="llm_service_provider",
            on_change=update_llm_service_provider,
        )

    if option is not None and option != st.session_state.llm_service_provider_selected:
        CONFIG_STORE.put(key="llm_service_provider_selected", val={
            "llm_service_provider_selected": option, 
        })
    
    current_llm_info = CONFIG_STORE.get(key="current_llm_info")

    if current_llm_info is None:
        save_current_llm_info()

init_llm_options()

option = st.session_state.llm_service_provider_selected

def change_ollama_endpoint():
    st.session_state.ollama_api_url = st.session_state.ollama_endpoint
    if ollama.is_alive():
        name = option + "_api_url" # e.g. "Ollama_api_url"
        CONFIG_STORE.put(key=name, val={
            name: st.session_state.ollama_api_url, 
        })
        save_current_llm_info()
    else:
        st.warning("Failed to connect to Ollama")

def change_ollama_model():
    st.session_state.ollama_model_selected = st.session_state.ollama_model_name
    name = option + "_model_selected" # e.g. "Ollama_model_selected"
    CONFIG_STORE.put(key=name, val={
        name: st.session_state.ollama_model_selected,
    })
    save_current_llm_info()

def change_llm_api_base():
    name = option + "_api_base" # e.g. "OpenAI_api_base"
    st.session_state[name] = st.session_state.llm_api_endpoint
    CONFIG_STORE.put(key=name, val={
        name: st.session_state.llm_api_endpoint, 
    })
    save_current_llm_info()

def change_llm_api_key():
    name = option + "_api_key" # e.g. "OpenAI_api_key"
    CONFIG_STORE.put(key=name, val={
        name: st.session_state.llm_api_key, 
    })
    is_valid = check_openai_llm(st.session_state.llm_api_model, st.session_state.llm_api_base, st.session_state.llm_api_key)
    CONFIG_STORE.put(key=name + "_valid", val={ # e.g. "OpenAI_api_key_valid"
        name + "_valid": is_valid, 
    })
    if is_valid:
        save_current_llm_info()
        print("API key is valid")
    else:
        print("API key is invalid")
 
def change_llm_api_model():
    name = option + "_model_selected" # e.g. "OpenAI_model_selected"
    st.session_state[name] = st.session_state.llm_api_model
    CONFIG_STORE.put(key=name, val={
        name: st.session_state.llm_api_model,
    })
    save_current_llm_info()

def llm_configuration_page():
    llm_api_settings = st.container(border=True)
    with llm_api_settings:
        if option == "Ollama":
            st.subheader("Configure for Ollama")
            st.text_input(
                "Ollama Endpoint",
                key="ollama_endpoint",
                value=st.session_state.ollama_api_url,
                on_change=change_ollama_endpoint,
            )
            if ollama.is_alive():
                ollama.get_model_list()
                st.write("🟢 Ollama is running")
                st.selectbox('Local LLM', st.session_state.ollama_models,
                            index=st.session_state.ollama_models.index(st.session_state.ollama_model_selected),
                            help='Select locally deployed LLM from Ollama',
                            on_change=change_ollama_model,
                            key='ollama_model_name', # session_state key
                )
            else:
                st.write("🔴 Ollama is not running")

            st.button(
                "Refresh models",
                on_click=ollama.get_model_list,
                help="Refresh the list of available models from the Ollama API.",
            )
            
        else: # OpenAI, Zhipu, Moonshot, Deepseek
            st.subheader(f"Configure for {llm['provider']}")
            st.text_input(
                "Base URL",
                key="llm_api_endpoint",
                value=st.session_state[option + "_api_base"],
                on_change=change_llm_api_base,
            )
            st.text_input(
                "API key",
                key="llm_api_key",
                value=st.session_state[option + "_api_key"],
                type="password",
                on_change=change_llm_api_key,
            )
            st.selectbox('Choose LLM API', llm['models'],
                        help='Choose LLMs API service',
                        on_change=change_llm_api_model,
                        key='llm_api_model',
                        index=llm['models'].index(st.session_state[option + "_model_selected"]),
            )

def show_llm_instance():
    create_llm_instance()
    if st.session_state.llm is not None:
        current_llm_info = CONFIG_STORE.get(key="current_llm_info")
        st.success("Current LLM instance: " + current_llm_info["service_provider"] + " / " + current_llm_info["model"])
    else:
        st.warning("No LLM instance available")

llm_configuration_page()

show_llm_instance()

st.caption("ThinkRAG supports `OpenAI` and all compatible LLM API like `Zhipu` or `Moonshot`. You may specify the LLMs you want to use in the `config.py` file.")
st.caption("It is recommended to use `Ollama` if you need run the system without an Internet connection. Plase refer to the Ollama docs to download and use Ollama models.")