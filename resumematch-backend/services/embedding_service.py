from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer
import torch
import numpy as np
from typing import List, Union
import logging
from config import config

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self, model_name: str = None, model_type: str = "gpt2"):
        self.model_type = model_type
        
        if model_type == "gpt2":
            self.model_name = model_name or "openai-community/gpt2"
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            # Add padding token if it doesn't exist
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            # Set model to evaluation mode
            self.model.eval()
        elif model_type == "sentence_transformer":
            self.model_name = model_name or config.EMBEDDING_MODEL
            self.model = SentenceTransformer(self.model_name)
        elif model_type == "qwen":
            self.model_name = model_name or "Qwen/Qwen2.5-3B-Instruct"
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            # Set model to evaluation mode
            self.model.eval()
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
    
    def encode_text(self, text: str) -> List[float]:
        """
        Encode a single text string into an embedding vector
        """
        try:
            if self.model_type == "gpt2":
                # Tokenize the input text
                inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
                
                # Get model outputs (using the transformer layers, not the LM head)
                with torch.no_grad():
                    outputs = self.model.transformer(**inputs)
                    # Use the mean of the last hidden states as the embedding
                    hidden_states = outputs.last_hidden_state
                    embedding = torch.mean(hidden_states, dim=1).squeeze().numpy()
                
                return embedding.tolist()
            elif self.model_type == "sentence_transformer":
                embedding = self.model.encode(text)
                return embedding.tolist()
            elif self.model_type == "qwen":
                # For Qwen, we can use the transformer layers for embeddings
                inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
                
                with torch.no_grad():
                    outputs = self.model(**inputs, output_hidden_states=True)
                    # Use the last hidden state as the embedding
                    hidden_states = outputs.hidden_states[-1]  # Last layer
                    # Average over sequence length
                    embedding = torch.mean(hidden_states, dim=1).squeeze().numpy()
                
                return embedding.tolist()
        except Exception as e:
            logger.error(f"Error encoding text: {str(e)}")
            raise
    
    def encode_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Encode multiple text strings into embedding vectors
        """
        try:
            if self.model_type == "gpt2":
                # For GPT-2, encode texts one by one
                embeddings = []
                for text in texts:
                    embedding = self.encode_text(text)
                    embeddings.append(embedding)
                return embeddings
            elif self.model_type == "sentence_transformer":
                embeddings = self.model.encode(texts)
                return [embedding.tolist() for embedding in embeddings]
            elif self.model_type == "qwen":
                # For Qwen, encode texts one by one
                embeddings = []
                for text in texts:
                    embedding = self.encode_text(text)
                    embeddings.append(embedding)
                return embeddings
        except Exception as e:
            logger.error(f"Error encoding texts: {str(e)}")
            raise
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two embedding vectors
        """
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        
        # Normalize the vectors
        v1_norm = v1 / np.linalg.norm(v1)
        v2_norm = v2 / np.linalg.norm(v2)
        
        # Calculate cosine similarity
        similarity = np.dot(v1_norm, v2_norm)
        return float(similarity)
    
    def calculate_similarity_matrix(self, query_embedding: List[float], 
                                  candidate_embeddings: List[List[float]]) -> List[float]:
        """
        Calculate similarity between a query embedding and multiple candidate embeddings
        """
        similarities = []
        for candidate_embedding in candidate_embeddings:
            similarity = self.cosine_similarity(query_embedding, candidate_embedding)
            similarities.append(similarity)
        return similarities
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of the embeddings
        """
        sample_text = "sample text to determine embedding dimension"
        sample_embedding = self.encode_text(sample_text)
        return len(sample_embedding)