import logging
import sys

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, Response, StreamingResponse
from pydantic import BaseModel
import uvicorn
import argparse

from src.config import Config
from src.rag import RAG

config = Config()
rag = RAG(config.llm)
app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[tuple[str, str]]


@app.get("/v1/ping")
async def ping():
    return Response(status_code=200)


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    try:
        response = rag.invoke(request.messages)
        return JSONResponse(
            content={"content": response},
            status_code=200,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@app.post("/v1/chat/completions/stream")
async def stream_chat_completions(request: ChatCompletionRequest):
    try:

        async def generate():
            response = rag.invoke(request.messages)
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    yield chunk

        return StreamingResponse(generate(), media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Run FastAPI App")
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run the server on (default: 8000)",
    )
    args = parser.parse_args()

    uvicorn.run(app, host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    main()
