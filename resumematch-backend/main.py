from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uuid
import os
from datetime import datetime
import shutil

from models.resume import Resume, ResumeResponse
from models.job import Job, JobRequest, JobResponse
from models.candidate import CandidateResponse
from services.parsing_service import ParsingService
from services.matching_service import MatchingService
from config import config

# Initialize services
parsing_service = ParsingService()
matching_service = MatchingService(model_type="sentence_transformer")

# Store for demonstration purposes (in production, use a database)
current_jobs = {}
current_resumes = {}
current_matches = {}

app = FastAPI(title="AI Resume Matcher API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Resume Matcher API", "version": "1.0.0"}

@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload a resume file (PDF or DOCX) and parse its content
    """
    # Validate file type
    if not parsing_service.validate_file_type(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and DOCX files are allowed.")
    
    # Validate file size
    file_location = f"temp_{uuid.uuid4()}_{file.filename}"
    try:
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
        
        if not parsing_service.is_file_size_valid(file_location):
            raise HTTPException(status_code=400, detail="File size exceeds maximum allowed size (16MB)")
        
        # Parse the resume
        parsed_data = parsing_service.parse_resume_from_bytes(
            open(file_location, "rb").read(), file.filename
        )
        
        # Extract skills using NLP
        skills_data = matching_service.skill_extractor.extract_skills_from_text(parsed_data["content"])
        all_skills = skills_data["technical_skills"] + skills_data["soft_skills"]
        
        # Generate resume ID
        resume_id = str(uuid.uuid4())
        
        # Create resume object
        resume = Resume(
            id=resume_id,
            filename=file_location,
            original_filename=file.filename,
            content=parsed_data["content"],
            extracted_skills=all_skills,
            upload_date=datetime.utcnow()
        )
        
        # Store resume (in production, save to database)
        current_resumes[resume_id] = resume
        
        # Create response
        resume_response = ResumeResponse(
            id=resume.id,
            filename=resume.filename,
            original_filename=resume.original_filename,
            extracted_skills=resume.extracted_skills,
            extracted_experience=resume.extracted_experience,
            extracted_education=resume.extracted_education,
            upload_date=resume.upload_date
        )
        
        return {"success": True, "data": resume_response}
    finally:
        # Clean up temporary file
        if os.path.exists(file_location):
            os.remove(file_location)

@app.post("/jobs/")
async def create_job(job_request: JobRequest):
    """
    Create a new job posting
    """
    job_id = str(uuid.uuid4())
    
    job = Job(
        id=job_id,
        title=job_request.title,
        description=job_request.description,
        required_skills=job_request.required_skills,
        preferred_skills=job_request.preferred_skills,
        experience_required=job_request.experience_required,
        role_responsibilities=job_request.role_responsibilities,
        created_at=datetime.utcnow()
    )
    
    # Store job (in production, save to database)
    current_jobs[job_id] = job
    
    job_response = JobResponse(
        id=job.id,
        title=job.title,
        description=job.description,
        required_skills=job.required_skills,
        preferred_skills=job.preferred_skills,
        experience_required=job.experience_required,
        role_responsibilities=job.role_responsibilities,
        created_at=job.created_at
    )
    
    return {"success": True, "data": job_response}

@app.get("/jobs/{job_id}")
async def get_job(job_id: str):
    """
    Get job details by ID
    """
    if job_id not in current_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = current_jobs[job_id]
    job_response = JobResponse(
        id=job.id,
        title=job.title,
        description=job.description,
        required_skills=job.required_skills,
        preferred_skills=job.preferred_skills,
        experience_required=job.experience_required,
        role_responsibilities=job.role_responsibilities,
        created_at=job.created_at
    )
    
    return {"success": True, "data": job_response}

@app.post("/match/{job_id}")
async def match_candidates(job_id: str):
    """
    Match all uploaded resumes to a specific job
    """
    if job_id not in current_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = current_jobs[job_id]
    matches = []
    
    for resume_id, resume in current_resumes.items():
        # Calculate match score
        match_analysis = matching_service.calculate_match_score(
            resume_content=resume.content,
            job_description=job.description,
            resume_skills=resume.extracted_skills,
            job_required_skills=job.required_skills,
            job_preferred_skills=job.preferred_skills,
            resume_experience=resume.extracted_experience
        )
        
        # Create candidate record
        candidate_id = str(uuid.uuid4())
        candidate = {
            "id": candidate_id,
            "resume_id": resume_id,
            "job_id": job_id,
            "match_analysis": match_analysis,
            "created_at": datetime.utcnow()
        }
        
        # Store match result
        current_matches[candidate_id] = candidate
        matches.append(candidate)
    
    # Sort matches by overall score
    matches.sort(key=lambda x: x["match_analysis"].match_score.overall_score, reverse=True)
    
    # Prepare response
    match_responses = []
    for match in matches:
        match_response = {
            "candidate_id": match["id"],
            "resume_id": match["resume_id"],
            "job_id": match["job_id"],
            "match_analysis": match["match_analysis"],
            "created_at": match["created_at"]
        }
        match_responses.append(match_response)
    
    return {"success": True, "data": match_responses}

@app.get("/matches/{job_id}")
async def get_matches(job_id: str):
    """
    Get all matches for a specific job, sorted by score
    """
    matches_for_job = []
    for candidate_id, candidate in current_matches.items():
        if candidate["job_id"] == job_id:
            matches_for_job.append(candidate)
    
    # Sort by overall score
    matches_for_job.sort(
        key=lambda x: x["match_analysis"].match_score.overall_score, 
        reverse=True
    )
    
    return {"success": True, "data": matches_for_job}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
