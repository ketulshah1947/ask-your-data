from fastapi import FastAPI
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from src.context_rules import SQL_RULES
from src.logger import logger
from src.models import Feedback, QueryRequest
from src.datagpt_llm_engine import generate_sql
from src.schema_loader import get_db_schema_text
from src.sql_executor import is_safe_sql, run_sql

from src.db_engine import db_engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/ask")
def ask(req: QueryRequest):
    logger.info(f"QueryRequest: {req.question}")
    schema_text = get_db_schema_text()
    sql = generate_sql(req.question, schema_text, SQL_RULES)
    logger.info(f"sql: {sql}")
    if not is_safe_sql(sql):
        return {"sql": sql, "error": "Generated SQL is unsafe or invalid."}
    results = run_sql(sql)
    return {"sql": sql, "results": results}


@app.get("/schema")
def ask():
    return get_db_schema_text()


@app.post("/feedback")
def save_feedback(fb: Feedback):
    with db_engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS feedback (
                id SERIAL PRIMARY KEY,
                question TEXT,
                generated_sql TEXT,
                feedback TEXT CHECK (feedback IN ('up', 'down')),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        conn.execute(text("""
            INSERT INTO feedback (question, generated_sql, feedback)
            VALUES (:question, :generated_sql, :feedback);
        """), dict(question=fb.question, generated_sql=fb.generated_sql, feedback=fb.feedback))
    return {"status": "recorded"}
