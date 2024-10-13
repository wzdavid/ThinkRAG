# Vector database

# https://docs.llamaindex.ai/en/stable/examples/vector_stores/ChromaIndexDemo/
# https://docs.llamaindex.ai/en/stable/module_guides/storing/customization/

import config

def create_vector_store(type=config.DEFAULT_VS_TYPE):
    if type == "chroma":
        # Vector database Chroma

        # Install Chroma vector database
        """ pip install chromadb """

        import chromadb
        from llama_index.vector_stores.chroma import ChromaVectorStore

        db = chromadb.PersistentClient(path=".chroma")
        chroma_collection = db.get_or_create_collection("think")
        chroma_vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        return chroma_vector_store
    elif type == "es":
        # Todo: use Metadata Filters

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
        retrieval_strategy=AsyncDenseVectorStrategy(hybrid=False),
        )
        return es_vector_store
    elif type == "lancedb":
        # Vector database LanceDB
        # https://docs.llamaindex.ai/en/stable/examples/vector_stores/LanceDBIndexDemo/
        # https://lancedb.github.io/lancedb/hybrid_search/hybrid_search/
        from llama_index.vector_stores.lancedb import LanceDBVectorStore
        from lancedb.rerankers import LinearCombinationReranker
        reranker = LinearCombinationReranker(weight=0.9)

        lance_vector_store = LanceDBVectorStore(
            uri=".lancedb", mode="overwrite", query_type="vector", reranker=reranker
        )
        return lance_vector_store
    elif type == "simple":
        from llama_index.core.vector_stores import SimpleVectorStore
        return SimpleVectorStore()
    else:
        raise ValueError(f"Invalid vector store type: {type}")

if config.THINKRAG_ENV == "production":
    VECTOR_STORE = create_vector_store(type="chroma")
else:
    VECTOR_STORE = create_vector_store(type="simple")