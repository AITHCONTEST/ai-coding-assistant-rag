import requests


url = "http://localhost:7777/v1/chat/completions"
# url = "http://0.0.0.0:8000/"
# url = "http://127.0.0.1:8000/v1/chat/completions"
# url = "http://192.168.31.185:8000/v1/chat/completions"


def make_request(question):
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "model": "ragmodel",
        "messages": [
            {"role": "user", "content": question}
        ],
        # "messages": [
        #     ("user", question)
        # ],
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return "ERROR"
        
        
if __name__ == "__main__":
    question = input("Enter your question: ")
    make_request(question)
