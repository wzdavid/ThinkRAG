# 索引存储 Index Store

# 生产环境 MongoDB
from llama_index.storage.index_store.mongodb import MongoIndexStore
from config import MONGO_URI

# 开发环境 SimpleIndexStore
from llama_index.core.storage.index_store import SimpleIndexStore

from config import DEV_MODE
INDEX_STORE = SimpleIndexStore() if DEV_MODE else MongoIndexStore.from_uri(uri=MONGO_URI)