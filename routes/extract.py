from fastapi import FastAPI, APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse
from .enums.ResponseEnum import ResponseSignal
from .schemes.extract import ExtractRequest
from controllers import BaseController
from processing import Embedding
from retriever import Retriever
from llm_gateway import OpenRouterProvider
from config import Settings, get_settings
import os
import json
from config.logging_config import get_logger

logger = get_logger(__name__)

extraction_router = APIRouter(
    tags=["regulatory-rag-api-v1"]
)

@extraction_router.post("/extract")
async def extract(extraction_request: ExtractRequest, app_settings : Settings =Depends(get_settings)):
    base_controller = BaseController()
    output_dir = base_controller.get_output_dir()
    k_numbers = ["K221000", "K232639", "K230909"]
    required_fields = ["k_number", "device name", "applicant" , "regulation number",
                        "product code", "intended use","indications for use","predicate devices",
                        "technology description", "testing summary", "substantial equivalence rationale"]

    
    model_name = extraction_request.model_name if extraction_request.model_name else app_settings.OPENROUTER_MODEL_NAME
    k_number = extraction_request.k_number
    
    if k_number not in k_numbers:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.INVALID_K_NUMBER.value
            }
        )
    
    embedding = Embedding()
    if os.path.exists(app_settings.DATABASE_DIR):
        logger.error(f"Faild to load vectorstore: vectorDB doesn't exist")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.DATABASE_LOADING_FAILURE.value
            }
        )
    retriever = Retriever(app_settings.DATABASE_DIR)

    vectorstore = retriever.load_vector_store(embedding=embedding)
    full_extraction = {}
    for query in required_fields:
        # Retrieve relevant chunks
        retrieved_docs_and_scores = retriever.retrieve_chunks(vectorstore, query, metadata_filter={"k_number": k_number})

        context = []

        for i, (doc, score) in enumerate(retrieved_docs_and_scores):
            context.append(
                f"""[Chunk_id: {doc.id}]
{doc.page_content}"""
            )
        # Get structured output   
        openrouter_provider = OpenRouterProvider(model_name=model_name)
        llm_chain = openrouter_provider.get_llm_gateway_chain()
        response = llm_chain.invoke({
        "query": query,
        "context": context
    })
        full_extraction.update(response)

    # Save structured output.
    try:
        output_path = os.path.join(output_dir, f"extraction_{k_number}.json" )
        with open(output_path, "w") as f:
            json.dump(full_extraction, f, indent=4)
        
    except Exception as e:
        logger.error(f"Error writing output file: {e}")
    
    return JSONResponse(
            content={"full_extraction": full_extraction}   
            )
    
        
        

