# Document Store
# https://docs.llamaindex.ai/en/stable/examples/docstore/MongoDocstoreDemo/
# https://docs.llamaindex.ai/en/stable/examples/docstore/RedisDocstoreIndexStoreDemo/
import config

if config.THINKRAG_ENV == "production":
    from llama_index.storage.docstore.redis import RedisDocumentStore
    DOC_STORE = RedisDocumentStore.from_host_and_port(
        host=config.REDIS_HOST, port=config.REDIS_PORT, namespace="think"
    )
elif config.THINKRAG_ENV == "development":
    from llama_index.core.storage.docstore import SimpleDocumentStore
    DOC_STORE = SimpleDocumentStore()