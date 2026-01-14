from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Job(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    experience_required: str  # e.g., "3+ years", "Entry level"
    role_responsibilities: List[str] = []
    embedding: Optional[List[float]] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class JobRequest(BaseModel):
    title: str
    description: str
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    experience_required: str = "Not specified"
    role_responsibilities: List[str] = []
    
    class Config:
        from_attributes = True

class JobResponse(BaseModel):
    id: str
    title: str
    description: str
    required_skills: List[str]
    preferred_skills: List[str]
    experience_required: str
    role_responsibilities: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True