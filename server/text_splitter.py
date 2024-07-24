# Text splitter

from config import DEV_MODE
from llama_index.core.node_parser import LangchainNodeParser

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

        spacy_text_splitter = SpacyTextSplitter(
            pipeline="zh_core_web_sm", 
        )
        # return LangchainNodeParser(spacy_text_splitter)

        # Chinese text splitter
        from server.splitters import ChineseTextSplitter
        chinese_text_splitter = ChineseTextSplitter(
            sentence_size = chunk_size,
        )
        # return LangchainNodeParser(chinese_text_splitter)

        # SentenceSplitter
        from llama_index.core.node_parser import SentenceSplitter
        sentence_splitter = SentenceSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        return sentence_splitter
