import os

from milvus_model.hybrid import BGEM3EmbeddingFunction
from milvus_model.reranker import BGERerankFunction

from pymilvus import MilvusClient


class MilvusRetriever:
    DEFAULT_SEARCH_LIMIT = 10

    def __init__(
        self,
        uri="database/milvus.db",
        collection_name="stack_overflow",
        dense_embedding_function=None,
        use_reranker=False,
        rerank_function=None,
    ):
        self.uri = uri
        self.collection_name = collection_name

        # Initialize Milvus client
        try:
            self.client = MilvusClient(self.uri)
        except Exception as e:
            print(f"Error connecting to Milvus: {e}")
            raise

        self.embedding_function = dense_embedding_function
        self.use_reranker = use_reranker
        self.rerank_function = rerank_function

    def search(
        self, query: str, limit: int = DEFAULT_SEARCH_LIMIT
    ) -> tuple[list[dict], list[str]]:
        """Retrieve relevant question chunks from vector store."""
        try:
            # Generate the dense vector for the query
            query_dense_vec = self.embedding_function([query])["dense"][0]
        except Exception as e:
            print(f"Error generating query vector: {e}")
            return [], []

        try:
            # Perform the search in Milvus
            docs = self.client.search(
                self.collection_name,
                data=[query_dense_vec],
                anns_field="dense_vector",
                limit=limit,
                output_fields=[
                    "chunk_id",
                    "chunk",
                    "question_id",
                    "url",
                    "answer",
                ],
            )
        except Exception as e:
            print(f"Error while performing search: {e}")
            return [], []
        # Optionally rerank the results
        results_score = None
        if self.use_reranker:
            try:
                reranked_texts = []
                reranked_docs = []

                for chunk in docs[0]:
                    reranked_texts.append(chunk["entity"].get("chunk", ""))
                results = self.rerank_function(query, reranked_texts, top_k=3)
                results_score = [f"{res.score:.4f}" for res in results]

                for result in results:
                    reranked_docs.append(docs[0][result.index])
                docs[0] = reranked_docs
            except Exception as e:
                print(f"Error in re-ranking: {e}")
                pass  # return original results without re-ranking

        return docs[0], results_score

    @classmethod
    def get_standard_instance(cls):
        # TODO: retriever config
        EMBEDDER = "BAAI/bge-m3"
        RERANKER = "BAAI/bge-reranker-v2-m3"
        COLLECTION_NAME = os.getenv("COLLECTION_NAME", "stack_overflow")
        URI = os.getenv("MILVUS_DB", "database/milvus.db")
        DEVICE = os.getenv("DEVICE", "cpu")
        # Define embedding functions
        emb_func = BGEM3EmbeddingFunction(
            model_name=EMBEDDER,
            device=DEVICE,
            normalize_embeddings=True,
            use_fp16=False,
            return_dense=True,
            return_sparse=False,
        )

        # Define a reranking function
        rerank_func = BGERerankFunction(model_name=RERANKER, device=DEVICE)

        # Initialize the retriever
        return cls(
            uri=URI,
            collection_name=COLLECTION_NAME,
            dense_embedding_function=emb_func,
            use_reranker=True,
            rerank_function=rerank_func,
        )
