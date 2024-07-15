# 日志配置
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# 配置Streamlit Web应用
import streamlit as st
from frontend.state import init_keys

if __name__ == '__main__':

    st.set_page_config(
        page_title="ThinkRAG 本地大模型知识库问答系统",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items=None,
    )

    init_keys()

    pages = {
        "应用" : [
            st.Page("frontend/1_Document_QA.py", title="文档问答", icon="🧊"),
            st.Page("frontend/2_Knowledge_Base.py", title="知识库", icon="📃"),
        ],
        "设置" : [
            st.Page("frontend/3_Settings.py", title="设置", icon="🧭"),
            #st.Page("learn.py", title="Learn about us"),
        ]
    }

    pg = st.navigation(pages, position="sidebar")

    pg.run()
