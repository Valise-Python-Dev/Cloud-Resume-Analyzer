from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from app.db import models, schemas
from app.db.session import get_db
from app.services import file_service, ml_service
from uuid import UUID
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

def background_analysis_task(resume_id: UUID, db: Session):
    """Background task wrapper to prevent blocking the main thread."""
    resume = db.get(models.Resume, resume_id)
    if not resume:
        return

    try:
        # Update status to PROCESSING
        resume.status = models.ResumeStatus.PROCESSING
        db.commit()
        
        # Run the heavy ML work
        results = ml_service.run_analysis_pipeline(resume)
        
        # Save results
        resume = db.get(models.Resume, resume_id) # Refresh session
        resume.analysis_result = results
        
        # Check for errors in the ML output
        if "error" in results or results.get("score", {}).get("error"):
            resume.status = models.ResumeStatus.FAILED
        else:
            resume.status = models.ResumeStatus.COMPLETED
            
        db.commit()
        logger.info(f"Task completed for Resume ID: {resume_id}")

    except Exception as e:
        logger.error(f"Background task failed: {e}")
        db.rollback()
        # Attempt to set failure status
        try:
            resume = db.get(models.Resume, resume_id)
            resume.status = models.ResumeStatus.FAILED
            resume.analysis_result = {"error": "Internal Server Error"}
            db.commit()
        except:
            pass

@router.post("/upload", response_model=schemas.ResumeUploadResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_resume(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Validate File Type
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")

    # 2. Save File Locally
    saved_path = file_service.save_upload_file(file)
    if not saved_path:
        raise HTTPException(status_code=500, detail="Failed to save file to disk.")

    # 3. Create Database Entry
    new_resume = models.Resume(
        original_filename=file.filename,
        file_path=saved_path,
        status=models.ResumeStatus.UPLOADED
    )
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    # 4. Trigger Background Analysis
    background_tasks.add_task(background_analysis_task, new_resume.id, db)

    return {
        "id": new_resume.id,
        "message": "Resume uploaded successfully. Analysis has started.",
        "status": new_resume.status
    }

@router.get("/{resume_id}/status", response_model=schemas.Resume)
def get_status(resume_id: UUID, db: Session = Depends(get_db)):
    resume = db.get(models.Resume, resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume