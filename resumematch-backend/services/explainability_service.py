from typing import Dict, List, Any
from ..models.candidate import MatchAnalysis
import logging

logger = logging.getLogger(__name__)

class ExplainabilityService:
    def __init__(self):
        pass
    
    def generate_match_explanation(self, match_analysis: MatchAnalysis) -> Dict[str, Any]:
        """
        Generate a comprehensive explanation for the match analysis
        """
        try:
            explanation = {
                "overall_assessment": self._generate_overall_assessment(
                    match_analysis.match_score.overall_score
                ),
                "skills_analysis": self._generate_skills_analysis(
                    match_analysis.matched_skills,
                    match_analysis.missing_skills,
                    match_analysis.transferable_skills,
                    match_analysis.match_score.skills_score
                ),
                "experience_insights": self._generate_experience_insights(
                    match_analysis.experience_summary,
                    match_analysis.match_score.experience_score
                ),
                "role_fit_evaluation": self._generate_role_fit_evaluation(
                    match_analysis.match_score.role_fit_score
                ),
                "recommendation": self._generate_final_recommendation(
                    match_analysis.role_recommendation,
                    match_analysis.match_score.overall_score
                ),
                "actionable_feedback": self._generate_actionable_feedback(
                    match_analysis.missing_skills
                ),
                "confidence_level": self._determine_confidence_level(
                    match_analysis.match_score.overall_score
                )
            }
            
            return explanation
        except Exception as e:
            logger.error(f"Error generating match explanation: {str(e)}")
            raise
    
    def _generate_overall_assessment(self, overall_score: float) -> str:
        """
        Generate overall assessment based on the overall score
        """
        if overall_score >= 0.8:
            return "Excellent Match - Strong alignment with job requirements"
        elif overall_score >= 0.6:
            return "Good Match - Solid alignment with minor gaps"
        elif overall_score >= 0.4:
            return "Partial Match - Some alignment with significant gaps"
        elif overall_score >= 0.2:
            return "Weak Match - Limited alignment with major gaps"
        else:
            return "Poor Match - Minimal alignment with job requirements"
    
    def _generate_skills_analysis(self, matched_skills: List[str], 
                                missing_skills: List[str], 
                                transferable_skills: List[str], 
                                skills_score: float) -> Dict[str, Any]:
        """
        Generate detailed skills analysis
        """
        analysis = {
            "summary": f"Skills match score: {skills_score:.2f}",
            "matched_skills_count": len(matched_skills),
            "missing_skills_count": len(missing_skills),
            "transferable_skills_count": len(transferable_skills),
            "matched_skills": matched_skills[:10],  # Limit to first 10 for readability
            "missing_skills": missing_skills[:10],
            "transferable_skills": transferable_skills[:10],
            "skills_alignment_level": self._determine_alignment_level(skills_score),
            "key_strengths": self._identify_key_strengths(matched_skills),
            "critical_gaps": self._identify_critical_gaps(missing_skills)
        }
        
        return analysis
    
    def _generate_experience_insights(self, experience_summary: str, 
                                    experience_score: float) -> Dict[str, Any]:
        """
        Generate insights about experience match
        """
        return {
            "summary": experience_summary,
            "experience_score": experience_score,
            "experience_alignment_level": self._determine_alignment_level(experience_score),
            "relevance_assessment": self._assess_experience_relevance(experience_score),
            "experience_brief": self._generate_experience_brief(experience_summary)
        }
    
    def _generate_role_fit_evaluation(self, role_fit_score: float) -> Dict[str, Any]:
        """
        Evaluate how well the candidate fits the role
        """
        return {
            "semantic_similarity": role_fit_score,
            "role_fit_level": self._determine_alignment_level(role_fit_score),
            "contextual_relevance": self._assess_contextual_relevance(role_fit_score),
            "fit_factors": self._identify_fit_factors(role_fit_score)
        }
    
    def _generate_final_recommendation(self, role_recommendation: str, 
                                     overall_score: float) -> Dict[str, str]:
        """
        Generate final recommendation
        """
        confidence = self._determine_confidence_level(overall_score)
        
        return {
            "recommendation": role_recommendation,
            "confidence": confidence,
            "next_steps": self._suggest_next_steps(overall_score)
        }
    
    def _generate_actionable_feedback(self, missing_skills: List[str]) -> List[str]:
        """
        Generate actionable feedback for improvement
        """
        feedback_items = []
        
        if missing_skills:
            feedback_items.append(
                f"Consider acquiring these key skills: {', '.join(missing_skills[:3])}"
            )
        
        if len(missing_skills) > 3:
            feedback_items.append(
                f"Also consider developing additional skills from: {', '.join(missing_skills[3:6])}"
            )
        
        feedback_items.extend([
            "Focus on highlighting transferable skills from your experience",
            "Consider pursuing relevant certifications to bridge skill gaps",
            "Emphasize projects or experiences that demonstrate relevant competencies"
        ])
        
        return feedback_items
    
    def _determine_confidence_level(self, score: float) -> str:
        """
        Determine confidence level based on score
        """
        if score >= 0.8:
            return "High Confidence"
        elif score >= 0.6:
            return "Medium Confidence"
        elif score >= 0.4:
            return "Low Confidence"
        else:
            return "Very Low Confidence"
    
    def _determine_alignment_level(self, score: float) -> str:
        """
        Determine alignment level based on score
        """
        if score >= 0.8:
            return "Excellent"
        elif score >= 0.6:
            return "Good"
        elif score >= 0.4:
            return "Fair"
        elif score >= 0.2:
            return "Poor"
        else:
            return "Very Poor"
    
    def _identify_key_strengths(self, matched_skills: List[str]) -> List[str]:
        """
        Identify key strengths from matched skills
        """
        if not matched_skills:
            return []
        
        # Return top 5 matched skills as key strengths
        return matched_skills[:min(5, len(matched_skills))]
    
    def _identify_critical_gaps(self, missing_skills: List[str]) -> List[str]:
        """
        Identify critical gaps from missing skills
        """
        if not missing_skills:
            return []
        
        # Return top 5 missing skills as critical gaps
        return missing_skills[:min(5, len(missing_skills))]
    
    def _assess_experience_relevance(self, experience_score: float) -> str:
        """
        Assess experience relevance
        """
        if experience_score >= 0.8:
            return "Highly relevant experience with strong alignment to role requirements"
        elif experience_score >= 0.6:
            return "Moderately relevant experience with good alignment"
        elif experience_score >= 0.4:
            return "Some relevant experience but with notable gaps"
        else:
            return "Limited relevant experience for this role"
    
    def _generate_experience_brief(self, experience_summary: str) -> str:
        """
        Generate brief experience summary
        """
        # Return the first 100 characters of the summary
        return experience_summary[:100] + "..." if len(experience_summary) > 100 else experience_summary
    
    def _assess_contextual_relevance(self, role_fit_score: float) -> str:
        """
        Assess contextual relevance
        """
        if role_fit_score >= 0.8:
            return "Strong contextual alignment with job requirements and responsibilities"
        elif role_fit_score >= 0.6:
            return "Good contextual alignment with most job requirements"
        elif role_fit_score >= 0.4:
            return "Partial contextual alignment with some overlap"
        else:
            return "Limited contextual alignment with job requirements"
    
    def _identify_fit_factors(self, role_fit_score: float) -> List[str]:
        """
        Identify key factors affecting role fit
        """
        if role_fit_score >= 0.8:
            return ["Strong semantic alignment", "Good role comprehension", "Relevant background"]
        elif role_fit_score >= 0.6:
            return ["Moderate semantic alignment", "Decent role comprehension"]
        elif role_fit_score >= 0.4:
            return ["Partial semantic alignment", "Limited role alignment"]
        else:
            return ["Weak semantic alignment", "Poor role alignment"]
    
    def _suggest_next_steps(self, overall_score: float) -> str:
        """
        Suggest next steps based on overall score
        """
        if overall_score >= 0.8:
            return "Proceed with interview process"
        elif overall_score >= 0.6:
            return "Consider for interview with additional screening"
        elif overall_score >= 0.4:
            return "Evaluate other candidates first"
        else:
            return "Not recommended for this role"
    
    def create_explanation_report(self, match_analysis: MatchAnalysis) -> Dict[str, Any]:
        """
        Create a comprehensive explanation report
        """
        explanation = self.generate_match_explanation(match_analysis)
        
        report = {
            "report_type": "Match Explanation Report",
            "timestamp": "generated_at_runtime",
            "analysis_summary": {
                "overall_score": match_analysis.match_score.overall_score,
                "skills_score": match_analysis.match_score.skills_score,
                "experience_score": match_analysis.match_score.experience_score,
                "role_fit_score": match_analysis.match_score.role_fit_score,
                "bonus_signals_score": match_analysis.match_score.bonus_signals_score,
            },
            "detailed_explanation": explanation,
            "highlights": self._extract_highlights(explanation),
            "summary": match_analysis.explanation
        }
        
        return report
    
    def _extract_highlights(self, explanation: Dict[str, Any]) -> List[str]:
        """
        Extract key highlights from the explanation
        """
        highlights = []
        
        # Add overall assessment
        highlights.append(explanation.get("overall_assessment", ""))
        
        # Add skills summary
        skills_analysis = explanation.get("skills_analysis", {})
        if "summary" in skills_analysis:
            highlights.append(skills_analysis["summary"])
        
        # Add recommendation
        recommendation = explanation.get("recommendation", {})
        if "recommendation" in recommendation:
            highlights.append(recommendation["recommendation"])
        
        # Filter out empty strings
        return [h for h in highlights if h]