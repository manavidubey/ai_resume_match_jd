from typing import List, Dict, Any
from services.embedding_service import EmbeddingService
import logging

logger = logging.getLogger(__name__)

class EmbeddingExtractor:
    def __init__(self, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service
    
    def extract_embeddings_from_resume(self, resume_content: str) -> List[float]:
        """
        Extract embeddings from resume content
        """
        try:
            return self.embedding_service.encode_text(resume_content)
        except Exception as e:
            logger.error(f"Error extracting embeddings from resume: {str(e)}")
            raise
    
    def extract_embeddings_from_job_description(self, job_description: str) -> List[float]:
        """
        Extract embeddings from job description
        """
        try:
            return self.embedding_service.encode_text(job_description)
        except Exception as e:
            logger.error(f"Error extracting embeddings from job description: {str(e)}")
            raise
    
    def extract_embeddings_from_segments(self, segments: List[str]) -> List[List[float]]:
        """
        Extract embeddings from multiple text segments
        """
        try:
            return self.embedding_service.encode_texts(segments)
        except Exception as e:
            logger.error(f"Error extracting embeddings from segments: {str(e)}")
            raise
    
    def compute_similarity(self, resume_embedding: List[float], 
                          job_embedding: List[float]) -> float:
        """
        Compute similarity between resume and job description embeddings
        """
        try:
            return self.embedding_service.cosine_similarity(resume_embedding, job_embedding)
        except Exception as e:
            logger.error(f"Error computing similarity: {str(e)}")
            raise
    
    def rank_candidates(self, query_embedding: List[float], 
                       candidate_embeddings: List[List[float]]) -> List[Dict[str, Any]]:
        """
        Rank candidates based on similarity to query
        """
        try:
            similarities = self.embedding_service.calculate_similarity_matrix(
                query_embedding, candidate_embeddings
            )
            
            # Create ranked results
            ranked_results = [
                {"index": i, "similarity": sim} 
                for i, sim in enumerate(similarities)
            ]
            
            # Sort by similarity in descending order
            ranked_results.sort(key=lambda x: x["similarity"], reverse=True)
            
            return ranked_results
        except Exception as e:
            logger.error(f"Error ranking candidates: {str(e)}")
            raise