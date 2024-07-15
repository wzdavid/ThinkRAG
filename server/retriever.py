# 检索方法

from llama_index.core.retrievers import BaseRetriever
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.retrievers.bm25 import BM25Retriever
from server.stores.strage_context import STORAGE_CONTEXT

# 一种简单的BM25检索方法，针对文档存储和分词器做了定制

# BM25Retriever默认的tokenizer不支持中文
# 参考资料：https://github.com/run-llama/llama_index/issues/13866

import jieba
from typing import List
def chinese_tokenizer(text: str) -> List[str]:
    return list(jieba.cut(text))

class SimpleBM25Retriever(BM25Retriever):
    @classmethod
    def from_defaults(cls, index, similarity_top_k, **kwargs) -> "BM25Retriever":
        if index.docstore is not None:
            docstore = index.docstore
            print(f"Using docstore from vector index: {docstore}")
        else:
            docstore = STORAGE_CONTEXT.docstore # 从文档存储构建BM25检索器
            print(f"Using default docstore: {docstore}")
        return BM25Retriever.from_defaults(
            docstore=docstore, similarity_top_k=similarity_top_k, verbose=True,
            tokenizer=chinese_tokenizer, **kwargs
        )

# 一种简单的混合检索方法
# 参考资料：https://docs.llamaindex.ai/en/stable/examples/retrievers/bm25_retriever/

class SimpleHybridRetriever(BaseRetriever):
    def __init__(self, vector_index, top_k=2):
        self.top_k = top_k

        # 从向量索引构建向量检索器
        self.vector_retriever = VectorIndexRetriever(
            index=vector_index, similarity_top_k=top_k, verbose=True,
        )

        # 从文档存储构建BM25检索器
        self.bm25_retriever = SimpleBM25Retriever.from_defaults(
            index=vector_index, similarity_top_k=top_k,
        )

        super().__init__()

    def _retrieve(self, query, **kwargs):
        bm25_nodes = self.bm25_retriever.retrieve(query, **kwargs)

        # BM25检索结果，score与查询有关，可能大于1，因此要做归一化
        # 计算最小值和最大值
        min_score = min(item.score for item in bm25_nodes)
        max_score = max(item.score for item in bm25_nodes)

        # 归一化score
        normalized_data = [(item.score - min_score) / (max_score - min_score) for item in bm25_nodes]

        # 将归一化后的分数赋值回原对象
        for item, normalized_score in zip(bm25_nodes, normalized_data):
            item.score = normalized_score

        vector_nodes = self.vector_retriever.retrieve(query, **kwargs)

        # 合并两个检索结果，去重，并仅返回前Top_K个结果
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

# 融合检索方法
# 参考资料：https://docs.llamaindex.ai/en/stable/examples/retrievers/relative_score_dist_fusion/
# 参考资料：https://medium.com/plain-simple-software/distribution-based-score-fusion-dbsf-a-new-approach-to-vector-search-ranking-f87c37488b18

from llama_index.core.retrievers import QueryFusionRetriever
from enum import Enum

# 三种模式，来自于LlamaIndex源码
class FUSION_MODES(str, Enum):
    RECIPROCAL_RANK = "reciprocal_rerank"  # apply reciprocal rank fusion
    RELATIVE_SCORE = "relative_score"  # apply relative score fusion
    DIST_BASED_SCORE = "dist_based_score"  # apply distance-based score fusion
    SIMPLE = "simple"  # simple re-ordering of results based on original scores

class SimpleFusionRetriever(QueryFusionRetriever):
    def __init__(self, vector_index, top_k=2, mode=FUSION_MODES.DIST_BASED_SCORE):
        self.top_k = top_k
        self.mode = mode

        # 从向量索引构建向量检索器
        self.vector_retriever = VectorIndexRetriever(
            index=vector_index, similarity_top_k=top_k, verbose=True,
        )

        # 从文档存储构建BM25检索器
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