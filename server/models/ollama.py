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
        print("Failed to connect to Ollama")
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
        print("Ollama is not alive")
        return None

# Create Ollama LLM
def create_ollama_llm(model:str, temperature:float = 0.5, system_prompt:str = None) -> Ollama:
    try:
        llm = Ollama(
            model=model, 
            base_url=st.session_state.ollama_api_url, 
            request_timeout=600,
            temperature=temperature,
            system_prompt=system_prompt,
            )
        print(f"created ollama model for query: {model}")
        Settings.llm = llm
        return llm
    except Exception as e:
        print(f"An error occurred while creating Ollama LLM: {e}")
        return None
