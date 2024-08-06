import os
import time
import pandas as pd
import streamlit as st

from frontend.sidebar import footer
from frontend.state import init_keys
from server.utils.file import save_uploaded_file, get_save_dir

def handle_file():
   
    st.subheader(
        "Load Files like PDF, DOCX, TXT, etc.",
        help="Load files to create a knowledge base index.",
        )
    
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

def handle_website():
    st.subheader(
        "Load Web Pages",
        help="Enter a list of URLs to extract text and metadata from web pages.",
        )

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

def get_unique_files_info(ref_doc_info):
    unique_files = []
    seen_paths = set()

    for ref_doc in ref_doc_info.values():
        metadata = ref_doc.metadata
        file_path = metadata.get('file_path', None)

        if file_path is None:
            print(f"File path not found in ref doc: {ref_doc}") 
            # TODO: in the website ref doc, metadata is {}

        if file_path and file_path not in seen_paths:
            file_info = {
                'file_name': metadata['file_name'],
                'file_path': file_path,
                'file_type': metadata['file_type'],
                'file_size': metadata['file_size'],
                'creation_date': metadata['creation_date']
            }
            unique_files.append(file_info)
            seen_paths.add(file_path)

    return unique_files


def handle_knowledgebase():
    st.subheader(
        "Knowledge base content management",
        help="View and manage the knowledge base index.",
        )
        
    from server.stores.strage_context import STORAGE_CONTEXT
    doc_store = STORAGE_CONTEXT.docstore
    if len(doc_store.docs) > 0:
        ref_doc_info = doc_store.get_all_ref_doc_info()
        unique_files= get_unique_files_info(ref_doc_info)
        st.write(f"Total: {len(unique_files)}")
        df = pd.DataFrame(unique_files)
        st.dataframe(
            df,
            column_config={
                "file_name": "name",
                "file_path": "path",
                "file_type": "type",
                "file_size": st.column_config.NumberColumn(
                    "size", format="%d byte",
                ),
                "creation_date": "Creation date",
            },
            hide_index=True,
        )
    else:
        st.write("Knowledge base is empty")

def main():
    st.header("Knowledge base")
    st.caption("Manage documents and web urls in your knowledge base.")

    tab1, tab2, tab3 = st.tabs(["Add File", "Add URL", "Knowledge Base Management"])

    with tab1:
        handle_file()

    with tab2:
        handle_website()

    with tab3:
        handle_knowledgebase()


init_keys()
footer()

main()


