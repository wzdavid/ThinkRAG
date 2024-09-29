# Log configuration
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Configure the Streamlit Web Application
import streamlit as st
from frontend.state import init_state

if __name__ == '__main__':

    st.set_page_config(
        page_title="ThinkRAG - LLM RAG system runs on laptop",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items=None,
    )

    st.logo("frontend/images/ThinkRAG_Logo.png")

    init_state()

    pages = {
        "Application" : [
            st.Page("frontend/Document_QA.py", title="Query"),
        ],
        "Knowledge Base" : [
           st.Page("frontend/KB_File.py", title="File"),
           st.Page("frontend/KB_Web.py", title="Web"),
           st.Page("frontend/KB_Manage.py", title="Manage"),
        ],
        "Model & Tool" : [
            st.Page("frontend/Model_LLM.py", title="LLM"),
            st.Page("frontend/Model_Embed.py", title="Embed"),
            st.Page("frontend/Model_Rerank.py", title="Rerank"),
            st.Page("frontend/Storage.py", title="Storage"),
        ],
        "Settings" : [
           st.Page("frontend/Setting_Advanced.py", title="Advanced"),
        ],
    }

    pg = st.navigation(pages, position="sidebar")

    pg.run()