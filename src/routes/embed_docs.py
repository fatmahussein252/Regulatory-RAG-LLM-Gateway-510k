from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse
from .enums.ResponseEnum import ResponseSignal
from .schemes.process_docs import EmbeddingRequest
from controllers import BaseController
from processing import ChunkEnum, Chunker, TextExtractor, LlamaIndexChunker
from embedding import Embedding
from langchain_community.retrievers import BM25Retriever
from config import Settings, get_settings
import os
import json
import shutil
from helpers.utils import normalize_text
from config.logging_config import get_logger


logger = get_logger(__name__)

embed_docs_router = APIRouter(
    tags=["regulatory-rag-api-v1"]
)

@embed_docs_router.post("/embed_docs")
async def embed_docs(request: Request, embdding_request: EmbeddingRequest, app_settings : Settings =Depends(get_settings)): 
    
    chunk_size = embdding_request.chunk_size if embdding_request.chunk_size else ChunkEnum.CHUNK_SIZE.value
    chunk_overlap = embdding_request.chunk_overlap_size if embdding_request.chunk_overlap_size else ChunkEnum.CHUNK_OVERLAP_SIZE.value

    base_controller = BaseController()
    pdf_files_dir = base_controller.get_pdf_files_dir()
    files_metadata_path = base_controller.get_files_metadata_path()

    text_extractor = TextExtractor(base_controller=base_controller)
    chunker = Chunker()
    #llamaindex_chunking = LlamaIndexChunker()
    embedding = Embedding()    

    # check whether files where downloaded
    files_names = os.listdir(pdf_files_dir)
    if len(files_names) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.NO_DOWNLOADED_FILES.value
            }
        )

    logger.info(f"Found {len(files_names)} files in {pdf_files_dir} to be processed")
        
    # Get metadata
    try: 
        with open(files_metadata_path, "r") as f:
            metadata = json.load(f)
    except Exception as e:
        logger.error(f"Error reading metadata file: {e}")
        
    chunks = []   
    for file in files_names:
        file_path = os.path.join(
            pdf_files_dir,
            file
        )
        
        # Extract and clean text
        pages_list = text_extractor.extract_text(
            file_path=file_path,
            file_source=metadata[os.path.basename(file_path)]["URL"],            
            )
        if not pages_list or len(pages_list) == 0:   
            logger.error(f"Failed to extract text and metadata from PDFs.")
        
        # chunk text   
        documents = chunker.create_page_documents(
            pages_list=pages_list,
            )
        
        """ # Section-aware chunking
        chunks = llamaindex_chunking.get_llama_index_chunks()"""
        
        chunks.extend(chunker.chunk_documents(
            documents=documents,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap))

  
    if not chunks or len(chunks) == 0:    
        logger.error(f"Failed to chunk documents\n")      
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.CHUNKING_FAILURE.value
            }
        )
   
    # Get Database directory
    persist_directory = base_controller.get_db_dir()
    
    # Store embeddings    
    embedded_successfully, vectorstore = embedding.embed_text(
        chunks=chunks,
        persist_directory=persist_directory
    )
    request.app.state.vectorstore = vectorstore
    
    # keyword Indexing
    if embdding_request.keyword_index:
        keyword_index = BM25Retriever.from_documents(chunks, preprocess_func=normalize_text)
        request.app.state.keyword_index = keyword_index


    if embedded_successfully:
        return JSONResponse(
                content={
                    "signal": ResponseSignal.VECTORDB_STORAGE_SUCCESS.value,
                    "vectordb_stored_at": str(persist_directory)
                }
            )
    else:
       return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.VECTORDB_STORAGE_FAILURE.value,
                }
            ) 


        
    