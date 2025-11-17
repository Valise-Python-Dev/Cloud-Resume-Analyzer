from sqlalchemy import Column, String, JSON, DateTime, func, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.session import Base
import enum

class ResumeStatus(str, enum.Enum):
    UPLOADED = "UPLOADED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(1024), nullable=False)  # Path on local disk
    status = Column(Enum(ResumeStatus), default=ResumeStatus.UPLOADED)
    analysis_result = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())