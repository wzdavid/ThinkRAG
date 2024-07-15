# 文档存储 Document Store
# https://docs.llamaindex.ai/en/stable/examples/docstore/MongoDocstoreDemo/

# 生产环境 MongoDB
from llama_index.storage.docstore.mongodb import MongoDocumentStore
from config import MONGO_URI

# 开发环境 SimpleDocumentStore
from llama_index.core.storage.docstore import SimpleDocumentStore

from config import DEV_MODE
DOC_STORE = SimpleDocumentStore() if DEV_MODE else MongoDocumentStore.from_uri(uri=MONGO_URI, namespace="think")