from fastapi import FastAPI, APIRouter, Depends
import os
from config import get_settings, Settings

base_router = APIRouter(
    tags=["regulatory-rag-api-v1"]
)

@base_router.get("/")
async def welcome(app_settings : Settings =Depends(get_settings)):
    
    app_name =app_settings.APP_NAME
    return {
        "App Name" : app_name,
    }