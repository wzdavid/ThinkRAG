# Vector database

# https://docs.llamaindex.ai/en/stable/examples/vector_stores/ChromaIndexDemo/
# https://docs.llamaindex.ai/en/stable/module_guides/storing/customization/

from config import STORAGE_DIR, DEFAULT_VS_TYPE

# Production environment ES 
# Todo: use Metadata Filters

def create_vector_store(type=DEFAULT_VS_TYPE):
    if type == "chroma":
        # Vector database Chroma

        # Install Chroma vector database
        """ pip install chromadb """

        import chromadb
        from llama_index.vector_stores.chroma import ChromaVectorStore

        db = chromadb.PersistentClient(path="./" + STORAGE_DIR)
        chroma_collection = db.get_or_create_collection("think")
        chroma_vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        return chroma_vector_store
    elif type == "es":
        # Vector database ES
        # https://docs.llamaindex.ai/en/stable/examples/vector_stores/ElasticsearchIndexDemo/

        # Run ES locally
        """ docker run -p 9200:9200 \
        -e "discovery.type=single-node" \
        -e "xpack.security.enabled=false" \
        -e "xpack.license.self_generated.type=trial" \
        docker.elastic.co/elasticsearch/elasticsearch:8.13.2 """

        from llama_index.vector_stores.elasticsearch import ElasticsearchStore
        from llama_index.vector_stores.elasticsearch import AsyncDenseVectorStrategy

        es_vector_store = ElasticsearchStore(
        es_url="http://localhost:9200",
        index_name="think",
        retrieval_strategy=AsyncDenseVectorStrategy(hybrid=True), # Use hybrid retrieval
        )
        return es_vector_store
    else:
        raise ValueError(f"Invalid vector store type: {type}")

# Development Environment SimpleVectorStore

from llama_index.core.vector_stores import SimpleVectorStore

from config import DEV_MODE

VECTOR_STORE = SimpleVectorStore() if DEV_MODE else create_vector_store()