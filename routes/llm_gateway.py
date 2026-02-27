from fastapi import FastAPI, APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse
from .enums.ResponseEnum import ResponseSignal
from .schemes.llm_gateway import LLMGatewayRequest
from embedding import Embedding
from retriever import Retriever
from llm_gateway import OpenRouterProvider
from config import Settings, get_settings
import os
from config.logging_config import get_logger

logger = get_logger(__name__)


llm_gateway_router = APIRouter(
    tags=["regulatory-rag-api-v1"]
)

@llm_gateway_router.post("/llm_gateway")
async def llm_gateway(llm_gateway_request: LLMGatewayRequest, app_settings : Settings =Depends(get_settings)): 
    query = llm_gateway_request.query
    model_name = llm_gateway_request.model_name if llm_gateway_request.model_name else app_settings.OPENROUTER_MODEL_NAME
    
    metadata_filter = {"k_number": llm_gateway_request.k_number} if llm_gateway_request.k_number else None
    
  
    if not os.path.exists(app_settings.DATABASE_DIR):
        logger.error(f"Faild to load vectorstore: vectorDB doesn't exist")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.DATABASE_LOADING_FAILURE.value
            }
        )
    retriever = Retriever(app_settings.DATABASE_DIR)

    embedding = Embedding()
    vectorstore = retriever.load_vector_store(embedding=embedding)

    retrieved_docs_and_scores = retriever.retrieve_chunks(vectorstore, query, metadata_filter=metadata_filter)
    
    context = []

    for i, (doc, score) in enumerate(retrieved_docs_and_scores):
         context.append(f"""chunk_id: {doc.id}
content: {doc.page_content}""") 
         

    if not retrieved_docs_and_scores or len(retrieved_docs_and_scores) == 0 :
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.RETRIEVAL_FAILURE.value
            }
        )
   
    openrouter_provider = OpenRouterProvider(model_name=model_name)
    llm_chain = openrouter_provider.get_llm_gateway_chain()
    response = llm_chain.invoke({
    "query": query,
    "context": context
})
    return JSONResponse(
            content={
                "response": response
            }
        )
    
    
    