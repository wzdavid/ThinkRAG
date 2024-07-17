import requests
import streamlit as st
from ollama import Client
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama

def is_alive():
    try:
        response = requests.get(st.session_state.ollama_api_url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def get_model_list():
    st.session_state.ollama_models = []
    if is_alive():
        client = Client(host=st.session_state.ollama_api_url)
        response = client.list()
        models = response["models"]
        # Initialize the list of model names
        for model in models:
            st.session_state.ollama_models.append(model["name"])
        return response["models"]
    else:
        return None

# Create Ollama LLM
def create_ollama_llm(model) -> Ollama:
    try:
        Settings.llm = Ollama(model=model, base_url=st.session_state.ollama_api_url, request_timeout=600)
        print(f"created ollama model for query: {model}")
        return Settings.llm
    except Exception as e:
        return None
