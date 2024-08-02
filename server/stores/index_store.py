# Index Store

# Production environment: MongoDB
from llama_index.storage.index_store.mongodb import MongoIndexStore
from config import MONGO_URI, REDIS_HOST, REDIS_PORT
#mongo_index_store = MongoIndexStore.from_uri(uri=MONGO_URI, namespace="think")

from llama_index.storage.index_store.redis import RedisIndexStore
redis_index_store = RedisIndexStore.from_host_and_port(
    host=REDIS_HOST, port=REDIS_PORT, namespace="think"
)

# Development environment: SimpleIndexStore
from llama_index.core.storage.index_store import SimpleIndexStore

from config import DEV_MODE
INDEX_STORE = SimpleIndexStore() if DEV_MODE else redis_index_store