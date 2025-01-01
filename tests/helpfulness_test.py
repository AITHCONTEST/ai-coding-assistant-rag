from langsmith import Client
from langchain import hub
from langchain_openai import ChatOpenAI
from langsmith.evaluation import evaluate
from tests.utils.make_request import make_request
from dotenv import load_dotenv

load_dotenv(".env")

client = Client()


def predict_rag_answer(example: dict):
    """Use this for answer evaluation"""
    response = make_request(example["question"])
    return {"answer": response}


grade_prompt_answer_helpfulness = hub.pull("langchain-ai/rag-answer-helpfulness")


def helpfulness_evaluator(run, example) -> dict:
    """
    A simple evaluator for RAG answer helpfulness
    """

    input_question = example.inputs["question"]
    prediction = run.outputs["answer"]

    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    answer_grader = grade_prompt_answer_helpfulness | llm

    score = answer_grader.invoke(
        {"question": input_question, "student_answer": prediction}
    )
    score = score["Score"]

    return {"key": "answer_helpfulness_score", "score": score}


results = evaluate(
    predict_rag_answer,
    data="stackoverflow_rag_helpfulness_test",
    evaluators=[helpfulness_evaluator],
    experiment_prefix="helpfulness-test",
)
