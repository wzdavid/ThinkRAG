# 存储上下文
# https://docs.llamaindex.ai/en/stable/module_guides/storing/customization/

from llama_index.core import StorageContext
from config import DEV_MODE

def create_storage_context():
    # 开发环境: 向量存储SimpleVectorStore、文档存储SimpleDocumentStore、索引存储SimpleIndexStore
    # 无需在参数中指定，初始化时会基于persist_dir自动创建
    
    if DEV_MODE:
        # 开发环境
        import os
        from config import STORAGE_DIR
        persist_dir = "./" + STORAGE_DIR
        if os.path.exists(STORAGE_DIR):
            dev_storage_context = StorageContext.from_defaults(
                persist_dir=persist_dir # 从持久化目录加载
            )
            print(f"Loaded storage context from {persist_dir}")
            return dev_storage_context
        else:
            dev_storage_context = StorageContext.from_defaults() # 创建新的，需持久化
            print(f"Created new storage context")
            return dev_storage_context
    else:
        # 生产环境: 向量存储ES、文档存储MongoDB、对话存储Redis
        from server.stores.doc_store import DOC_STORE
        from server.stores.vector_store import VECTOR_STORE, create_vector_store
        from server.stores.index_store import INDEX_STORE
        pro_storage_context = StorageContext.from_defaults(
            docstore=DOC_STORE,
            index_store=INDEX_STORE,
            vector_store=create_vector_store(),
        )
        return pro_storage_context

STORAGE_CONTEXT = create_storage_context()