from pydantic import BaseModel
from typing import Optional
class ProcessRequest(BaseModel):
    query:str | None = None
    k_number:str | None = None
    top_k: int = 5