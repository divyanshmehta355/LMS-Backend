from fastapi import HTTPException, UploadFile
from app.appwrite_config import storage
from appwrite.input_file import InputFile
import os
from dotenv import load_dotenv
import tempfile
from typing import List

load_dotenv()

async def upload_file(file: UploadFile):
    try:
        # Save uploaded file temporarily
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(file.file.read())
        temp_file.close()

        # Upload file to Appwrite Storage
        bucket_id = os.getenv("APPWRITE_BUCKET_ID")
        result = storage.create_file(
            bucket_id=bucket_id,
            file_id="unique()",
            file=InputFile.from_path(temp_file.name),
            permissions=["read(\"any\")"]
        )

        # Delete temporary file
        os.remove(temp_file.name)

        return {"fileId": result["$id"], "message": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def bulk_upload_files(files: List[UploadFile]):
    """Uploads multiple files to Appwrite Storage"""
    uploaded_files = []

    for file in files:
        try:
            result = await upload_file(file)
            uploaded_files.append(result)
        except Exception as e:
            uploaded_files.append({"filename": file.filename, "error": str(e)})

    return {"uploaded_files": uploaded_files}