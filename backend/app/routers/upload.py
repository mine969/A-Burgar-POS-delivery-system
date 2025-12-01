from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
import uuid

router = APIRouter(
    prefix="/upload",
    tags=["upload"]
)

UPLOAD_DIR = "static/images"

# Ensure directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Return URL
        # Use API_HOST env var if available, otherwise default to localhost:3001
        # Note: In production/docker, this should be the public URL
        base_url = os.getenv("API_HOST", "http://localhost:3001")
        return {"url": f"{base_url}/static/images/{filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
