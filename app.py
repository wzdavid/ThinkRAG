# Log configuration
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Configure the Streamlit Web Application
import streamlit as st
from frontend.state import init_keys

if __name__ == '__main__':

    st.set_page_config(
        page_title="ThinkRAG —— Local LLM Knowledge Base Q&A System",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items=None,
    )

    init_keys()

    pages = {
        "Application" : [
            st.Page("frontend/1_Document_QA.py", title="Document-based Q&A", icon="🧊"),
            st.Page("frontend/2_Knowledge_Base.py", title="Knowledge Base", icon="📃"),
        ],
        "Settings" : [
            st.Page("frontend/3_Settings.py", title="Settings", icon="🧭"),
            #st.Page("learn.py", title="Learn about us"),
        ]
    }

    pg = st.navigation(pages, position="sidebar")

    pg.run()
