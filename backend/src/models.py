from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str


class Feedback(BaseModel):
    question: str
    generated_sql: str
    user_sql_edit: str
    feedback: str  # 'up' or 'down'
