from typing import List
import os
import shutil
import zipfile
import uuid
from fastapi import File, UploadFile, HTTPException, FastAPI
from fastapi.responses import FileResponse

upload_folder = "files"

app = FastAPI()

@app.post("/upload_file/")
async def upload_file(files: list[UploadFile] = File(...)):
    archive_id = str(uuid.uuid4())
    archive_path = f"{upload_folder}/{archive_id}.zip"

    with zipfile.ZipFile(archive_path, 'w') as archive:
        for file in files:
            file_path = f"{upload_folder}/{file.filename}"
            
            with open(file_path, "wb") as new_file:
                new_file.write(await file.read())

            archive.write(file_path, arcname=f"{file.filename}")
            os.remove(file_path)
    return {"file_id": archive_id}

@app.get("/download_file/{file_id}")
async def download_file(file_id: str):
    file_path = f"{upload_folder}/{file_id}.zip"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="application/zip", filename=file_id)