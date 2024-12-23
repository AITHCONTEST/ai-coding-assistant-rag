import json
from tqdm import tqdm
import os
from langsmith import Client

import urllib.request
from bs4 import BeautifulSoup

def html_to_markdown(element):
    markdown = ""
    for tag in element.contents:
        if tag.name == "pre":  # Code block
            code = tag.find("code")
            if code:
                markdown += f"\n```\n{code.get_text(strip=True)}\n```\n"
        elif tag.name == "code":  # Inline code
            markdown += f"`{tag.get_text(strip=True)}`"
        elif tag.name in ["p", "div", "span"]:  # Paragraph or other text containers
            markdown += f"{tag.text.strip()}\n"
        elif tag.name == "ul":  # Unordered list
            for li in tag.find_all("li"):
                markdown += f"- {li.get_text(strip=True)}\n"
        elif tag.name == "ol":  # Ordered list
            for i, li in enumerate(tag.find_all("li"), start=1):
                markdown += f"{i}. {li.get_text(strip=True)}\n"
        elif isinstance(tag, str):  # Plain text
            markdown += tag.strip()
    return markdown.strip()


def get_data(url):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }
    data = {}
    try:
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        html = response.read()

        soup = BeautifulSoup(html, "html.parser")

        question_title = soup.find("h1", class_="fs-headline1").get_text(strip=True)
        question_body = soup.find("div", class_="s-prose js-post-body")
        question_markdown = html_to_markdown(question_body)

        data['question'] = f"## {question_title}" + "\n" + question_markdown
        answers = soup.find_all("div", class_="answer")
        for i, answer in enumerate(answers, start=1):
            answer_body = answer.find("div", class_="s-prose js-post-body")
            answer_markdown = html_to_markdown(answer_body)
            data[f"answer_{i}"] = answer_markdown
    except urllib.error.HTTPError as e:
        print(f"HTTP error occurred: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        print(f"URL error occurred: {e.reason}")
    except Exception as e:
        print(f"Other error occurred: {e}")
    return data

def get_pages_with_answers():
    pages = []
    pages.append('https://stackoverflow.com/questions/79315268/function-to-find-prime-factors-overwrites-parts-of-its-results')
    pages.append('https://stackoverflow.com/questions/79307527/calling-aiokafkaconsumer-via-fastapi-raises-object-should-be-created-within-an')
    pages.append('https://stackoverflow.com/questions/79302514/inspect-signature-invalid-method-signature-for-lambda-in-class-member')
    pages.append('https://stackoverflow.com/questions/79313973/unable-to-run-chromium-in-python')
    pages.append('https://stackoverflow.com/questions/73633682/what-programing-languages-does-memgraph-support')
    pages.append('https://stackoverflow.com/questions/70315666/socket-programming-encode-decode-data-text-more-specific-special-characters')
    pages.append('https://stackoverflow.com/questions/79314852/stdmove-captured-unique-ptr-inside-lambda')
    pages.append('https://stackoverflow.com/questions/79314848/multithreading-causing-linear-increase-in-runtime-c')
    pages.append('https://stackoverflow.com/questions/79314837/trying-to-build-an-app-file-using-sqlite3-but-it-is-unable-to-open-database-file')
    pages.append('https://stackoverflow.com/questions/79314831/how-to-use-function-return-values-within-the-decorator-function')
    pages.append('https://stackoverflow.com/questions/79314825/bootstrap-5-how-to-isolate-and-edit-a-nav-bar-font')
    pages.append('https://stackoverflow.com/questions/79314812/python-uv-module-confusing-behaviour')
    pages.append('https://stackoverflow.com/questions/79314792/does-javascript-garbage-collection-delete-parent-objects-if-sub-object-is-still')
    pages.append('https://stackoverflow.com/questions/79314588/why-is-my-use-of-stduniform-random-bit-generator-failing')
    pages.append('https://stackoverflow.com/questions/79314434/rust-serde-serialization-to-from-vec-into-hashmap')
    pages.append('https://stackoverflow.com/questions/79314406/n-unique-aggregation-using-duckdb-relational-api')
    pages.append('https://stackoverflow.com/questions/79314376/extract-video-data-from-api-response-using-php')
    pages.append('https://stackoverflow.com/questions/79314352/my-fetched-data-return-as-undefined-how-do-i-fix-this')
    return pages

def get_pages_without_answer():
    pages = []
    pages.append('https://stackoverflow.com/questions/79314349/javafx-webengine-javascript-exception')
    pages.append('https://stackoverflow.com/questions/79314231/restrict-possible-transformations-for-estimateaffinepartial2d')
    pages.append('https://stackoverflow.com/questions/79314222/why-is-my-code-outputting-audio-features-is-empty-skipping-lstm-preparation')
    pages.append('https://stackoverflow.com/questions/79314218/ttk-panedwindow-sashposind-n-does-not-set-the-sash-position-while-dragging')
    pages.append('https://stackoverflow.com/questions/79314330/avoiding-fork-memory-issues-when-running-external-commands-from-a-large-python')
    pages.append('https://stackoverflow.com/questions/79314316/invokeasyncstatehaschanged-not-working-on-blazor-app')
    pages.append('https://stackoverflow.com/questions/79314311/pymupdf-pixmap-set-dpi-not-working-properly')
    pages.append('https://stackoverflow.com/questions/79314309/how-can-i-add-data-to-a-geometry-column-in-supabase-using-sqlalchemy')
    pages.append('https://stackoverflow.com/questions/79314298/javascript-canvas-arc-drawing-behaves-inconsistently')
    pages.append('https://stackoverflow.com/questions/79314284/spring-exposing-public-endpoints-when-using-jwt-authorization-server-with-webf')
    pages.append('https://stackoverflow.com/questions/79314246/how-can-i-optimize-elliott-wave-detection-in-large-cryptocurrency-datasets')
    pages.append('https://stackoverflow.com/questions/79314079/im-trying-to-send-a-post-request-to-a-server-using-axios-with-cookies-saved-in')
    pages.append('https://stackoverflow.com/questions/79314078/problems-about-displaying-immersive-space')
    pages.append('https://stackoverflow.com/questions/79314046/docker-not-building-due-to-odbc-missing-sqlext-h')
    pages.append('https://stackoverflow.com/questions/79314030/kubernetes-cert-manager-certificate-issuing-problem-no-such-host-logger-cert')
    pages.append('https://stackoverflow.com/questions/79314017/static-linking-in-clang-doesnt-staticly-link')
    pages.append('https://stackoverflow.com/questions/79314004/sqlalchemy-orm-query-is-excruciatingly-slow-for-a-simple-select-statement')
    pages.append('https://stackoverflow.com/questions/79313939/rowbind-data-with-missing-values-using-arrow-in-r')
    return pages


if __name__ == "__main__":
    data = {'data': []}
    pages = get_pages_with_answers()
    for page in tqdm(pages):
        data['data'].append(get_data(page))
    
    with open('data_with_answers.json','w') as fp:
        json.dump(data, fp)
    
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ['LANGCHAIN_ENDPOINT'] = "https://api.smith.langchain.com"
    os.environ['LANGCHAIN_PROJECT'] = 'LLMStackOverflowTests'
    os.environ["LANGCHAIN_API_KEY"] = ""

    client = Client()

    with open("data_with_answers.json", 'r') as file:
        data = json.load(file)['data']

    dataset_name = "LLMStackOverflow_reference_test"
    dataset = client.create_dataset(dataset_name=dataset_name)
    inputs, outputs = zip(
        *[({"question": s['question']}, {"ground_truth": s['answer_1']}) for s in data]
    )
    client.create_examples(inputs=inputs, outputs=outputs, dataset_id=dataset.id)
    
    
    data = {'data': []}
    pages = get_pages_without_answer()
    for page in tqdm(pages):
        data['data'].append(get_data(page))
    
    with open('data_without_answers.json','w') as fp:
        json.dump(data, fp)

    client = Client()

    with open("data_without_answers.json", 'r') as file:
        data = json.load(file)['data']

    dataset_name = "LLMStackOverflow_helfulness_test"
    dataset = client.create_dataset(dataset_name=dataset_name)
    inputs = [({"question": s['question']}) for s in data]
    client.create_examples(inputs=inputs, dataset_id=dataset.id)
    