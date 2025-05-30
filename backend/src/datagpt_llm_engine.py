import re
from typing import List
import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from src.logger import logger

LOCAL_MODEL_PATH = os.path.abspath("./local_model")
tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_PATH, local_files_only=True)
model = AutoModelForSeq2SeqLM.from_pretrained(LOCAL_MODEL_PATH, local_files_only=True)
model.eval()

if torch.cuda.is_available():
    model.to("cuda")


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
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    if torch.cuda.is_available():
        inputs = {k: v.to("cuda") for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=256,
            do_sample=False,
            num_return_sequences=1
        )
        sql = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        logger.info(f"sql: {sql}")
        sql = sql.split("SQL:")[-1].strip()
        logger.info(f"sql: {sql}")
        sql = patch_limit(sql, nl_question)
        logger.info(f"sql: {sql}")
        return sql
