from fastapi import FastAPI, APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse
from .enums.ResponseEnum import ResponseSignal
from .schemes.llm_gateway import LLMGatewayRequest
from embedding import Embedding
from retriever import VectorRetriever, BMRetriever
from helpers.utils import normalize_text
from llm_gateway import OpenRouterProvider
from config import Settings, get_settings
import os
from config.logging_config import get_logger

logger = get_logger(__name__)


llm_gateway_router = APIRouter(
    tags=["regulatory-rag-api-v1"]
)

@llm_gateway_router.post("/llm_gateway")
async def llm_gateway(request: Request, llm_gateway_request: LLMGatewayRequest, app_settings : Settings =Depends(get_settings)): 
    
    query = normalize_text(llm_gateway_request.query)
    
    model_name = llm_gateway_request.model_name if llm_gateway_request.model_name else app_settings.OPENROUTER_MODEL_NAME
    
    k_number = llm_gateway_request.k_number
    metadata_filter = {"k_number": k_number} if k_number else None
    
  
    if not os.path.exists(app_settings.DATABASE_DIR):
        logger.error(f"\nFaild to load vectorstore: vectorDB doesn't exist\n")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.DATABASE_LOADING_FAILURE.value
            }
        )
    retriever = VectorRetriever(app_settings.DATABASE_DIR)

    embedding = Embedding()

    vectorstore = retriever.load_vector_store(embedding=embedding)
    retrieved_docs_and_scores = retriever.retrieve_chunks(vectorstore, query, metadata_filter=metadata_filter)
    
    if not retrieved_docs_and_scores or len(retrieved_docs_and_scores) == 0 :
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.RETRIEVAL_FAILURE.value
            }
        )
    
    context = []
    for i, (doc, score) in enumerate(retrieved_docs_and_scores):
         context.append(f"""chunk_id: {doc.id}
content: {doc.page_content}""") 
    
    # Add keyword retrieved chunks to the context if indexed
    if hasattr(request.app.state, "keyword_index"):
        keyword_index = request.app.state.keyword_index
        keyword_retriever = BMRetriever()
        keyword_retrieved_docs = keyword_retriever.retrieve_docs(
            keyword_index=keyword_index,
            query=query,
            metadata_filter=k_number) 

        for i, doc in enumerate(keyword_retrieved_docs):
            context.append(f"""chunk_id: {doc.id}
    content: {doc.page_content}""")
         

   
    openrouter_provider = OpenRouterProvider(model_name=model_name)
    llm_chain = openrouter_provider.get_llm_gateway_chain()
    response = llm_chain.invoke({
    "query": query,
    "context": "\n\n".join(context)
})
    return JSONResponse(
            content={
                "context": context,
                "response": response
            }
        )
    
    
    