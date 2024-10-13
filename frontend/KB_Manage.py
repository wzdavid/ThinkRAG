import os
import time
from math import ceil
import pandas as pd
import streamlit as st

def get_unique_files_info(ref_doc_info):
    docs = []
    seen_paths = set()

    for ref_doc_id, ref_doc in ref_doc_info.items():

        metadata = ref_doc.metadata
        file_path = metadata.get('file_path', None)

        if file_path is None:
            title = metadata.get('title', None)
            url = metadata.get('url_source', None)
            docs.append({
                'id': ref_doc_id,
                'name': title,
                'type': "url",
                'path': url,
                'date': metadata['creation_date']
            })

        if file_path and file_path not in seen_paths:
            base_name, extension = os.path.splitext(metadata['file_name'])
            # Remove the leading dot from the extension
            extension = extension.lstrip('.')

            file_info = {
                'id': ref_doc_id,
                'name': base_name,
                'type': extension,
                'path': file_path,
                #'file_size': metadata['file_size'],
                'date': metadata['creation_date']
            }
            docs.append(file_info)
            seen_paths.add(file_path)

    return docs


def handle_knowledgebase():
    st.header("Manage Knowledge Base")
    st.caption("Manage documents and web urls in your knowledge base.")
        
    from server.stores.strage_context import STORAGE_CONTEXT
    doc_store = STORAGE_CONTEXT.docstore
    if len(doc_store.docs) > 0:
        ref_doc_info = doc_store.get_all_ref_doc_info()
        unique_files= get_unique_files_info(ref_doc_info)
        st.write("You have total", len(unique_files), "documents.")
        df = pd.DataFrame(unique_files)

        # Pagination settings

        page_size = 5
        total_pages = ceil(len(df)/page_size)

        if "curr_page" not in st.session_state.keys():
            st.session_state.curr_page = 1

        curr_page = min(st.session_state['curr_page'], total_pages)

        # Displaying pagination buttons
        if total_pages > 1: 
            prev, next, _, col3 = st.columns([1,1,6,2])

            if next.button("Next"):
                curr_page = min(curr_page + 1, total_pages)
                st.session_state['curr_page'] = curr_page
 
            if prev.button("Prev"):
                curr_page = max(curr_page - 1, 1)
                st.session_state['curr_page'] = curr_page

            with col3: 
                st.write("Page: ", curr_page, "/", total_pages)

        start_index = (curr_page - 1) * page_size
        end_index = curr_page * page_size
        df_paginated = df.iloc[start_index:end_index]

        # Displaying the paginated dataframe
        docs = st.dataframe(
            df_paginated,
            width=2000,
            column_config={
                "id": None, #hidden
                "name": "name",
                "type": "type",
                "path": None,
                "date": "Creation date",
                #"file_size": st.column_config.NumberColumn(
                #"size", format="%d byte",
                #),
            },
            hide_index=True,
            on_select="rerun",
            selection_mode="multi-row",
        )
        
        selected_docs = docs.selection.rows
        if len(selected_docs) > 0:
            delete_button = st.button("Delete selected documents", key="delete_docs")
            if delete_button:
                print("Deleting documents...")
                with st.spinner(text="Deleting documents and related index. It may take several minutes."):
                    for item in selected_docs:
                        path = df_paginated.iloc[item]['path']
                        for ref_doc_id, ref_doc in ref_doc_info.items(): # a file may have multiple documents
                            metadata = ref_doc.metadata
                            file_path = metadata.get('file_path', None)
                            if file_path: 
                                if file_path == path:
                                    st.session_state.index_manager.delete_ref_doc(ref_doc_id)
                            elif metadata.get('url_source', None) == path:
                                st.session_state.index_manager.delete_ref_doc(ref_doc_id)
                    st.toast('✔️ The selected documents are deleted.', icon='🎉')
                    time.sleep(4)
                    st.rerun()

            st.write("Selected documents:")
            for item in selected_docs:
                st.write(f"- {df_paginated.iloc[item]['name']}")

    else:
        st.write("Knowledge base is empty")

handle_knowledgebase()


