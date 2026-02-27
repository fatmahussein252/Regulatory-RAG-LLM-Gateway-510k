from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from .enums.ResponseEnum import ResponseSignal
from .schemes.process_docs import EmbeddingRequest
from controllers import BaseController
from processing import ChunkEnum, Chunker, TextExtractor, Embedding
from config import Settings, get_settings
import os
import json
import logging
import shutil

embed_docs_router = APIRouter(
    tags=["regulatory-rag-api-v1"]
)

@embed_docs_router.post("/embed_docs")
async def embed_docs(embdding_request: EmbeddingRequest, app_settings : Settings =Depends(get_settings)): 
    
    logger = logging.getLogger(__name__)

    chunk_size = embdding_request.chunk_size if embdding_request.chunk_size else ChunkEnum.CHUNK_SIZE.value
    chunk_overlap = embdding_request.chunk_overlap_size if embdding_request.chunk_overlap_size else ChunkEnum.CHUNK_OVERLAP_SIZE.value

    base_controller = BaseController()
    pdf_files_dir = base_controller.get_pdf_files_dir()
    files_metadata_path = base_controller.get_files_metadata_path()

    text_extractor = TextExtractor(base_controller=base_controller)
    chunker = Chunker()
    embedding = Embedding()    

    files_names = os.listdir(pdf_files_dir)

    logger.info(f"Found {len(files_names)} in {pdf_files_dir} to be processed")
        
    chunks = []
    with open(files_metadata_path, "r") as f:
        metadata = json.load(f)
        
    for file in files_names:
        file_path = os.path.join(
            pdf_files_dir,
            file
        )
        

        pages_list = text_extractor.extract_text(
            file_path=file_path,
            file_source=metadata[os.path.basename(file_path)]["URL"],            
            )
        if not pages_list or len(pages_list) == 0:   
            logger.error(f"Failed to extract text and metadata from PDFs ")
        
            
        documnets = chunker.create_page_documents(
            pages_list=pages_list,
            )
        
        chunks.extend(chunker.chunk_documents(
            documents=documnets,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap))

  
    if not chunks or len(chunks) == 0:    
        logger.error(f"Failed to chunk documents")      
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.CHUNKING_FAILURE.value
            }
        )
   
    
    if(os.path.exists(app_settings.DATABASE_DIR)):
        try:
            shutil.rmtree(app_settings.DATABASE_DIR)
            os.mkdir(app_settings.DATABASE_DIR)
            logger.info(f"Directory '{app_settings.DATABASE_DIR}' and all its contents have been removed.")
        except OSError as e:
            logger.info(f"Error: {app_settings.DATABASE_DIR} : {e.strerror}")
    
        
    vectorstore = embedding.embed_text(
        chunks=chunks,
        persist_directory=app_settings.DATABASE_DIR
    )

    if os.path.exists(app_settings.DATABASE_DIR):
        return JSONResponse(
                content={
                    "signal": ResponseSignal.VECTORDB_STORAGE_SUCCESS.value,
                    "vectordb_stored_at": app_settings.DATABASE_DIR
                }
            )

        
    