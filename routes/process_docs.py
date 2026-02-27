from fastapi import FastAPI, APIRouter, Depends, status, Request
from config import Settings, get_settings
from fastapi.responses import JSONResponse
from .enums.ResponseEnum import ResponseSignal
from controllers import BaseController
from processing import TextExtractor
import logging
import os
import json

process_docs_router = APIRouter(
    tags=["regulatory-rag-api-v1"]
)

@process_docs_router.post("/process_docs")
async def process_docs( app_settings : Settings =Depends(get_settings)): 
    logger = logging.getLogger(__name__)

    base_controller = BaseController()
    pdf_files_dir = base_controller.get_pdf_files_dir()
    files_metadata_path = base_controller.get_files_metadata_path()

    text_extractor = TextExtractor(base_controller=base_controller)

    files_names = os.listdir(pdf_files_dir)

    logger.info(f"Found {len(files_names)} in {pdf_files_dir} to be processed")
        
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

    return JSONResponse(
        content={
            "signal": ResponseSignal.TEXT_EXTRACTION_SUCCESS.value,
            "text_files_stored_at": base_controller.get_txt_files_dir
        }
    )
        
            
        
    
    