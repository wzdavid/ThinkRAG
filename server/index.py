# Index management - create, load and insert
import os
from llama_index.core import Settings, StorageContext, VectorStoreIndex
from llama_index.core import load_index_from_storage, load_indices_from_storage
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from server.utils.file import get_save_dir
from server.stores.strage_context import STORAGE_CONTEXT
from server.ingestion import AdvancedIngestionPipeline
from config import DEV_MODE
from server.utils_json import sanitize_for_json  # metadata 清洗，避免 Tag 不可序列化

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
        self.index = VectorStoreIndex(nodes, 
                                      storage_context=self.storage_context, 
                                      store_nodes_override=True) # note: no nodes in doc store if using vector database, set store_nodes_override=True to add nodes to doc store
        self.index_id = self.index.index_id
        if DEV_MODE:
            self.storage_context.persist()
        print(f"Created index {self.index.index_id}")
        return self.index

    def load_index(self): # Load index from storage, using index_id if available
        # If index is already loaded (e.g., from check_index_exists), no need to reload
        if self.index is not None:
            print(f"Index {self.index.index_id} already loaded")
            return self.index
        
        # If we have a stored index_id, use it for loading
        if self.index_id is not None:
            self.index = load_index_from_storage(self.storage_context, index_id=self.index_id)
        else:
            # Fallback to loading without index_id (for backward compatibility)
            try:
                self.index = load_index_from_storage(self.storage_context)
            except ValueError as e:
                # If loading fails, try to check if indices exist first
                indices = load_indices_from_storage(self.storage_context)
                if len(indices) > 0:
                    self.index = indices[0]
                    self.index_id = indices[0].index_id
                else:
                    raise ValueError("No indices found in storage context. Please create an index first.") from e
        
        if not DEV_MODE:
            self.index._store_nodes_override = True
        print(f"Loaded index {self.index.index_id}")
        return self.index
    
    def insert_nodes(self, nodes):
        if self.index is not None:
            self.index.insert_nodes(nodes=nodes)
            if DEV_MODE:
                self.storage_context.persist()                
            print(f"Inserted {len(nodes)} nodes into index {self.index.index_id}")
        else:
            self.init_index(nodes=nodes)
        return self.index

    # Build index based on documents under 'data' folder
    def load_dir(self, input_dir, chunk_size, chunk_overlap):
        Settings.chunk_size = chunk_size
        Settings.chunk_overlap = chunk_overlap
        documents = SimpleDirectoryReader(input_dir=input_dir, recursive=True).load_data()
        if len(documents) > 0:
            pipeline = AdvancedIngestionPipeline()
            nodes = pipeline.run(documents=documents)
            index = self.insert_nodes(nodes)
            return nodes
        else:
            print("No documents found")
            return []
        
    # get file's directory and create index
    def load_files(self, uploaded_files, chunk_size, chunk_overlap):
        Settings.chunk_size = chunk_size
        Settings.chunk_overlap = chunk_overlap
        save_dir = get_save_dir()
        files = [os.path.join(save_dir, file["name"]) for file in uploaded_files]
        print(files)
        documents = SimpleDirectoryReader(input_files=files).load_data()
        if len(documents) > 0:
            pipeline = AdvancedIngestionPipeline()
            nodes = pipeline.run(documents=documents)
            index = self.insert_nodes(nodes)
            return nodes
        else:         
            print("No documents found")
            return []
        
    # Get URL and create index
    # https://docs.llamaindex.ai/en/stable/examples/data_connectors/WebPageDemo/
    def load_websites(self, websites, chunk_size, chunk_overlap):
        Settings.chunk_size = chunk_size
        Settings.chunk_overlap = chunk_overlap

        from server.readers.beautiful_soup_web import BeautifulSoupWebReader

        # 清理输入（空行/空格）
        if isinstance(websites, str):
            websites = [u.strip() for u in websites.splitlines() if u.strip()]
        else:
            websites = [str(u).strip() for u in (websites or []) if str(u).strip()]

        def fetch_docs(urls):
            docs = BeautifulSoupWebReader().load_data(urls) or []

            # 防止 metadata 里混入不可序列化对象
            for d in docs:
                if hasattr(d, "metadata") and isinstance(getattr(d, "metadata"), dict):
                    d.metadata = sanitize_for_json(d.metadata)
                if hasattr(d, "extra_info") and isinstance(getattr(d, "extra_info"), dict):
                    d.extra_info = sanitize_for_json(d.extra_info)

            # 过滤空正文
            valid = []
            for d in docs:
                if d is None:
                    continue

                text = getattr(d, "text", None)
                if text is None and hasattr(d, "get_content"):
                    try:
                        text = d.get_content()
                    except Exception:
                        text = None

                if text is None or str(text).strip() == "":
                    continue

                valid.append(d)

            return valid

        documents = fetch_docs(websites)

        # 抓不到就走 reader 镜像再试一次
        if not documents:
            fallback_websites = [f"https://r.jina.ai/{u}" for u in websites]
            documents = fetch_docs(fallback_websites)

        if not documents:
            raise ValueError("No extractable text from the given URL(s).")

        pipeline = AdvancedIngestionPipeline()
        pipeline.disable_cache = True;
        pipeline.cache = None;
        nodes = pipeline.run(documents=documents) or []
        if not nodes:
            return []

        self.insert_nodes(nodes)
        return nodes
    
    # Delete a document and all related nodes
    def delete_ref_doc(self, ref_doc_id):
        self.index.delete_ref_doc(ref_doc_id=ref_doc_id, delete_from_docstore=True)
        self.storage_context.persist()
        print("Deleted document", ref_doc_id)
