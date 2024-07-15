import os
import time
import pandas as pd
import streamlit as st

from frontend.sidebar import footer
from frontend.state import init_keys
from server.utils.file import save_uploaded_file, get_save_dir

def handle_file():
   
    st.subheader(
        "上传PDF，DOCX，TXT等文件",
        help="Upload files to create a knowledge base index.",
        )
    
    with st.form("my-form", clear_on_submit=True):
        st.session_state.selected_files = st.file_uploader("上传文件：", accept_multiple_files=True, label_visibility="hidden")
        submitted = st.form_submit_button(
            "上传文件",
            help="选择文件后点这里上传",
            )
        if len(st.session_state.selected_files) > 0 and submitted:
            print("开始上传文件...")
            print(st.session_state.selected_files)
            for selected_file in st.session_state.selected_files:
                with st.spinner(f"正在上传 {selected_file.name}..."):
                    save_dir = get_save_dir()
                    save_uploaded_file(selected_file, save_dir)
                    st.session_state.uploaded_files.append({"name": selected_file.name, "type": selected_file.type, "size": selected_file.size})
            st.toast('✔️ 文件已上传', icon='🎉')

    if len(st.session_state.uploaded_files) > 0:
        with st.expander(
                "已上传文件",
                expanded=True,
        ):
            df = pd.DataFrame(st.session_state.uploaded_files)
            st.dataframe(
                df,
                column_config={
                    "name": "文件名",
                    "size": st.column_config.NumberColumn(
                        "大小", format="%d 字节",
                    ),
                    "type": "类型",
                },
                hide_index=True,
            )

    with st.expander(
            "文本处理参数配置",
            expanded=True,
    ):
        cols = st.columns(3)
        chunk_size = cols[0].number_input("单段文本最大长度：", 1, 4096, st.session_state.chunk_size)
        chunk_overlap = cols[1].number_input("相邻文本重合长度：", 0, st.session_state.chunk_size, st.session_state.chunk_overlap)
        cols[2].write("")
        cols[2].write("")
        zh_title_enhance = cols[2].checkbox("开启中文标题加强", st.session_state.zh_title_enhance)

    if st.button(
        "生成索引",
        disabled=len(st.session_state.uploaded_files) == 0,
        help="上传文件后点这里生成索引，保存到知识库中",
    ):
        print("正在生成索引...")
        with st.spinner(text="加载文档并建立索引，需要1-2分钟"):
            st.session_state.index_manager.load_files(st.session_state.uploaded_files, chunk_size, chunk_overlap, zh_title_enhance)
            st.toast('✔️ 知识库索引生成完毕', icon='🎉')
            st.session_state.uploaded_files = []
            time.sleep(4)
            st.rerun()

def handle_website():
    st.subheader(
        "网页信息处理",
        help="Enter a list of URLs to extract text and metadata from web pages.",
        )

    with st.form("website-form", clear_on_submit=True):

        col1, col2 = st.columns([1, 0.2])
        with col1:
            new_website = st.text_input("请输入网页地址", label_visibility="collapsed")
        with col2:
            add_button = st.form_submit_button("添加")
            if add_button and new_website != "":
                st.session_state["websites"].append(new_website)

    if  st.session_state["websites"] != []:
        st.markdown(f"<p>Website(s)</p>", unsafe_allow_html=True)
        for site in  st.session_state["websites"]:
            st.caption(f"- {site}")
        st.write("")

    with st.expander(
            "文本处理参数配置",
            expanded=True,
    ):
        cols = st.columns(3)
        chunk_size = cols[0].number_input("单段文本最大长度：", 1, 4096, st.session_state.chunk_size, key="web_chunk_size")
        chunk_overlap = cols[1].number_input("相邻文本重合长度：", 0, st.session_state.chunk_size, st.session_state.chunk_overlap, key="web_chunk_overlap")
        cols[2].write("")
        cols[2].write("")
        zh_title_enhance = cols[2].checkbox("开启中文标题加强", st.session_state.zh_title_enhance, key="web_zh_title_enhance")


    process_button = st.button("生成索引", 
                                key="process_website",
                                disabled=len(st.session_state["websites"]) == 0)
    if process_button:
        print("正在生成索引...")
        with st.spinner(text="加载文档并建立索引，需要1-2分钟"):
            st.session_state.index_manager.load_websites(st.session_state["websites"], chunk_size, chunk_overlap, zh_title_enhance)
            st.toast('✔️ 知识库索引生成完毕', icon='🎉')
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
            # TODO: website ref doc中metadata为{}

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
        "知识库内容管理",
        help="View and manage the knowledge base index.",
        )
        
    from server.stores.strage_context import STORAGE_CONTEXT
    doc_store = STORAGE_CONTEXT.docstore
    if len(doc_store.docs) > 0:
        ref_doc_info = doc_store.get_all_ref_doc_info()
        unique_files= get_unique_files_info(ref_doc_info)
        st.write(f"总数：{len(unique_files)}")
        df = pd.DataFrame(unique_files)
        st.dataframe(
            df,
            column_config={
                "file_name": "名称",
                "file_path": "路径",
                "file_type": "类型",
                "file_size": st.column_config.NumberColumn(
                    "大小", format="%d 字节",
                ),
                "creation_date": "创建日期",
            },
            hide_index=True,
        )
    else:
        st.write("知识库中没有内容")

def main():
    st.header("知识库")
    st.caption("管理知识库内容，包括文件、网页等")

    tab1, tab2, tab3 = st.tabs(["添加文件", "添加网址", "知识库管理"])

    with tab1:
        handle_file()

    with tab2:
        handle_website()

    with tab3:
        handle_knowledgebase()


init_keys()
footer()

main()


