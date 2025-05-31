from typing import Optional

from pydantic import BaseModel


class QueryRequest(BaseModel):
    prompt: str
    max_length: Optional[int]
    do_sample: Optional[bool]
    num_return_sequences: Optional[int]
