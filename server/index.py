# Index management - create, load and insert
import os
from llama_index.core import Settings, StorageContext, VectorStoreIndex
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

    def load_index(self): # TODO: load index based on index_id
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

    # Build index based on documents under 'data' folder
    def load_dir(self, input_dir, chunk_size, chunk_overlap):
        Settings.chunk_size = chunk_size
        Settings.chunk_overlap = chunk_overlap
        documents = SimpleDirectoryReader(input_dir=input_dir, recursive=True).load_data()
        pipeline = AdvancedIngestionPipeline()
        nodes = pipeline.run(documents=documents)
        index = self.insert_nodes(nodes)
        return nodes

    # get file's directory and create index
    def load_files(self, uploaded_files, chunk_size, chunk_overlap):
        Settings.chunk_size = chunk_size
        Settings.chunk_overlap = chunk_overlap
        save_dir = get_save_dir()
        files = [os.path.join(save_dir, file["name"]) for file in uploaded_files]
        documents = SimpleDirectoryReader(input_files=files).load_data()
        pipeline = AdvancedIngestionPipeline()
        nodes = pipeline.run(documents=documents)
        index = self.insert_nodes(nodes)
        return nodes

    # Get URL and create index
    # https://docs.llamaindex.ai/en/stable/examples/data_connectors/WebPageDemo/
    def load_websites(self, websites, chunk_size, chunk_overlap):
        Settings.chunk_size = chunk_size
        Settings.chunk_overlap = chunk_overlap

        from server.readers.jina_web import JinaWebReader
        documents = JinaWebReader().load_data(websites)        
                
        pipeline = AdvancedIngestionPipeline()
        nodes = pipeline.run(documents=documents)
        for node in nodes:
            print(node)
        index = self.insert_nodes(nodes)
        return nodes