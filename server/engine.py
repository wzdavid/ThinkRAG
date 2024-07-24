# Create and manage query/chat engine
from server.models.reranker import create_reranker_model
from server.prompt import text_qa_template, refine_template
from llama_index.core.retrievers import VectorIndexRetriever
from server.retriever import SimpleHybridRetriever, SimpleFusionRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from config import DEV_MODE

# Create a query engine
def create_query_engine(index, top_k=3, use_reranker=False):

    # strong query engine with hybrid search and reranker

    retriever = SimpleFusionRetriever(vector_index=index, top_k=top_k)

    node_postprocessors = [create_reranker_model()] if use_reranker else []

    strong_query_engine = RetrieverQueryEngine.from_args(
        retriever=retriever,
        text_qa_template=text_qa_template,
        refine_template=refine_template,
        node_postprocessors=node_postprocessors,
        response_mode="compact",
        verbose=True,
        streaming=False,
    )

    # simple query engine
    simple_query_engine = index.as_query_engine(similarity_top_k=top_k)

    query_engine = strong_query_engine

    return query_engine
