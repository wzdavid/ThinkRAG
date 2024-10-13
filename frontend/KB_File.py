import time
import pandas as pd
import streamlit as st
from server.utils.file import save_uploaded_file, get_save_dir

def handle_file():

    st.header("Load Files")
    st.caption("Load Files like PDF, DOCX, TXT, etc. to create a knowledge base index.")
    
    with st.form("my-form", clear_on_submit=True):
        st.session_state.selected_files = st.file_uploader("Upload files: ", accept_multiple_files=True, label_visibility="hidden")
        submitted = st.form_submit_button(
            "Load",
            help="Click here to load it after you select a file.",
            )
        if len(st.session_state.selected_files) > 0 and submitted:
            print("Starting to upload files...")
            print(st.session_state.selected_files)
            for selected_file in st.session_state.selected_files:
                with st.spinner(f"Uploading {selected_file.name}..."):
                    save_dir = get_save_dir()
                    save_uploaded_file(selected_file, save_dir)
                    st.session_state.uploaded_files.append({"name": selected_file.name, "type": selected_file.type, "size": selected_file.size})
            st.toast('✔️ Upload successful', icon='🎉')

    if len(st.session_state.uploaded_files) > 0:
        with st.expander(
                "The following files are uploaded successfully.",
                expanded=True,
        ):
            df = pd.DataFrame(st.session_state.uploaded_files)
            st.dataframe(
                df,
                column_config={
                    "name": "File name",
                    "size": st.column_config.NumberColumn(
                        "size", format="%d byte",
                    ),
                    "type": "type",
                },
                hide_index=True,
            )

    with st.expander(
            "Text Splitter Settings",
            expanded=True,
    ):
        cols = st.columns(2)
        chunk_size = cols[0].number_input("Maximum length of a single text block: ", 1, 4096, st.session_state.chunk_size)
        chunk_overlap = cols[1].number_input("Adjacent text overlap length: ", 0, st.session_state.chunk_size, st.session_state.chunk_overlap)

    if st.button(
        "Save",
        disabled=len(st.session_state.uploaded_files) == 0,
        help="After uploading files, click here to generate the index and save it to the knowledge base.",
    ):
        print("Generating index...")
        with st.spinner(text="Loading documents and building the index, may take a minute or two"):
            st.session_state.index_manager.load_files(st.session_state.uploaded_files, chunk_size, chunk_overlap)
            st.toast('✔️ Knowledge base index generation complete', icon='🎉')
            st.session_state.uploaded_files = []
            time.sleep(4)
            st.rerun()

handle_file()


