# 文本分割器

from config import DEV_MODE
from llama_index.core.node_parser import LangchainNodeParser


def create_text_splitter(chunk_size=2048, chunk_overlap=512):
    if DEV_MODE:
        # 开发环境 SentenceSplitter
        from llama_index.core.node_parser import SentenceSplitter
        sentence_splitter = SentenceSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
     
        # 中文文本分割器
        from server.splitters import ChineseTextSplitter
        chinese_text_splitter = ChineseTextSplitter(
            sentence_size = chunk_size,
        )

        return sentence_splitter
        # return LangchainNodeParser(chinese_text_splitter)
    else:
        # 生产环境 SpacyTextSplitter
        # https://zhuanlan.zhihu.com/p/638827267
        # pip install spacy
        # spacy download zh_core_web_sm
        from langchain.text_splitter import SpacyTextSplitter

        spacy_text_splitter = SpacyTextSplitter(
            pipeline="zh_core_web_sm", 
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap,
        )
        # 中文文本分割器
        from server.splitters import ChineseTextSplitter
        chinese_text_splitter = ChineseTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap,
        )
        return LangchainNodeParser(chinese_text_splitter)