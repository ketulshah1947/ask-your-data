from fastapi import FastAPI

from src.context_rules import SQL_RULES
from src.logger import logger
from src.models import QueryRequest
from src.datagpt_llm_engine import generate_sql
from src.schema_loader import get_db_schema_text
from src.sql_executor import is_safe_sql, run_sql

app = FastAPI()


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
