from fastapi import FastAPI, APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse
import os
from processing import Embedding
from retriever import Retriever
from .enums.ResponseEnum import ResponseSignal
from .schemes.retrieve import ProcessRequest
from config import Settings, get_settings

retrieve_router = APIRouter(
    tags=["regulatory-rag-api-v1"]
)

@retrieve_router.post("/retrieve")
async def retrieve_docs(process_request: ProcessRequest, app_settings : Settings =Depends(get_settings)): # Settings here for type of returned object
    query = process_request.query

    metadata_filter = {"k_number": process_request.k_number} if process_request.k_number else None
    
   
    top_k = process_request.top_k 
    
    retriever = Retriever(persist_directory=app_settings.DATABASE_DIR)

    embedding = Embedding()
    vectorstore = retriever.load_vector_store(embedding=embedding)

    retrieved_docs_and_scores = retriever.retrieve_chunks(vectorstore, query, metadata_filter=metadata_filter, k=top_k)
    
    retrieved_documents = []

    for i, (doc, score) in enumerate(retrieved_docs_and_scores):
        retrieved_documents.append({
            "chunk_number": i + 1,
            "score": score,
            "content": doc.page_content,
            "metadata": doc.metadata
        })
    if not retrieved_documents or len(retrieved_documents) == 0 :
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.RETRIEVAL_FAILURE.value
            }
        )
    else:
        return JSONResponse(
            content={
                "retrieved_documents": retrieved_documents
            }
        )
    
    