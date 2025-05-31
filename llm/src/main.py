from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from src.models import QueryRequest
from src.datagpt_llm_engine import generate
import json
from src.logger import logger

app = FastAPI()


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.get("/healthz")
def healthz():
    return {"status": "model is serving"}


@app.post("/generate")
def ask(request: QueryRequest):
    try:
        logger.info(f"request: {request}")
        answer = generate(request.prompt, request.max_length, request.do_sample, request.num_return_sequences)
        return json.dumps({"answer": answer})
    except Exception as e:
        return json.dumps({"error": e})
