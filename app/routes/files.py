from fastapi import APIRouter, UploadFile, File
from typing import List
from app.services.file_service import upload_file, bulk_upload_files

router = APIRouter()

@router.post("/upload", summary="Upload a File")
async def upload_file(file: UploadFile = File(...)):
    return await upload_file(file)

@router.post("/bulk-upload", summary="Upload Multiple Files")
async def bulk_upload_files_route(files: List[UploadFile] = File(...)):
    return await bulk_upload_files(files)