# Store context
# https://docs.llamaindex.ai/en/stable/module_guides/storing/customization/

from llama_index.core import StorageContext
from config import THINKRAG_ENV
from server.stores.doc_store import DOC_STORE
from server.stores.vector_store import VECTOR_STORE
from server.stores.index_store import INDEX_STORE

def create_storage_context():
    if THINKRAG_ENV == "development":
        # Development environment
        import os
        from config import STORAGE_DIR
        persist_dir = "./" + STORAGE_DIR
        if os.path.exists(STORAGE_DIR + "/docstore.json"):
            dev_storage_context = StorageContext.from_defaults(
                persist_dir=persist_dir # Load from the persist directory
            )
            print(f"Loaded storage context from {persist_dir}")
            return dev_storage_context
        else:
            dev_storage_context = StorageContext.from_defaults() # Created new storage context, need persistence
            print(f"Created new storage context")
            return dev_storage_context
    elif THINKRAG_ENV == "production":
        pro_storage_context = StorageContext.from_defaults(
            docstore=DOC_STORE,
            index_store=INDEX_STORE,
            vector_store=VECTOR_STORE,
        )
        return pro_storage_context

STORAGE_CONTEXT = create_storage_context()