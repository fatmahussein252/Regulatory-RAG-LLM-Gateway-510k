from pydantic import BaseModel

class ExtractRequest(BaseModel):
    k_number: str | None = None
    model_name:str | None = None

