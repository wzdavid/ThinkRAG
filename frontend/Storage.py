import streamlit as st
from config import THINKRAG_ENV

st.header("Storage")
st.caption("All your data is stored in local file system or the database you configured.",
    help="You may change the storage settings in the config.py file.",
)

embedding_settings = st.container(border=True)
with embedding_settings:
    st.info("You are running ThinkRAG in " + THINKRAG_ENV + " mode.")
    st.dataframe(data={
        "Type": ["Vector Store","Doc Store","Index Store","Chat Store","KV Store"],
        "Lite": ["Simple Vector Store","Simple Document Store","Simple Index Store","Simple Chat Store","Simple KV Store"],
        "Prod": ["LanceDB","Redis","Redis","Redis","Redis"],
        "Plus": ["Elasticsearch","MongoDB","MongoDB","Redis","Redis"],
     },hide_index=True)
