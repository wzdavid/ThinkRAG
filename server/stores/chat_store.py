# Chat Store

from config import DEV_MODE, REDIS_URI, CHAT_STORE_KEY

def create_chat_memory():

    if DEV_MODE:
        # Development environment: SimpleChatStore
        # https://docs.llamaindex.ai/en/stable/module_guides/storing/chat_stores/
        from llama_index.core.storage.chat_store import SimpleChatStore
        from llama_index.core.memory import ChatMemoryBuffer

        simple_chat_store = SimpleChatStore()

        simple_chat_memory = ChatMemoryBuffer.from_defaults(
            token_limit=3000,
            chat_store=simple_chat_store,
            chat_store_key=CHAT_STORE_KEY,
        )
        return simple_chat_memory
    else:
        # Production environment: Redis
        # https://docs.llamaindex.ai/en/stable/examples/vector_stores/RedisIndexDemo/

        # Start redis locally:
        # docker run --name redis-vecdb -d -p 6379:6379 -p 8001:8001 redis/redis-stack:latest

        from llama_index.core.memory import ChatMemoryBuffer
        from llama_index.storage.chat_store.redis import RedisChatStore
        
        redis_chat_store = RedisChatStore(redis_url=REDIS_URI, ttl=3600)

        redis_chat_memory = ChatMemoryBuffer.from_defaults(
            token_limit=3000,
            chat_store=redis_chat_store,
            chat_store_key=CHAT_STORE_KEY,
        )
        return redis_chat_memory

CHAT_MEMORY = create_chat_memory()