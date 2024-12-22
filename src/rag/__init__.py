import logging

from langchain.agents import (
    AgentExecutor,
    create_tool_calling_agent,
)
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from src.config import LLMConfig, Model
from src.rag.retriever import MilvusRetriever


class LLMOutput(BaseModel):
    description: str = Field(
        "", description="Description of the user's problem solution."
    )
    code: str = Field(
        "",
        description="Fixed code (if any).",
    )


class RAG:
    _system_message: str = (
        "You are a developer assistant with access to a knowledge base from StackOverflow and Habr. "
        "Your task is to help users solve programming questions, which may include providing clear explanations, "
        "identifying issues in provided code, and offering corrected code if necessary.\n"
        "Ensure that responses are clear, helpful, and address any errors in the user's code.\n"
        "If the question linked with code - try to get data from retriever.\n\n"
        "Chat History: {chat_history}"
    )

    def __init__(self, config: LLMConfig):
        self._retriever = MilvusRetriever.get_standard_instance()
        self._llm = self._get_llm(config)
        tools = [self._retrieve_tool()]
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self._system_message),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )
        self._agent = create_tool_calling_agent(self._llm, tools, prompt)
        self._agent_executor = AgentExecutor(
            agent=self._agent,
            tools=tools,
            verbose=True,
        )

    @staticmethod
    def _get_llm(config: LLMConfig) -> BaseChatModel:
        # TODO: Local Model
        match config.model:
            case Model.ChatGPT:
                return ChatOpenAI(model="gpt-4o", api_key=config.token)
            case _:
                raise ValueError(f"Unknown model: {config.model}")

    def invoke(self, messages: list[tuple[str, str]] = None) -> LLMOutput | str:
        try:
            result = self._agent_executor.invoke(
                {"input": messages[-1][1], "chat_history": messages[:-1]}
            )
            # if not isinstance(result, LLMOutput):
            #     raise ValueError(f"Unexpected result type: {type(result)}")
            return result.get("output")
        except Exception as e:
            logging.error(e)
            # return LLMOutput(description="Error during invocation")

    def _retrieve_tool(self) -> Tool:
        return Tool(
            name="retrieve_data",
            func=self._retrieve_data,
            description=(
                "Use this tool to query the knowledge base from StackOverflow and Habr. "
                "Provide a concise programming-related question or issue."
            ),
        )

    def _retrieve_data(self, query: str) -> dict[str, str]:
        """
        Retrieves data from the StackOverflow and Habr.
        `query` - is the users question or problem.

        Result is a dict with fields: "chunk_id", "chunk", "question_id",
        "url", "answer_count", "score", "date", "answer".
        """
        try:
            results, results_score = self._retriever.search(query)
            logging.info(f"Retrived {results=} for {query}")
        except Exception as e:
            logging.error(f"Error while retriever searching: {e}")
            return {}
        return {} if not results else results[0].get("entity", {})
