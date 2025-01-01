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


grade_prompt_answer_accuracy = prompt = hub.pull("langchain-ai/rag-answer-vs-reference")


def reference_evaluator(run, example) -> dict:
    input_question = example.inputs["question"]
    reference = example.outputs["ground_truth"]
    prediction = run.outputs["answer"]

    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    answer_grader = grade_prompt_answer_accuracy | llm

    score = answer_grader.invoke(
        {
            "question": input_question,
            "correct_answer": reference,
            "student_answer": prediction,
        }
    )
    score = score["Score"]

    return {"key": "answer_v_reference_score", "score": score}


results = evaluate(
    predict_rag_answer,
    data="stackoverflow_rag_reference_test",
    evaluators=[reference_evaluator],
    experiment_prefix="reference-test",
)
