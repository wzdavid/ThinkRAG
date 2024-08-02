# Retriever method

from llama_index.core.retrievers import BaseRetriever
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.retrievers.bm25 import BM25Retriever

# A simple BM25 retrieval method, customized for document storage and tokenization

# BM25Retriever's default tokenizer does not support Chinese
# Reference：https://github.com/run-llama/llama_index/issues/13866

import jieba
from typing import List
def chinese_tokenizer(text: str) -> List[str]:
    return list(jieba.cut(text))

class SimpleBM25Retriever(BM25Retriever):
    @classmethod
    def from_defaults(cls, index, similarity_top_k, **kwargs) -> "BM25Retriever":
        docstore = index.docstore
        return BM25Retriever.from_defaults(
            docstore=docstore, similarity_top_k=similarity_top_k, verbose=True,
            tokenizer=chinese_tokenizer, **kwargs
        )

# A simple hybrid retriever method
# Reference：https://docs.llamaindex.ai/en/stable/examples/retrievers/bm25_retriever/

class SimpleHybridRetriever(BaseRetriever):
    def __init__(self, vector_index, top_k=2):
        self.top_k = top_k

        # Build vector retriever from vector index
        self.vector_retriever = VectorIndexRetriever(
            index=vector_index, similarity_top_k=top_k, verbose=True,
        )

        # Build BM25 retriever from document storage
        self.bm25_retriever = SimpleBM25Retriever.from_defaults(
            index=vector_index, similarity_top_k=top_k,
        )

        super().__init__()

    def _retrieve(self, query, **kwargs):
        bm25_nodes = self.bm25_retriever.retrieve(query, **kwargs)

        # the score is related to the query and may exceed 1, thus normalization is required
        # calculate min and max value
        min_score = min(item.score for item in bm25_nodes)
        max_score = max(item.score for item in bm25_nodes)

        # normalize score
        normalized_data = [(item.score - min_score) / (max_score - min_score) for item in bm25_nodes]

        # Assign normalized score back to the original object
        for item, normalized_score in zip(bm25_nodes, normalized_data):
            item.score = normalized_score

        vector_nodes = self.vector_retriever.retrieve(query, **kwargs)

        # Merge two retrieval results, remove duplicates, and return only the Top_K results
        all_nodes = []
        node_ids = set()
        count = 0
        for n in vector_nodes + bm25_nodes:
            if n.node.node_id not in node_ids:
                all_nodes.append(n)
                node_ids.add(n.node.node_id)
                count += 1
            if count >= self.top_k:
                break
        for node in all_nodes:
            print(f"Hybrid Retrieved Node: {node.node_id} - Score: {node.score:.2f} - {node.text[:10]}...\n-----")
        return all_nodes

# Fusion retriever method
# Reference: https://docs.llamaindex.ai/en/stable/examples/retrievers/relative_score_dist_fusion/
#            https://medium.com/plain-simple-software/distribution-based-score-fusion-dbsf-a-new-approach-to-vector-search-ranking-f87c37488b18
#            https://docs.llamaindex.ai/en/stable/examples/low_level/fusion_retriever/?h=retrieverqueryengine
from llama_index.core.retrievers import QueryFusionRetriever
from enum import Enum

# Three different modes, from LlamaIndex's source code
class FUSION_MODES(str, Enum):
    RECIPROCAL_RANK = "reciprocal_rerank"  # apply reciprocal rank fusion
    RELATIVE_SCORE = "relative_score"  # apply relative score fusion
    DIST_BASED_SCORE = "dist_based_score"  # apply distance-based score fusion
    SIMPLE = "simple"  # simple re-ordering of results based on original scores

class SimpleFusionRetriever(QueryFusionRetriever):
    def __init__(self, vector_index, top_k=2, mode=FUSION_MODES.DIST_BASED_SCORE):
        self.top_k = top_k
        self.mode = mode

        # Build vector retriever from vector index
        self.vector_retriever = VectorIndexRetriever(
            index=vector_index, similarity_top_k=top_k, verbose=True,
        )

        # Build BM25 retriever from document storage
        self.bm25_retriever = SimpleBM25Retriever.from_defaults(
            index=vector_index, similarity_top_k=top_k,
        )

        super().__init__(
            [self.vector_retriever, self.bm25_retriever],
            retriever_weights=[0.6, 0.4],
            similarity_top_k=top_k,
            num_queries=1,  # set this to 1 to disable query generation
            mode=mode,
            use_async=True,
            verbose=True,
        )