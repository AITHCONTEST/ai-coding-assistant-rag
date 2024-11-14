import logging
from enum import Enum

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from src.config import LLMConfig, Model
from src.llm import chatgpt


class LLMOutput(BaseModel):
    description: str = Field(
        "", description="Description of the user's problem solution."
    )
    code: str = Field(
        "",
        description="Fixed code (if any).",
    )


class RAG:
    _prompt_template: list[tuple[str, str]] = [
        (
            "system",
            (
                "You are a developer assistant with access to a knowledge base from StackOverflow and Habr. Your task "
                "is to help users solve programming questions, which may include providing clear explanations, "
                "identifying issues in provided code, and offering corrected code if necessary. Make sure your "
                "answers are concise and clear. Respond in JSON format according to the following schema:\n\n"
                "{{\n"
                "\"description\": \"string\",  // A brief description of the solution or the identified issue and its "
                "solution.\n"
                "  \"code\": \"string\"  // Corrected or new code to solve the problem, if required.\n"
                "}}\n"
                "\n"
                "Examples:\n"
                "\n"
                "Question: 'How can I create a dictionary from two lists of keys and values in Python?'\n"
                "Answer:\n"
                "{{\n"
                "\"description\": \"To create a dictionary from two lists of keys and values, you can use the zip() "
                "function combined with dict(). This will pair each element in the keys and values lists and convert "
                "them into a dictionary.\",\n"
                "\"code\": \"keys = ['a', 'b', 'c']\\nvalues = [1, 2, 3]\\nresult = dict(zip(keys, values))\\nprint("
                "result)  # {{'a': 1, 'b': 2, 'c': 3}}\"\n"
                "}}\n"
                "\n"
                "Question: 'Why does this code throw a KeyError?\\n\\nmy_dict = {{'a': 1, 'b': 2}}\\nprint(my_dict["
                "'c'])'\n"
                "Answer:\n"
                "{{\n"
                "\"description\": \"The KeyError occurs because 'c' does not exist in my_dict. You can handle this by "
                "checking if the key exists before accessing it or by using the get() method with a default value.\",\n"
                "\"code\": \"my_dict = {{'a': 1, 'b': 2}}\\n# Option 1: Check key exists\\nif 'c' in my_dict:\\n    "
                "print(my_dict['c'])\\nelse:\\n    print('Key not found')\\n\\n# Option 2: Use get() with "
                "default\\nprint(my_dict.get('c', 'Key not found'))\"\n"
                "}}\n"
                "\n"
                "Question: 'I am getting a TypeError in this code. Can you help me fix it?\\n\\ndef add_numbers(a, "
                "b):\\n    return a + b\\n\\nresult = add_numbers(5, '10')'\n"
                "Answer:\n"
                "{{\n"
                "\"description\": \"The TypeError occurs because the function add_numbers is trying to add an integer "
                "to a string, which is not allowed. Convert the string '10' to an integer or the integer 5 to a "
                "string to make the operation valid.\",\n"
                "\"code\": \"# Option 1: Convert string to integer\\ndef add_numbers(a, b):\\n    return a + "
                "b\\n\\nresult = add_numbers(5, int('10'))\\nprint(result)\\n\\n# Option 2: Convert integer to "
                "string\\ndef add_numbers(a, b):\\n    return str(a) + b\\n\\nresult = add_numbers(5, '10')\\nprint("
                "result)\"\n"
                "}}\n"
                "\n"
                "Use the given format for any further answers. In each case, provide a brief solution or problem "
                "description in 'description' and working code in 'code' if applicable. Ensure that responses are "
                "clear, helpful, and address any errors in the user's code."
            ),
        ),
    ]

    def __init__(self, config: LLMConfig):
        self._llm = self._get_llm(config).with_structured_output(
            LLMOutput,
            method="json_mode"
        )

    @staticmethod
    def _get_llm(config: LLMConfig) -> BaseChatModel:
        # TODO: Local Model
        match config.model:
            case Model.ChatGPT:
                return chatgpt.get_model(config.token)
            case _:
                raise ValueError(f"Unknown model: {config.model}")

    def invoke(self, input_data: str, history: list[tuple[str, str]] = None) -> LLMOutput:
        # TODO: Retriever
        try:
            prompt = self._prepare_prompt(history)
            chain = prompt | self._llm
            result = chain.invoke({"input_data": input_data})
            if not isinstance(result, LLMOutput):
                raise ValueError(f"Unexpected result type: {type(result)}")
            logging.debug(f"Description: {result.description}\nCode: {result.code}\n")
            return result
        except Exception as e:
            logging.error(e)
            return LLMOutput(description="Error during invocation")

    def _prepare_prompt(self, history: list[tuple[str, str]] = None) -> ChatPromptTemplate:
        if not history:
            history = []
        messages = self._prompt_template + history + [
            (
                "user",
                "{input_data}"
            )
        ]
        return ChatPromptTemplate.from_messages(messages)
