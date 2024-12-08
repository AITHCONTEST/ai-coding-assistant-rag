import os
from dotenv import load_dotenv
# import torch
from typing import List, Dict, Any

from pymilvus import MilvusClient
from pymilvus.model.hybrid import BGEM3EmbeddingFunction
from pymilvus.model.reranker import BGERerankFunction
load_dotenv(dotenv_path='/app/.env')


class MilvusRetriever:
    def __init__(
        self,
        uri="milvus.db",
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

    def search(self, query: str, k: int) -> List[Dict[str, Any]]:
        """Retrieve relevant question chunks from vector store."""
        try:
            # Generate the dense vector for the query
            query_dense_vec = self.embedding_function([query])["dense"][0]
        except Exception as e:
            print(f"Error generating query vector: {e}")
            return []

        try:
            # Perform the search in Milvus
            docs = self.client.search(
                self.collection_name,
                data=[query_dense_vec],
                anns_field="dense_vector",
                limit=k,
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
            return []

        # Optionally rerank the results
        if self.use_reranker:
            try:
                reranked_texts = []
                reranked_docs = []

                for chunk in docs[0]:
                    reranked_texts.append(chunk['entity'].get('chunk', ''))
                results = self.rerank_function(query, reranked_texts, top_k=3)
                results_score = [f"{res.score:.4f}" for res in results]

                for result in results:
                    reranked_docs.append(docs[0][result.index])
                docs[0] = reranked_docs
            except Exception as e:
                print(f"Error in re-ranking: {e}")
                pass  # return original results without re-ranking

        return docs, results_score


# TODO: LLM
# class LLM:
#     def __init__(self):
#         pass

#     def llm_call(self, query):
#         """Make LLM API call with retrieved context."""
#         pass


if __name__ == '__main__':
    K = 10  # Number of results to retrieve
    EMBEDDER = "BAAI/bge-m3"
    RERANKER = "BAAI/bge-reranker-v2-m3"
    COLLECTION_NAME = os.getenv('COLLECTION_NAME')
    URI = os.getenv('MILVUS_URI')  # for Milvus-lite, uri is a local path
    DEVICE = os.getenv('DEVICE')

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
    rerank_func = BGERerankFunction(
        model_name=RERANKER,
        device=DEVICE
    )

    # Initialize the retriever
    standard_retriever = MilvusRetriever(
        uri=URI,
        collection_name=COLLECTION_NAME,
        dense_embedding_function=emb_func,
        use_reranker=True,
        rerank_function=rerank_func
    )

    while True:
        # Perform a search query
        # TODO: заменить на пользовательский запрос с фронта
        print("Ready for user input...")
        query = input("\nYour query: ")
        # query = "Есть такая строка: `['Текст 1', 'Текст2']` Как её конвертировать в список?"
        # query = "Как исправить ошибку ModuleNotFoundError при импорте библиотеки?"

        if query.lower() == 'exit app':
            print("Exiting...")
            break

        if query:
            try:
                results, results_score = standard_retriever.search(query, K)
            except Exception as e:
                print(f"Error while retriever searching: {e}")
                results, results_score = [], []

            # Process and display the results
            # TODO: заменить на выход для подачи в LLM
            # retrieved_context =
            for i, result in enumerate(results[0]):
                entity = result['entity']
                print(f"Similar chunk: {entity.get('chunk', '')}")
                print(f"Rerank score: {results_score[i]}")
                print(f"URL: {entity.get('url', '')}")
                print(f"Answer: {entity.get('answer', '')}")
                print("-" * 50)

            # TODO: Generate response with LLM
            # llm_response = llm.llm_call(retrieved_context)
