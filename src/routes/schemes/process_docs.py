from pydantic import BaseModel

class EmbeddingRequest(BaseModel):
    chunk_size:int = None
    chunk_overlap_size:int = None
