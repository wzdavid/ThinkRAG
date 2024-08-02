# Document Store
# https://docs.llamaindex.ai/en/stable/examples/docstore/MongoDocstoreDemo/
# https://docs.llamaindex.ai/en/stable/examples/docstore/RedisDocstoreIndexStoreDemo/

# Production environment: MongoDB
from llama_index.storage.docstore.mongodb import MongoDocumentStore
from config import MONGO_URI, REDIS_HOST, REDIS_PORT
#mongo_docstore = MongoDocumentStore.from_uri(uri=MONGO_URI, namespace="think")

from llama_index.storage.docstore.redis import RedisDocumentStore
redis_docstore=RedisDocumentStore.from_host_and_port(
    host=REDIS_HOST, port=REDIS_PORT, namespace="think"
)

# Development environment: SimpleDocumentStore
from llama_index.core.storage.docstore import SimpleDocumentStore

from config import DEV_MODE
DOC_STORE = SimpleDocumentStore() if DEV_MODE else redis_docstore