from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from typing import Dict, List
import logging
import re

logger = logging.getLogger(__name__)

class QwenService:
    def __init__(self, model_name: str = "Qwen/Qwen2.5-3B-Instruct"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.model.eval()
    
    def generate_match_explanation(self, resume_content: str, job_description: str, match_score: float) -> str:
        """
        Generate an explanation for how well the resume matches the job description using Qwen
        """
        prompt = f"""You are an expert at analyzing resume-job matches. Explain how this resume matches the job description.

Resume: {resume_content[:1000]}...

Job Description: {job_description[:1000]}...

Match Score: {match_score:.2f}/1.0

Provide a detailed explanation of:
1. Which skills from the job description are present in the resume
2. Which skills are missing and could be added
3. How the candidate's experience aligns with the job requirements
4. Specific recommendations for improving the match

Explanation:"""
        
        try:
            inputs = self.tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=1024)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs, 
                    max_length=len(inputs[0]) + 150,
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
            logger.error(f"Error generating match explanation with Qwen: {str(e)}")
            # Fallback explanation
            return f"The candidate shows a match score of {match_score:.2f}, indicating {'strong' if match_score > 0.7 else 'moderate' if match_score > 0.5 else 'weak'} alignment with the job requirements."

    def generate_improvement_suggestions(self, resume_content: str, job_description: str) -> str:
        """
        Generate specific suggestions for improving the resume to better match the job
        """
        prompt = f"""As a career advisor, provide specific suggestions to improve this resume to better match the job description.

Resume: {resume_content[:800]}...

Job Description: {job_description[:800]}...

Provide specific, actionable suggestions for:
1. Skills to highlight or add
2. Experience to emphasize
3. Keywords to include
4. Formatting improvements

Suggestions:"""
        
        try:
            inputs = self.tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=1024)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs, 
                    max_length=len(inputs[0]) + 120,
                    temperature=0.6,
                    pad_token_id=self.tokenizer.eos_token_id,
                    do_sample=True,
                    num_return_sequences=1
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            suggestions = response[len(prompt):].strip()
            suggestions = self._clean_generated_text(suggestions)
            
            return suggestions
        except Exception as e:
            logger.error(f"Error generating improvement suggestions with Qwen: {str(e)}")
            return "Consider highlighting relevant skills and experiences that directly match the job requirements."

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
            if len(cleaned + sentence) < 300:  # Limit length
                cleaned += sentence + " "
            else:
                break
        
        return cleaned.strip()