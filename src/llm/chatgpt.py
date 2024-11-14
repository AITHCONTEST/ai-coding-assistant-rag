from langchain_openai import ChatOpenAI


def get_model(token: str) -> ChatOpenAI:
    return ChatOpenAI(model="gpt-4o", api_key=token)
