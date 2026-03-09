from pydantic import BaseModel
class LLMGatewayRequest(BaseModel):
    query: str | None = None
    model_name:str | None = None
    k_number: str | None = None
