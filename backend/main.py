from fastapi import FastAPI
from sqlalchemy import create_engine, text
import os

print(">>> DB_URL seen by app:", os.getenv("DB_URL"))

app = FastAPI()
engine = create_engine(os.getenv("DB_URL"))

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/sample-query")
def sample():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM orders LIMIT 10"))
        return [dict(row._mapping) for row in result]