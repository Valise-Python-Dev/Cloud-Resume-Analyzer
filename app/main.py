from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import resume
from app.db.session import Base, engine

# Create Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cloud Resume Analyzer (Local Mode)")

# Allow frontend to connect (if needed later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume.router, prefix="/api/v1/resume", tags=["Resume"])

@app.get("/")
def root():
    return {"message": "Resume Analyzer API is running locally"}