import shutil
import os
import uuid
from fastapi import UploadFile
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def save_upload_file(upload_file: UploadFile) -> str:
    """
    Stream-saves an uploaded file to the local disk to handle large files efficiently.
    Returns the absolute file path.
    """
    try:
        # Generate unique filename to prevent overwrites
        file_ext = upload_file.filename.split('.')[-1]
        safe_filename = f"{uuid.uuid4()}.{file_ext}"
        file_path = os.path.join(settings.UPLOAD_FOLDER, safe_filename)
        
        # Write file to disk using shutil for efficiency
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
            
        logger.info(f"File successfully saved to {file_path}")
        return file_path
        
    except Exception as e:
        logger.error(f"Failed to save file locally: {e}")
        return None