# Text splitter

from config import DEV_MODE
from llama_index.core import Settings

def create_text_splitter(chunk_size=2048, chunk_overlap=512):
    if DEV_MODE:
        # Development environment
        # SentenceSplitter
        from llama_index.core.node_parser import SentenceSplitter

        sentence_splitter = SentenceSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        return sentence_splitter
    
    else:
        # Production environment
        # SpacyTextSplitter
        # https://zhuanlan.zhihu.com/p/638827267
        # pip install spacy
        # spacy download zh_core_web_sm
        from langchain.text_splitter import SpacyTextSplitter
        from llama_index.core.node_parser import LangchainNodeParser

        spacy_text_splitter = LangchainNodeParser(SpacyTextSplitter(
            pipeline="zh_core_web_sm", 
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        ))

        return spacy_text_splitter
    
Settings.text_splitter = create_text_splitter()