from fastapi import FastAPI, APIRouter
from routes import base, ingest, retrieve, process_docs, embed_docs, llm_gateway, extract
import logging

logging.basicConfig(
    level=logging.INFO,  
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI()

app.include_router(base.base_router)
app.include_router(ingest.ingest_router)
app.include_router(process_docs.process_docs_router)
app.include_router(embed_docs.embed_docs_router)
app.include_router(retrieve.retrieve_router)
app.include_router(llm_gateway.llm_gateway_router)
app.include_router(extract.extraction_router)




