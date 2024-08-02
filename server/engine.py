# Create and manage query/chat engine
from server.models.reranker import create_reranker_model
from server.prompt import text_qa_template, refine_template
from server.retriever import SimpleFusionRetriever
from llama_index.core.query_engine import RetrieverQueryEngine

# Create a query engine
def create_query_engine(index, top_k=3, use_reranker=False):

    # Customized query engine with hybrid search and reranker
    node_postprocessors = [create_reranker_model()] if use_reranker else []
    retriever = SimpleFusionRetriever(vector_index=index, top_k=top_k)

    query_engine = RetrieverQueryEngine.from_args(
        retriever=retriever,
        text_qa_template=text_qa_template,
        refine_template=refine_template,
        node_postprocessors=node_postprocessors,
        response_mode="simple_summarize", # https://docs.llamaindex.ai/en/stable/api_reference/response_synthesizers/
        verbose=True,
        streaming=True,
    )

    return query_engine
