from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from typing import Dict, List
import logging
import re

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, model_name: str = "openai-community/gpt2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        # Add padding token if it doesn't exist
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.model.eval()
    
    def generate_match_explanation(self, resume_content: str, job_description: str, match_score: float) -> str:
        """
        Generate an explanation for why a resume matches a job description
        """
        prompt = f"""Generate a professional explanation of how this resume matches this job description.
        
Resume: {resume_content[:500]}...
        
Job Description: {job_description[:500]}...
        
Match Score: {match_score:.2f}/1.0
        
Explanation:"""
        
        try:
            inputs = self.tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=1024)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs, 
                    max_length=len(inputs[0]) + 100,
                    temperature=0.7,
                    pad_token_id=self.tokenizer.eos_token_id,
                    do_sample=True,
                    num_return_sequences=1
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Extract just the generated part (after the prompt)
            explanation = response[len(prompt):].strip()
            # Clean up the response to get a coherent explanation
            explanation = self._clean_generated_text(explanation)
            
            return explanation
        except Exception as e:
            logger.error(f"Error generating match explanation: {str(e)}")
            # Fallback explanation
            return f"The candidate shows a match score of {match_score:.2f}, indicating {'strong' if match_score > 0.7 else 'moderate' if match_score > 0.5 else 'weak'} alignment with the job requirements."
    
    def generate_skill_gap_analysis(self, resume_skills: List[str], required_skills: List[str]) -> str:
        """
        Analyze skill gaps between resume and job requirements
        """
        resume_skills_str = ", ".join(resume_skills)
        required_skills_str = ", ".join(required_skills)
        
        prompt = f"""Analyze the skill gaps for this candidate.
        
Candidate Skills: {resume_skills_str}
        
Required Skills: {required_skills_str}
        
Gap Analysis:"""
        
        try:
            inputs = self.tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=1024)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs, 
                    max_length=len(inputs[0]) + 100,
                    temperature=0.7,
                    pad_token_id=self.tokenizer.eos_token_id,
                    do_sample=True,
                    num_return_sequences=1
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            analysis = response[len(prompt):].strip()
            analysis = self._clean_generated_text(analysis)
            
            return analysis
        except Exception as e:
            logger.error(f"Error generating skill gap analysis: {str(e)}")
            missing_skills = set(required_skills) - set(resume_skills)
            return f"The candidate is missing these required skills: {', '.join(missing_skills)}. Consider upskilling in these areas."
    
    def generate_hiring_recommendation(self, match_score: float, experience_years: float = None) -> str:
        """
        Generate a hiring recommendation based on match score
        """
        prompt = f"""Generate a professional hiring recommendation based on this match score.
        
Match Score: {match_score:.2f}/1.0
        Years of Experience: {experience_years or 'Not specified'}
        
Recommendation:"""
        
        try:
            inputs = self.tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=1024)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs, 
                    max_length=len(inputs[0]) + 80,
                    temperature=0.6,
                    pad_token_id=self.tokenizer.eos_token_id,
                    do_sample=True,
                    num_return_sequences=1
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            recommendation = response[len(prompt):].strip()
            recommendation = self._clean_generated_text(recommendation)
            
            return recommendation
        except Exception as e:
            logger.error(f"Error generating hiring recommendation: {str(e)}")
            if match_score > 0.8:
                return "Strong recommendation to proceed with interview."
            elif match_score > 0.6:
                return "Consider for interview with additional screening."
            elif match_score > 0.4:
                return "Evaluate other candidates first."
            else:
                return "Not recommended for this position."
    
    def _clean_generated_text(self, text: str) -> str:
        """
        Clean up generated text to remove artifacts and make it more coherent
        """
        # Remove any continuation of the prompt
        text = text.replace('\n\n', '\n').strip()
        
        # Truncate at sentence boundary if too long
        sentences = re.split(r'(?<=[.!?]) +', text)
        cleaned = ""
        for sentence in sentences:
            if len(cleaned + sentence) < 200:  # Limit length
                cleaned += sentence + " "
            else:
                break
        
        return cleaned.strip()