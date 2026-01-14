from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class MatchScore(BaseModel):
    skills_score: float
    experience_score: float
    role_fit_score: float
    bonus_signals_score: float
    overall_score: float
    
    class Config:
        from_attributes = True


class MatchAnalysis(BaseModel):
    match_score: MatchScore
    matched_skills: List[str]
    missing_skills: List[str]
    transferable_skills: List[str]
    experience_summary: str
    role_recommendation: str
    explanation: str
    
    class Config:
        from_attributes = True


class Candidate(BaseModel):
    id: str
    resume_id: str
    job_id: str
    match_analysis: MatchAnalysis
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class CandidateResponse(BaseModel):
    id: str
    resume_id: str
    job_id: str
    match_analysis: MatchAnalysis
    created_at: datetime
    
    class Config:
        from_attributes = True