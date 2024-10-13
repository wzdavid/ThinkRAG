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
        "Storage Type": ["Vector Store","Doc Store","Index Store","Chat Store","Config Store"],
        "Development": ["Simple Vector Store","Simple Document Store","Simple Index Store","Simple Chat Store (in memory)","Simple KV Store"],
        "Production": ["Chroma","Redis","Redis","Redis","Simple KV Store"],
        #"Enterprise": ["Elasticsearch","MongoDB","MongoDB","Redis","Simple KV Store"],
     },hide_index=True)
    
    st.caption("You may change the storage settings in the config.py file.")
    st.caption("`Development Mode` uses local storage which means you need not install any extra tools. All the data is stored as local files in the 'storage' directory where you run ThinkRAG.")
    st.caption("`Production Mode`: is recommended to use for production on your laptop. You need a redis instance, either running locally or using a cloud service.")
    st.caption("If you want to deploy ThinkRAG on a server and handle large volume of data, please contact the author of ThinkRAG (wzdavid@gmail.com)")