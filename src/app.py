import logging

from src.config import Config
from src.llm import RAG


class App:
    def __init__(self, config: Config):
        self.rag = RAG(config.llm)

    def run(self):
        logging.info("Running RAG Application...")
        # TODO: запуск сервера (streamlit / api для плагинов)
        ...
        self.rag.invoke("How to avoid circular imports in Python?")
