import time
import streamlit as st

def handle_website():
    st.header("Load Web Pages")
    st.caption("Enter a list of URLs to extract text and metadata from web pages.")

    with st.form("website-form", clear_on_submit=True):

        col1, col2 = st.columns([1, 0.2])
        with col1:
            new_website = st.text_input("Please enter the web page address", label_visibility="collapsed")
        with col2:
            add_button = st.form_submit_button("Load")
            if add_button and new_website != "":
                st.session_state["websites"].append(new_website)

    if  st.session_state["websites"] != []:
        st.markdown(f"<p>Website(s)</p>", unsafe_allow_html=True)
        for site in  st.session_state["websites"]:
            st.caption(f"- {site}")
        st.write("")

    with st.expander(
            "Text processing parameter configuration",
            expanded=True,
    ):
        cols = st.columns(2)
        chunk_size = cols[0].number_input("Maximum length of a single text block: ", 1, 4096, st.session_state.chunk_size, key="web_chunk_size")
        chunk_overlap = cols[1].number_input("Adjacent text overlap length: ", 0, st.session_state.chunk_size, st.session_state.chunk_overlap, key="web_chunk_overlap")

    process_button = st.button("Save", 
                                key="process_website",
                                disabled=len(st.session_state["websites"]) == 0)
    if process_button:
        print("Generating index...")
        with st.spinner(text="Loading documents and building the index, may take a minute or two"):
            st.session_state.index_manager.load_websites(st.session_state["websites"], chunk_size, chunk_overlap)
            st.toast('✔️ Knowledge base index generation complete', icon='🎉')
            st.session_state.websites = []
            time.sleep(4)
            st.rerun()

handle_website()


