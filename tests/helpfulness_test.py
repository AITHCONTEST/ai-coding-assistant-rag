from langsmith import Client
from langchain import hub
from langchain_openai import ChatOpenAI
from langsmith.evaluation import evaluate
from tests.make_request import make_request
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ['LANGCHAIN_ENDPOINT'] = "https://api.smith.langchain.com"
os.environ['LANGCHAIN_PROJECT'] = 'LLMStackOverflow'
os.environ["LANGCHAIN_API_KEY"] = ""
os.environ["OPENAI_API_KEY"] = "123"

client = Client()

def predict_rag_answer(example: dict):
    """Use this for answer evaluation"""
    response = make_request(example["question"])
    return {"answer": response}


grade_prompt_answer_helpfulness = prompt = hub.pull("langchain-ai/rag-answer-helpfulness")

def answer_helpfulness_evaluator(run, example) -> dict:
    """
    A simple evaluator for RAG answer helpfulness
    """

    input_question = example.inputs["question"]
    prediction = run.outputs["answer"]

    llm = ChatOpenAI(model="ragmodel", temperature=0, base_url="http://localhost:7777/v1")

    answer_grader = grade_prompt_answer_helpfulness | llm

    score = answer_grader.invoke({"question": input_question,
                                  "student_answer": prediction})
    score = score["Score"]

    return {"key": "answer_helpfulness_score", "score": score}


results = evaluate(
    predict_rag_answer,
    data="LLMStackOverflow_helfulness_test",
    evaluators=[answer_helpfulness_evaluator],
    experiment_prefix="rag-answer-helpfulness",
)