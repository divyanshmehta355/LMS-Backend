from fastapi import HTTPException, UploadFile
from app.appwrite_config import storage
from appwrite.input_file import InputFile
import os
from dotenv import load_dotenv

load_dotenv()

bucket_id = os.getenv("APPWRITE_BUCKET_ID")

async def upload_file(file: UploadFile):
    try:
        # Read file content as a stream
        file_stream = file.file

        # Upload file directly to Appwrite
        result = storage.create_file(
            bucket_id=bucket_id,
            file_id="unique()",
            file=InputFile.from_bytes(file_stream.read(), filename=file.filename),
            permissions=["read(\"any\")"]
        )

        return {"fileId": result["$id"], "message": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def bulk_upload_files(files: list[UploadFile]):
    try:
        uploaded_files = []

        for file in files:
            file_stream = file.file

            result = storage.create_file(
                bucket_id=bucket_id,
                file_id="unique()",
                file=InputFile.from_bytes(file_stream.read(), filename=file.filename),
                permissions=["read(\"any\")"]
            )

            uploaded_files.append({"fileId": result["$id"], "filename": file.filename})

        return {"message": "Files uploaded successfully", "files": uploaded_files}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))