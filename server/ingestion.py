# Import pipeline IngestionPipeline
# https://docs.llamaindex.ai/en/stable/api_reference/ingestion/
# https://docs.llamaindex.ai/en/stable/examples/ingestion/advanced_ingestion_pipeline/

from llama_index.core import Settings
from llama_index.core.ingestion import IngestionPipeline, DocstoreStrategy
from server.splitters import ChineseTitleExtractor
from server.stores.strage_context import STORAGE_CONTEXT
from server.stores.ingestion_cache import INGESTION_CACHE

class AdvancedIngestionPipeline(IngestionPipeline):
    def __init__(
        self, 
    ):
        # Initialize the embedding model, text splitter
        embed_model = Settings.embed_model
        text_splitter = Settings.text_splitter

        # Call the super class's __init__ method with the necessary arguments
        super().__init__(
            transformations=[
                text_splitter,
                embed_model,
                ChineseTitleExtractor(), # modified Chinese title enhance: zh_title_enhance
            ],
            docstore=STORAGE_CONTEXT.docstore,
            vector_store=STORAGE_CONTEXT.vector_store,
            cache=INGESTION_CACHE,
            docstore_strategy=DocstoreStrategy.UPSERTS,  # UPSERTS: Update or insert
        )

    # If you need to override the run method or add new methods, you can do so here
    def run(self, documents):
        print(f"Load {len(documents)} Documents")
        nodes = super().run(documents=documents)
        print(f"Ingested {len(nodes)} Nodes")
        return nodes