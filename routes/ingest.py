from fastapi import FastAPI, APIRouter, Depends, status
from fastapi.responses import JSONResponse
from controllers import BaseController
from Ingestion import Downloader
from .enums.ResponseEnum import ResponseSignal


ingest_router = APIRouter(
    tags=["regulatory-rag-api-v1"]
)

@ingest_router.get("/ingest")
async def ingest_files(): # Settings here for type of returned object
    
    base_controller = BaseController()
    downloader = Downloader(base_controller=base_controller)
    downloaded_files = downloader.download_and_save_files()
    if not downloaded_files:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.DOWNLOAD_FILES_FAILURE.value
            }
        )
    files_metadata_content = downloader.save_files_metadata()
    if not files_metadata_content:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.FILES_METADATA_EXTRACTION_FAILURE.value
            }
        )
    
    return JSONResponse(
        content={
            "downloaded files": downloaded_files,
            "files_meta_data": files_metadata_content
        }
    )
    