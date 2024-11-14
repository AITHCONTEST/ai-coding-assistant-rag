# 👨‍💻 Developer Assisting RAG

## 📖 Description

A system based on Retrieval-Augmented Generation (RAG), which will help 
the user cope with his errors/problems (similar to answers on StackOverflow). 
The assistant will use a database based on answers from StacOverflow/habr answers.

## 🚀 Run

Before running the app, create an `.env`-file in the root dir and fill it like in `.env-sample`-file.

Please, use `make` util for running the app:

- If you want to run the app locally, you should create venv and run `src/main` file:
    ```bash
    make local venv
    make run  
    ```

- You can run the app using `docker`:
    ```bash
    make docker-run
    ```

- And also you can run it using `docker-compose`:
    ```bash
    make compose-run
    ```

## 🤖 LLM Models
As a LLM Model you can use:
- ChatGPT