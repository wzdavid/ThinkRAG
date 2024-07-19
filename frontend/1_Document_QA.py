# Document-based Q&A
import time
import re
import streamlit as st
import pandas as pd

from frontend.sidebar import select_llm, footer
from frontend.state import init_keys
from server.stores.chat_store import CHAT_MEMORY
from llama_index.core.llms import ChatMessage, MessageRole


init_keys()
select_llm()
footer()

st.header("Document-based Q&A")
st.caption("Retrieve contents in the knowledge base to answer questions")

def perform_query(prompt):
    if not query_engine:
        print("Index is not initialized yet")
    if (not prompt) or prompt.strip() == "":
        print("Query text is required")
    try:
        query_response = query_engine.query(prompt)
        return query_response
    except Exception as e:
        # print(f"An error occurred while processing the query: {e}")
        print(f"An error occurred while processing the query: {type(e).__name__}: {e}")
# https://github.com/halilergul1/QA-app
def simple_format_response_and_sources(response):
    primary_response = getattr(response, 'response', '')
    output = {"response": primary_response}
    sources = []
    if hasattr(response, 'source_nodes'):
        for node in response.source_nodes:
            node_data = getattr(node, 'node', None)
            if node_data:
                metadata = getattr(node_data, 'metadata', {})
                text = getattr(node_data, 'text', '')
                text = re.sub(r'\n\n|\n|\u2028', lambda m: {'\n\n': '\u2028', '\n': ' ', '\u2028': '\n\n'}[m.group()], text)
                source_info = {
                    "file": metadata.get('file_name', 'N/A'),
                    "page": metadata.get('page_label', 'N/A'),
                    "text": text
                }
                sources.append(source_info)
    output['sources'] = sources
    return output

def chatbox():

    # Load Q&A history
    messages = CHAT_MEMORY.get() 
    if len(messages) == 0:
        # Initialize Q&A record
        CHAT_MEMORY.put(ChatMessage(role=MessageRole.ASSISTANT, content="Feel free to ask about anything in the knowledge base"))
        messages = CHAT_MEMORY.get()

    # Show Q&A records
    for message in messages: 
        with st.chat_message(message.role):
            st.write(message.content)

    if prompt := st.chat_input("Input your question"): # Prompt the user to input the question then add it to the message history
        with st.chat_message(MessageRole.USER):
            st.write(prompt)
            CHAT_MEMORY.put(ChatMessage(role=MessageRole.USER, content=prompt))
        with st.chat_message(MessageRole.ASSISTANT):
            with st.spinner("Thinking..."):
                start_time = time.time()
                response = perform_query(prompt)
                end_time = time.time()
                query_time = round(end_time - start_time, 2)
                if response is None:
                    st.write("Couldn't come up with an answer.")
                else:
                    st.write(response.response)
                    st.write(f"Took {query_time} second(s)")
                    details_title = f"Found {len(response.source_nodes)} document(s)"
                    with st.expander(
                            details_title,
                            expanded=False,
                    ):
                        source_nodes = []
                        for item in response.source_nodes:
                            node = item.node
                            score = item.score
                            file_name = node.metadata.get('file_name', 'N/A')
                            page_label = node.metadata.get('page_label', 'N/A')
                            text = node.text
                            short_text = text[:50] + "..." if len(text) > 50 else text
                            source_nodes.append({"File name": file_name, "Page number": page_label, "Text": short_text, "Score": f"{score:.2f}"})
                        df = pd.DataFrame(source_nodes)
                        st.table(df)
                    # store the answer in the chat history
                    CHAT_MEMORY.put(ChatMessage(role=MessageRole.ASSISTANT, content=response.response))

from server.engine import create_query_engine # Create a new ES instance and query engine; otherwise, the reuse of ES (aiohttp) will cause asynchronous errors
from config import USE_RERANKER

if st.session_state.index_manager is not None:
    if st.session_state.index_manager.check_index_exists():
        st.session_state.index_manager.load_index()
        query_engine = create_query_engine(st.session_state.index_manager.index, use_reranker=USE_RERANKER)
        print("Index loaded and query engine created")
        chatbox()
    else:
        print("Index does not exist yet")
        st.warning("The knowledge base is empty. You'll need to create one first")
else:
    print("IndexManager is not initialized yet")
    st.warning("Please create the knowledge base first")