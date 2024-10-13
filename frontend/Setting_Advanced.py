import streamlit as st
from server.stores.config_store import CONFIG_STORE
from frontend.state import create_llm_instance
from config import RESPONSE_MODE

st.header("Advanced settings")
advanced_settings = st.container(border=True)

def change_top_k():
    st.session_state["current_llm_settings"]["top_k"] = st.session_state["top_k"]
    CONFIG_STORE.put(key="current_llm_settings", val=st.session_state["current_llm_settings"])
    create_llm_instance()

def change_temperature():
    st.session_state["current_llm_settings"]["temperature"] = st.session_state["temperature"]
    CONFIG_STORE.put(key="current_llm_settings", val=st.session_state["current_llm_settings"])
    create_llm_instance()

def change_system_prompt():
    st.session_state["current_llm_settings"]["system_prompt"] = st.session_state["system_prompt"]
    CONFIG_STORE.put(key="current_llm_settings", val=st.session_state["current_llm_settings"])
    create_llm_instance()

def change_response_mode():
    st.session_state["current_llm_settings"]["response_mode"] = st.session_state["response_mode"]
    CONFIG_STORE.put(key="current_llm_settings", val=st.session_state["current_llm_settings"])
    create_llm_instance()

with advanced_settings:
    col_1, _, col_2 = st.columns([4, 2, 4])
    with col_1:
        st.number_input(
            "Top K",
            min_value=1,
            max_value=100,
            help="The number of most similar documents to retrieve in response to a query.",
            value=st.session_state["current_llm_settings"]["top_k"],
            key="top_k",
            on_change=change_top_k,
        )
    with col_2:
        st.select_slider(
            "Temperature",
            options=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
            help="The temperature to use when generating responses. Higher temperatures result in more random responses.",
            value=st.session_state["current_llm_settings"]["temperature"],
            key="temperature",
            on_change=change_temperature,
        )
    st.text_area(
        "System Prompt",
        help="The prompt to use when generating responses. The system prompt is used to provide context to the model.",
        value=st.session_state["current_llm_settings"]["system_prompt"],
        key="system_prompt",
        height=240,
        on_change=change_system_prompt,
    )
    st.selectbox(
        "Response Mode",
        options=RESPONSE_MODE,
        help="Sets the Llama Index Query Engine response mode used when creating the Query Engine. Default: `compact`.",
        key="response_mode",
        index=RESPONSE_MODE.index(st.session_state["current_llm_settings"]["response_mode"]), # simple_summarize by default
        on_change=change_response_mode,
    )

# For debug purpost only
def show_session_state():
    st.write("")
    with st.expander("List of current application parameters"):
        state = dict(sorted(st.session_state.items()))
        st.write(state)

# show_session_state()