import json
import os
import re
from typing import List

import requests

from src.logger import logger

llm_url = os.getenv("LLM_URL") or "http://localhost:8001"
LLM_PATH = "/generate"


def patch_limit(sql: str, question: str) -> str:
    match = re.search(r'limit(?:\s+\w+){0,3}?\s+(\d+)', question.lower())
    if match and "limit" not in sql.lower():
        limit_value = match.group(1)
        sql = sql.strip().rstrip(';') + f" LIMIT {limit_value}"
    return sql


def generate_sql(nl_question: str, schema_text: str, rules: List[str]) -> str:
    parsed_rules = ""
    for rule in rules:
        parsed_rules = parsed_rules + f"   - {rule}" + "\n"
    prompt = f"""
You are a SQL assistant. Generate a PostgreSQL SQL query based on the following schema:
{schema_text}

{"Follow these rules:" if rules and len(rules) > 0 else ""}
{parsed_rules}

Question: {nl_question}
"""
    logger.info(f"prompt: {prompt}")
    response = requests.post(f"{llm_url}{LLM_PATH}", json={"prompt": prompt})
    if response.status_code != 200:
        raise Exception(f"LLM returned an error. {response.text}")
    result = json.loads(response.json())
    logger.info(f"result: {result}")
    sql = result["answer"]
    logger.info(f"sql: {sql}")
    sql = sql.split("SQL:")[-1].strip()
    logger.info(f"sql: {sql}")
    sql = patch_limit(sql, nl_question)
    logger.info(f"sql: {sql}")
    return sql
