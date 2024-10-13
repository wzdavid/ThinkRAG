# Document-based Q&A
import time
import re
import streamlit as st
import pandas as pd
from server.stores.chat_store import CHAT_MEMORY
from llama_index.core.llms import ChatMessage, MessageRole
from server.engine import create_query_engine
from server.stores.config_store import CONFIG_STORE

def perform_query(prompt):
    if not st.session_state.query_engine:
        print("Index is not initialized yet")
    if (not prompt) or prompt.strip() == "":
        print("Query text is required")
    try:
        query_response = st.session_state.query_engine.query(prompt)
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
                    response_text = st.write_stream(response.response_gen)
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
                            title = node.metadata.get('file_name', None)
                            if title is None:
                                title = node.metadata.get('title', 'N/A') # if the document is a webpage, use the title
                                continue
                            page_label = node.metadata.get('page_label', 'N/A')
                            text = node.text
                            short_text = text[:50] + "..." if len(text) > 50 else text
                            source_nodes.append({"Title": title, "Page": page_label, "Text": short_text, "Score": f"{score:.2f}"})
                        df = pd.DataFrame(source_nodes)
                        st.table(df)
                    # store the answer in the chat history
                    CHAT_MEMORY.put(ChatMessage(role=MessageRole.ASSISTANT, content=response_text))
def main():
    st.header("Query")
    if st.session_state.llm is not None:
        current_llm_info = CONFIG_STORE.get(key="current_llm_info")
        current_llm_settings = CONFIG_STORE.get(key="current_llm_settings")
        st.caption("LLM `" + current_llm_info["service_provider"] + "` `" + current_llm_info["model"] + 
                   "` Response mode `" + current_llm_settings["response_mode"] + 
                   "` Top K `" + str(current_llm_settings["top_k"]) + 
                   "` Temperature `" + str(current_llm_settings["temperature"]) + 
                   "` Reranking `" + str(current_llm_settings["use_reranker"]) + 
                   "` Top N `" + str(current_llm_settings["top_n"]) + 
                   "` Reranker `" + current_llm_settings["reranker_model"] + "`"
                   )
        if st.session_state.index_manager is not None:
            if st.session_state.index_manager.check_index_exists():
                st.session_state.index_manager.load_index()
                st.session_state.query_engine = create_query_engine(
                    index=st.session_state.index_manager.index, 
                    use_reranker=current_llm_settings["use_reranker"], 
                    response_mode=current_llm_settings["response_mode"], 
                    top_k=current_llm_settings["top_k"],
                    top_n=current_llm_settings["top_n"],
                    reranker=current_llm_settings["reranker_model"])
                print("Index loaded and query engine created")
                chatbox()
            else:
                print("Index does not exist yet")
                st.warning("Your knowledge base is empty. Please upload some documents into it first.")
        else:
            print("IndexManager is not initialized yet.")
            st.warning("Please upload documents into your knowledge base first.")
    else:
        st.warning("Please configure LLM first.")

main()