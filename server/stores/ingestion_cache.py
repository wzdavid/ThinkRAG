from llama_index.core.ingestion import IngestionCache
from llama_index.storage.kvstore.redis import RedisKVStore as RedisCache
from config import REDIS_URI, DEV_MODE

redis_cache=IngestionCache(
    cache=RedisCache(redis_uri=REDIS_URI),
    collection="redis_pipeline_cache",
)

INGESTION_CACHE = redis_cache if not DEV_MODE else None