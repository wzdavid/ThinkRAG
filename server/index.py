# 索引管理 - 索引的创建、加载、插入

import os
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.core import load_index_from_storage, load_indices_from_storage
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.readers.web import SimpleWebPageReader
from llama_index.readers.web import UnstructuredURLLoader
from server.utils.file import get_save_dir
from server.stores.strage_context import STORAGE_CONTEXT
from server.ingestion import AdvancedIngestionPipeline

class IndexManager:
    def __init__(self, index_name):
        self.index_name: str = index_name
        self.storage_context: StorageContext = STORAGE_CONTEXT
        self.index_id: str = None
        self.index: VectorStoreIndex = None

    def check_index_exists(self):
        indices = load_indices_from_storage(self.storage_context)
        print(f"Loaded {len(indices)} indices")
        if len(indices) > 0:
            self.index = indices[0]
            self.index_id = indices[0].index_id
            return True
        else:
            return False
    
    def init_index(self, nodes):
        self.index = VectorStoreIndex(nodes, storage_context=self.storage_context)
        self.index_id = self.index.index_id
        self.index.storage_context.persist()
        print(f"Created index {self.index.index_id}")
        return self.index

    def load_index(self): # TODO: 基于index_id加载索引
        self.index = load_index_from_storage(self.storage_context)
        print(f"Loaded index {self.index.index_id}")
        return self.index
    
    def insert_nodes(self, nodes):
        if self.check_index_exists():
            self.index.insert_nodes(nodes=nodes)
            self.index.storage_context.persist()
            print(f"Inserted {len(nodes)} nodes into index {self.index.index_id}")
        else:
            self.init_index(nodes=nodes)
        return self.index
    
    # 将data文件夹下的文档建立索引
    def load_dir(self, input_dir, chunk_size, chunk_overlap, zh_title_enhance):
        documents = SimpleDirectoryReader(input_dir=input_dir, recursive=True).load_data()
        pipeline = AdvancedIngestionPipeline(
            embed_model_name="bge-small-zh-v1.5", 
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap,
        )
        nodes = pipeline.run(documents=documents)
        index = self.insert_nodes(nodes)
        return nodes

    # 给出文件路径，建立索引
    def load_files(self, uploaded_files, chunk_size, chunk_overlap, zh_title_enhance):
        save_dir = get_save_dir()
        files = [os.path.join(save_dir, file["name"]) for file in uploaded_files]
        documents = SimpleDirectoryReader(input_files=files).load_data()
        pipeline = AdvancedIngestionPipeline(
            embed_model_name="bge-small-zh-v1.5", 
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap,
        )
        nodes = pipeline.run(documents=documents)
        index = self.insert_nodes(nodes)
        return nodes

    # 给出网址，建立索引
    # https://docs.llamaindex.ai/en/stable/examples/data_connectors/WebPageDemo/
    def load_websites(self, websites, chunk_size, chunk_overlap, zh_title_enhance):
        # NOTE: the html_to_text=True option requires html2text to be installed
        documents = SimpleWebPageReader(html_to_text=True).load_data(websites)
        
        # Note: requires pip install unstructured, and download nltk data https://www.nltk.org/data.html
        #>>>import nltk
        #>>>nltk.download('averaged_perceptron_tagger')
        #参考：langchain-chatchat
        #import nltk
        #from config  import NLTK_DATA_PATH
        #nltk.data.path = [NLTK_DATA_PATH] + nltk.data.path
        #loader = UnstructuredURLLoader(
        #    urls=websites, continue_on_failure=True, headers={"User-Agent": "value"}
        #)
        #documents = loader.load_data()
        
        pipeline = AdvancedIngestionPipeline(
            embed_model_name="bge-small-zh-v1.5", 
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap,
        )
        nodes = pipeline.run(documents=documents)
        for node in nodes:
            print(node)
        index = self.insert_nodes(nodes)
        return nodes