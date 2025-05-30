from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str


class Feedback(BaseModel):
    question: str
    generated_sql: str
    feedback: str  # 'up' or 'down'
