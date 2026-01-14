from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Resume(BaseModel):
    id: Optional[str] = None
    filename: str
    original_filename: str
    content: str
    extracted_skills: List[str] = []
    extracted_experience: List[dict] = []  # List of jobs with company, role, duration
    extracted_education: List[dict] = []   # List of education entries
    extracted_certifications: List[str] = []
    embedding: Optional[List[float]] = None
    upload_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ResumeResponse(BaseModel):
    id: str
    filename: str
    original_filename: str
    extracted_skills: List[str]
    extracted_experience: List[dict]
    extracted_education: List[dict]
    upload_date: datetime
    
    class Config:
        from_attributes = True