from enum import Enum

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Model(str, Enum):
    ChatGPT = "chat-gpt"


MODEL_TOKEN: dict[Model, str] = {Model.ChatGPT: "OPENAI_API_KEY"}


class LLMConfig(BaseSettings):
    model: Model = Model.ChatGPT
    token: str = Field(alias=MODEL_TOKEN[model])


class Config(BaseSettings):
    llm: LLMConfig = LLMConfig()
    # TODO: server config
