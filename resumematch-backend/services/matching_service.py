from typing import List, Dict, Any
from models.candidate import MatchScore, MatchAnalysis
from nlp.skill_extractor import SkillExtractor
from nlp.embedding_extractor import EmbeddingExtractor
from services.embedding_service import EmbeddingService
from services.qwen_service import QwenService
from config import config
import logging

logger = logging.getLogger(__name__)

class MatchingService:
    def __init__(self, model_type: str = "sentence_transformer"):
        self.embedding_service = EmbeddingService(model_type=model_type)
        self.embedding_extractor = EmbeddingExtractor(self.embedding_service)
        self.skill_extractor = SkillExtractor()
        self.model_type = model_type
        # Initialize Qwen service only when needed to avoid startup issues
        self._qwen_service = None
    
    @property
    def qwen_service(self):
        if self._qwen_service is None:
            from services.qwen_service import QwenService
            self._qwen_service = QwenService()
        return self._qwen_service
    
    def calculate_match_score(self, resume_content: str, job_description: str, 
                             resume_skills: List[str], job_required_skills: List[str],
                             job_preferred_skills: List[str], 
                             resume_experience: List[dict] = None) -> MatchAnalysis:
        """
        Calculate comprehensive match score between resume and job description
        """
        # Extract embeddings
        resume_embedding = self.embedding_extractor.extract_embeddings_from_resume(resume_content)
        job_embedding = self.embedding_extractor.extract_embeddings_from_job_description(job_description)
        
        # Calculate base semantic similarity
        semantic_similarity = self.embedding_extractor.compute_similarity(resume_embedding, job_embedding)
        
        # Calculate skills score
        skills_match_result = self._calculate_skills_score(
            resume_skills, job_required_skills, job_preferred_skills
        )
        
        # Calculate experience score
        experience_score = self._calculate_experience_score(resume_experience, job_description)
        
        # Calculate role fit score
        role_fit_score = self._calculate_role_fit_score(resume_content, job_description)
        
        # Calculate bonus signals score
        bonus_signals_score = self._calculate_bonus_signals_score(resume_content, job_description)
        
        # Calculate weighted overall score
        overall_score = (
            skills_match_result['score'] * config.SKILLS_WEIGHT +
            experience_score * config.EXPERIENCE_WEIGHT +
            role_fit_score * config.ROLE_FIT_WEIGHT +
            bonus_signals_score * config.BONUS_SIGNALS_WEIGHT
        )
        
        # Create match score object
        match_score = MatchScore(
            skills_score=skills_match_result['score'],
            experience_score=experience_score,
            role_fit_score=role_fit_score,
            bonus_signals_score=bonus_signals_score,
            overall_score=overall_score
        )
        
        # Generate match analysis with Qwen explanations
        match_analysis = MatchAnalysis(
            match_score=match_score,
            matched_skills=skills_match_result['matched_skills'],
            missing_skills=skills_match_result['missing_skills'],
            transferable_skills=skills_match_result['transferable_skills'],
            experience_summary=skills_match_result['experience_summary'],
            role_recommendation=self._generate_role_recommendation(overall_score),
            explanation=self._generate_explanation_with_qwen(
                resume_content, job_description, overall_score
            )
        )
        
        return match_analysis
    
    def _calculate_skills_score(self, resume_skills: List[str], 
                               job_required_skills: List[str], 
                               job_preferred_skills: List[str]) -> Dict[str, Any]:
        """
        Calculate skills match score
        """
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        job_required_skills_lower = [skill.lower() for skill in job_required_skills]
        job_preferred_skills_lower = [skill.lower() for skill in job_preferred_skills]
        
        # Find matched required skills
        matched_required = [skill for skill in job_required_skills_lower if skill in resume_skills_lower]
        
        # Find matched preferred skills
        matched_preferred = [skill for skill in job_preferred_skills_lower if skill in resume_skills_lower]
        
        # Find missing required skills
        missing_required = [skill for skill in job_required_skills_lower if skill not in resume_skills_lower]
        
        # Calculate scores
        required_skills_score = len(matched_required) / len(job_required_skills) if job_required_skills else 1.0
        preferred_skills_score = len(matched_preferred) / len(job_preferred_skills) if job_preferred_skills else 0.0
        
        # Weighted skills score (70% required, 30% preferred)
        skills_score = (required_skills_score * 0.7) + (preferred_skills_score * 0.3)
        
        # Identify potential transferable skills (not exact matches but related)
        transferable_skills = self._identify_transferable_skills(resume_skills_lower, job_required_skills_lower)
        
        return {
            "score": skills_score,
            "matched_skills": matched_required + matched_preferred,
            "missing_skills": missing_required,
            "transferable_skills": transferable_skills,
            "experience_summary": f"Matched {len(matched_required)}/{len(job_required_skills)} required skills and {len(matched_preferred)}/{len(job_preferred_skills)} preferred skills"
        }
    
    def _calculate_experience_score(self, resume_experience: List[dict], job_description: str) -> float:
        """
        Calculate experience match score
        """
        if not resume_experience:
            return 0.0
        
        # Count relevant experience
        relevant_experience_count = 0
        total_years = 0
        
        for exp in resume_experience:
            if 'duration' in exp and exp['duration']:
                # Extract years from duration string
                years = self._extract_years_from_duration(exp['duration'])
                total_years += years
            
            # Check if experience is relevant to job
            if self._is_experience_relevant(exp, job_description):
                relevant_experience_count += 1
        
        # Normalize experience score
        if len(resume_experience) > 0:
            relevance_ratio = relevant_experience_count / len(resume_experience)
        else:
            relevance_ratio = 0.0
        
        # Score based on both relevance and total years
        experience_score = min(1.0, (relevance_ratio + min(total_years / 10.0, 1.0)) / 2.0)
        
        return experience_score
    
    def _calculate_role_fit_score(self, resume_content: str, job_description: str) -> float:
        """
        Calculate how well the resume fits the role
        """
        # Use embedding similarity as primary measure
        resume_embedding = self.embedding_extractor.extract_embeddings_from_resume(resume_content)
        job_embedding = self.embedding_extractor.extract_embeddings_from_job_description(job_description)
        
        similarity = self.embedding_extractor.compute_similarity(resume_embedding, job_embedding)
        
        return similarity
    
    def _calculate_bonus_signals_score(self, resume_content: str, job_description: str) -> float:
        """
        Calculate bonus signals that indicate strong fit
        """
        bonus_points = 0
        max_bonus_points = 5
        
        # Check for relevant certifications
        cert_matches = self._check_certifications(resume_content, job_description)
        if cert_matches:
            bonus_points += 1
        
        # Check for specific company experience
        company_matches = self._check_company_experience(resume_content, job_description)
        if company_matches:
            bonus_points += 1
        
        # Check for advanced education
        education_matches = self._check_advanced_education(resume_content)
        if education_matches:
            bonus_points += 1
        
        # Check for leadership experience
        leadership_matches = self._check_leadership_experience(resume_content)
        if leadership_matches:
            bonus_points += 1
        
        # Check for specific achievements
        achievement_matches = self._check_achievements(resume_content)
        if achievement_matches:
            bonus_points += 1
        
        return min(bonus_points / max_bonus_points, 1.0)
    
    def _extract_years_from_duration(self, duration_str: str) -> float:
        """
        Extract years from duration string
        """
        import re
        # Look for patterns like "2 years", "3 months", "1.5 years", etc.
        year_patterns = [r'(\d+(?:\.\d+)?)\s*(?:years?|yrs?)', r'(\d+(?:\.\d+)?)\s*(?:months?)']
        
        for pattern in year_patterns:
            matches = re.findall(pattern, duration_str, re.IGNORECASE)
            if matches:
                value = float(matches[0])
                if 'month' in pattern:
                    return value / 12.0  # Convert months to years
                return value
        
        return 0.0
    
    def _is_experience_relevant(self, experience: dict, job_description: str) -> bool:
        """
        Check if experience is relevant to job description
        """
        # Check if role title or company is mentioned in job description
        role_title = experience.get('role', '').lower()
        company = experience.get('company', '').lower()
        
        job_desc_lower = job_description.lower()
        
        return role_title in job_desc_lower or company in job_desc_lower
    
    def _identify_transferable_skills(self, resume_skills: List[str], job_skills: List[str]) -> List[str]:
        """
        Identify skills that may be transferable even if not exact matches
        """
        transferable = []
        
        for job_skill in job_skills:
            for resume_skill in resume_skills:
                # Simple similarity check (could be enhanced with NLP)
                if self._strings_are_similar(job_skill, resume_skill):
                    transferable.append(resume_skill)
                    break
        
        return transferable
    
    def _strings_are_similar(self, str1: str, str2: str, threshold: float = 0.8) -> bool:
        """
        Check if two strings are similar using a simple heuristic
        """
        # This is a simplified version - in practice, you'd use more sophisticated NLP
        common_words = set(str1.split()) & set(str2.split())
        if len(common_words) > 0:
            return True
        
        # Additional checks could include fuzzy matching
        return False
    
    def _check_certifications(self, resume_content: str, job_description: str) -> bool:
        """
        Check for relevant certifications
        """
        cert_keywords = ['certified', 'certification', 'certificate', 'aws', 'azure', 'gcp', 'ccna', 'pmp', 'scrum', 'saas']
        resume_lower = resume_content.lower()
        job_lower = job_description.lower()
        
        return any(keyword in resume_lower and keyword in job_lower for keyword in cert_keywords)
    
    def _check_company_experience(self, resume_content: str, job_description: str) -> bool:
        """
        Check for experience at companies mentioned in job description
        """
        # This would require more sophisticated entity extraction
        # For now, a simple keyword match
        resume_lower = resume_content.lower()
        job_lower = job_description.lower()
        
        # Look for common company indicators
        return 'experience' in resume_lower and ('previous company' in resume_lower or 'worked at' in resume_lower)
    
    def _check_advanced_education(self, resume_content: str) -> bool:
        """
        Check for advanced education
        """
        advanced_edu_keywords = ['master', 'phd', 'doctorate', 'mba', 'advanced degree']
        resume_lower = resume_content.lower()
        
        return any(keyword in resume_lower for keyword in advanced_edu_keywords)
    
    def _check_leadership_experience(self, resume_content: str) -> bool:
        """
        Check for leadership experience
        """
        leadership_keywords = ['lead', 'managed', 'manager', 'supervisor', 'director', 'head of', 'team lead', 'senior']
        resume_lower = resume_content.lower()
        
        return any(keyword in resume_lower for keyword in leadership_keywords)
    
    def _check_achievements(self, resume_content: str) -> bool:
        """
        Check for achievements
        """
        achievement_keywords = ['achieved', 'improved', 'increased', 'reduced', 'saved', 'generated', 'awarded', 'recognized']
        resume_lower = resume_content.lower()
        
        return any(keyword in resume_lower for keyword in achievement_keywords)
    
    def _generate_role_recommendation(self, overall_score: float) -> str:
        """
        Generate role recommendation based on overall score
        """
        if overall_score >= 0.8:
            return "Strong Recommendation - Highly Suitable"
        elif overall_score >= 0.6:
            return "Moderate Recommendation - Good Fit"
        elif overall_score >= 0.4:
            return "Consideration Needed - Partial Fit"
        else:
            return "Not Recommended - Poor Fit"
    
    def _generate_explanation_with_qwen(self, resume_content: str, job_description: str, overall_score: float) -> str:
        """
        Generate explanation using Qwen model for better analysis
        """
        # Use Qwen service to generate a more detailed explanation
        qwen_explanation = self.qwen_service.generate_match_explanation(
            resume_content, job_description, overall_score
        )
        
        if qwen_explanation:
            return qwen_explanation
        
        # Fallback to rule-based explanation
        explanation_parts = []
        
        # Since we can't call _calculate_skills_score without all parameters here,
        # we'll use a simplified approach for the fallback
        explanation_parts.append(
            f"Skills Match: Analysis based on semantic similarity. "
            f"Missing skills: Various skills may need to be added to improve match."
        )
        
        # Experience explanation
        exp_level = "High" if overall_score >= 0.7 else "Medium" if overall_score >= 0.4 else "Low"
        explanation_parts.append(f"Experience Level: {exp_level} - Based on relevance and duration of past roles.")
        
        # Role fit explanation
        fit_level = "Excellent" if overall_score >= 0.8 else "Good" if overall_score >= 0.6 else "Fair" if overall_score >= 0.4 else "Poor"
        explanation_parts.append(f"Role Fit: {fit_level} - Semantic similarity between resume and job requirements.")
        
        # Final recommendation
        recommendation = self._generate_role_recommendation(overall_score)
        explanation_parts.append(f"Final Recommendation: {recommendation}")
        
        return " ".join(explanation_parts)