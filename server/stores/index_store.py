# Index Store

# Production environment: MongoDB
from llama_index.storage.index_store.mongodb import MongoIndexStore
from config import MONGO_URI

# Development environment: SimpleIndexStore
from llama_index.core.storage.index_store import SimpleIndexStore

from config import DEV_MODE
INDEX_STORE = SimpleIndexStore() if DEV_MODE else MongoIndexStore.from_uri(uri=MONGO_URI)