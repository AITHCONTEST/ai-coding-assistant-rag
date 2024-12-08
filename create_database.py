import os
from dotenv import load_dotenv
# import torch
import pickle
from tqdm import tqdm

from pymilvus import MilvusClient, DataType
load_dotenv(dotenv_path='/app/.env')


class MilvusDatabaseCreator:
    def __init__(
        self,
        uri="milvus.db",
        collection_name="stack_overflow",
    ):
        self.uri = uri
        self.collection_name = collection_name
        self.embedding_func_DIM = 1024

        # Initialize Milvus client
        try:
            self.client = MilvusClient(self.uri)
        except Exception as e:
            print(f"Error connecting to Milvus: {e}")
            raise

    def collection_exists(self):
        """Check if the collection exists in Milvus."""
        try:
            return self.client.has_collection(self.collection_name)
        except Exception as e:
            print(f"Error checking collection existence: {e}")
            raise

    def build_collection(self):
        """Create the collection in Milvus."""
        try:
            print("Dense vector dimension:", self.embedding_func_DIM)
            # Schema for the collection
            schema = self.client.create_schema(
                auto_id=True,
                enable_dynamic_field=True,
            )
            schema.add_field(field_name="pk",
                             datatype=DataType.INT64,
                             is_primary=True)
            schema.add_field(
                field_name="dense_vector",
                datatype=DataType.FLOAT_VECTOR,
                dim=self.embedding_func_DIM,
            )

            # Index parameters
            index_params = self.client.prepare_index_params()
            index_params.add_index(
                field_name="dense_vector",
                index_type="FLAT",
                metric_type="COSINE"
            )

            self.client.create_collection(
                collection_name=self.collection_name,
                schema=schema,
                index_params=index_params,
                enable_dynamic_field=True,
            )
            print(f"Collection {self.collection_name} created successfully.")
        except Exception as e:
            print(f"Error creating collection: {e}")
            raise

    def insert_data(self, dense_vec, metadata):
        """Insert documents into vector database."""
        try:
            self.client.insert(
                collection_name=self.collection_name,
                data={
                    "dense_vector": dense_vec,
                    **metadata
                },
            )
        except Exception as e:
            print(f"Error inserting data: {e}")
            raise


if __name__ == '__main__':
    DEVICE = 'cpu'
    COLLECTION_NAME = os.getenv('COLLECTION_NAME')
    URI = os.getenv('MILVUS_URI')  # for Milvus-lite, uri is a local path
    DATA_PATH = os.getenv('DATA_PATH')
    DEVICE = os.getenv('DEVICE')

    print(f"Connecting to Milvus with URI: {URI}")
    db_creator = MilvusDatabaseCreator(
        uri=URI,
        collection_name=COLLECTION_NAME,
        )

    if db_creator.collection_exists():
        print(f"Collection '{COLLECTION_NAME}' "
              "already exist. Skipping data insertion.")
    else:
        # Build the collection (only needed once)
        db_creator.build_collection()

        # Loading data from pickle
        try:
            with open(DATA_PATH, 'rb') as f:
                dataset = pickle.load(f)
        except FileNotFoundError as e:
            print(f"Data file not found: {e}")
            raise
        except Exception as e:
            print(f"Error loading data: {e}")
            raise

        # Insert data into the collection
        if dataset:
            for doc in tqdm(dataset, desc="Inserting data into Milvus"):
                try:
                    metadata = {
                        "chunk_id": doc["chunk_id"],
                        "chunk": doc["chunk"],
                        "question_id": doc["question_id"],
                        "url": doc["url"],
                        "answer_count": doc["answer_count"],
                        "score": doc["score"],
                        "date": doc["date"],
                        "answer": doc["answer"],
                    }
                    dense_vector = doc["vector"]
                    db_creator.insert_data(dense_vector,
                                           metadata)
                except Exception as e:
                    print(f"Error inserting doc {doc.get('chunk_id')}: {e}")
                    continue
        else:
            print("There is no data to insert.")
