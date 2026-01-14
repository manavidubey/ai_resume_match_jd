import re
from typing import List, Dict, Set
import spacy
from collections import Counter
import logging

logger = logging.getLogger(__name__)

class SkillExtractor:
    def __init__(self):
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("spaCy model 'en_core_web_sm' not found. Please install it with: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Define common technical skills
        self.technical_skills = {
            # Programming languages
            "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "php", "go", "rust", "scala",
            "swift", "kotlin", "dart", "r", "matlab", "perl", "sql", "html", "css", "sass", "less",
            
            # Frameworks and Libraries
            "react", "angular", "vue", "node.js", "express", "django", "flask", "spring", "spring boot",
            "laravel", "rails", "tensorflow", "pytorch", "keras", "pandas", "numpy", "scikit-learn",
            "bootstrap", "jquery", "redux", "graphql", "rest", "soap",
            
            # Databases
            "mysql", "postgresql", "mongodb", "redis", "oracle", "sqlite", "mssql", "cassandra", "elasticsearch",
            
            # Cloud Platforms
            "aws", "azure", "google cloud", "gcp", "docker", "kubernetes", "terraform", "jenkins", "git", "github",
            "gitlab", "bitbucket", "ci/cd", "devops",
            
            # Other Technical Skills
            "linux", "unix", "bash", "powershell", "agile", "scrum", "kanban", "jira", "salesforce", "sap",
            "adobe", "figma", "sketch", "invision", "illustrator", "photoshop", "excel", "tableau", "power bi",
            "hadoop", "spark", "hive", "pig", "kafka", "airflow",
        }
        
        # Define soft skills
        self.soft_skills = {
            "communication", "leadership", "teamwork", "problem-solving", "adaptability", "creativity",
            "critical thinking", "time management", "decision making", "negotiation", "conflict resolution",
            "emotional intelligence", "interpersonal skills", "collaboration", "attention to detail",
            "organizational skills", "analytical thinking", "customer service", "presentation skills",
            "project management", "strategic thinking", "innovation", "accountability", "integrity",
            "punctuality", "reliability", "flexibility", "resilience", "patience", "empathy",
        }
    
    def extract_skills_from_text(self, text: str) -> Dict[str, List[str]]:
        """
        Extract both technical and soft skills from text
        """
        # Preprocess text
        processed_text = self._preprocess_text(text.lower())
        
        # Extract skills
        technical_skills_found = self._find_skills(processed_text, self.technical_skills)
        soft_skills_found = self._find_skills(processed_text, self.soft_skills)
        
        # Return as dictionary
        return {
            "technical_skills": list(set(technical_skills_found)),
            "soft_skills": list(set(soft_skills_found))
        }
    
    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text by removing punctuation and extra spaces
        """
        # Remove special characters and replace with spaces
        text = re.sub(r'[\-_/]', ' ', text)
        # Remove other special characters but keep spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        # Normalize whitespace
        text = ' '.join(text.split())
        return text
    
    def _find_skills(self, text: str, skill_set: Set[str]) -> List[str]:
        """
        Find skills from a given skill set in the text
        """
        found_skills = []
        for skill in skill_set:
            # Use word boundaries to match whole words
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                found_skills.append(skill)
        return found_skills
    
    def extract_entities_with_spacy(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities using spaCy
        """
        if not self.nlp:
            return {"entities": [], "organizations": [], "dates": [], "locations": []}
        
        doc = self.nlp(text)
        
        entities = {
            "entities": [(ent.text, ent.label_) for ent in doc.ents],
            "organizations": [ent.text for ent in doc.ents if ent.label_ in ["ORG", "NORP"]],
            "dates": [ent.text for ent in doc.ents if ent.label_ in ["DATE", "TIME"]],
            "locations": [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]],
        }
        
        return entities
    
    def extract_keywords(self, text: str, num_keywords: int = 10) -> List[str]:
        """
        Extract top keywords from text using TF-IDF approach
        """
        # Tokenize text
        doc = self.nlp(text) if self.nlp else None
        
        if doc:
            # Filter tokens: remove stop words, punctuations, and get nouns/adjectives
            tokens = [token.lemma_.lower() for token in doc 
                     if not token.is_stop and not token.is_punct and 
                     token.pos_ in ["NOUN", "ADJ"] and len(token.text) > 2]
        else:
            # Simple fallback without spaCy
            tokens = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
            tokens = [token for token in tokens if token not in {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'who', 'boy', 'did', 'she', 'too', 'use'}]
        
        # Count frequency of tokens
        token_counts = Counter(tokens)
        
        # Return top N keywords
        return [token for token, count in token_counts.most_common(num_keywords)]