from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any
from .models import ResumeStatus

class ResumeBase(BaseModel):
    original_filename: str

class Resume(ResumeBase):
    id: UUID
    file_path: str
    status: ResumeStatus
    analysis_result: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class ResumeUploadResponse(BaseModel):
    id: UUID
    message: str
    status: ResumeStatus