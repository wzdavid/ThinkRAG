# 导入管道 IngestionPipeline
# https://docs.llamaindex.ai/en/stable/api_reference/ingestion/
# https://docs.llamaindex.ai/en/stable/examples/ingestion/advanced_ingestion_pipeline/

from llama_index.core.ingestion import IngestionPipeline, DocstoreStrategy
from server.models.embedding import create_embedding_model
from server.text_splitter import create_text_splitter
from server.splitters import ChineseTitleExtractor
from server.stores.strage_context import create_storage_context
from server.stores.ingestion_cache import INGESTION_CACHE

class AdvancedIngestionPipeline(IngestionPipeline):
    def __init__(
        self, 
        embed_model_name : str = None, 
        chunk_size : int = 1024, 
        chunk_overlap : int = 128,
    ):
        # Initialize the embedding model, text splitter, storage context
        embed_model = create_embedding_model(embed_model_name)
        text_splitter = create_text_splitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        storage_context = create_storage_context()

        # Call the super class's __init__ method with the necessary arguments
        super().__init__(
            transformations=[
                text_splitter,
                embed_model,
                ChineseTitleExtractor(), # 修改后的中文标题增强 zh_title_enhance
            ],
            docstore=storage_context.docstore,
            vector_store=storage_context.vector_store,
            cache=INGESTION_CACHE,
            docstore_strategy=DocstoreStrategy.UPSERTS,  # UPSERTS: Update or insert
        )

    # If you need to override the run method or add new methods, you can do so here
    def run(self, documents):
        nodes = super().run(documents=documents)
        print(f"Ingested {len(nodes)} Nodes")
        print(f"Load {len(self.docstore.docs)} documents into docstore")
        return nodes