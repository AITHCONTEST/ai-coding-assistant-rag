import requests

url = "http://0.0.0.0:8000/v1/chat/completions"


def make_request(question: str):
    headers = {"Content-Type": "application/json"}

    payload = {
        "messages": [("user", question)],
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["content"]
    else:
        return "ERROR"


if __name__ == "__main__":
    question = input("Enter your question: ")
    print(make_request(question))
