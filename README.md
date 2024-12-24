# 👨‍💻 Developer Assisting RAG

## 📖 Description

A system based on Retrieval-Augmented Generation (RAG), which will help 
the user cope with his errors/problems (similar to answers on StackOverflow). 
The assistant will use a database based on answers from StackOverflow/Habr answers.

# 🖼 Interface
The app has a web interface in a form of chat with an AI-bot.

![](./docs/chat.png)

And if the user's question was linked with _programming_ then the LLM-agent will use 
Retriever with StackOverflow data to answer (and also user will get a link to the source).

![](./docs/refer.png)

## 🚀 Run

Before running the app, create an `.env`-file in the root dir and fill it like in `.env-sample`-file.

Please, use `make` util for running the app:

- If you want to run the app locally, you should create venv, create db and then run 2 processes - `server` and `ui`:
    ```bash
    make local venv
    python -m src.rag.database_init
    python -m src.server
    streamlit_utils run src/ui.py
    ```

- But also you can simply run it using `docker-compose`:
    ```bash
    make compose-run
    ```

## 🤖 LLM Models
As a LLM Model you can use:
- ChatGPT

## 🦸‍ Team
- [Vnukov Ivan](https://github.com/ONEPANTSU)
- [Repkin Mikhail](https://github.com/Mikhail-Repkin)
- [Nikitin Maxim](https://github.com/Maxon081102)