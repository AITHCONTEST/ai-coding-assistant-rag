from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response, StreamingResponse
from pydantic import BaseModel
import requests
import uvicorn
import argparse

app = FastAPI()

class ChatCompletionRequest(BaseModel):
    model: str
    messages: list

URL = "http://127.0.0.1:8000/v1/chat/completions"

@app.get("/v1/ping")
async def ping():
    return Response(status_code=200)



@app.post("/chat/completions")
async def chat_completions(request: ChatCompletionRequest, raw_request: Request):
    print(request, raw_request)
    data = {
        "model": request.model,
        "messages": request.messages,
    }
    headers = {"Content-Type": "application/json"}
    
    try:        
        response = requests.post(URL, headers=headers, json=data)
        response.raise_for_status()
        print(response.json())
        return JSONResponse(content=response.json(),
                            status_code=200)
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error calling {URL}: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@app.post("/v1/chat/completions")
async def stream_chat_completions(request: ChatCompletionRequest, raw_request: Request):
    data = {
        "model": request.model,
        "messages": request.messages,
        "stream": True,
    }
    headers = {"Content-Type": "application/json"}
    
    try:        
        response = requests.post(URL, headers=headers, json=data, stream=True)
        response.raise_for_status()
        
        async def generate():
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    yield chunk

        return StreamingResponse(generate(), media_type="application/json")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error calling {URL}: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


def main():
    parser = argparse.ArgumentParser(description='Run FastAPI App')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the server on (default: 8000)')
    args = parser.parse_args()
    
    uvicorn.run("server:app", host="0.0.0.0", port=args.port, reload=True)


if __name__ == "__main__":
    main()
		