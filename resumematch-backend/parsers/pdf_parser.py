import fitz  # PyMuPDF
import io
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class PDFParser:
    def __init__(self):
        pass
    
    @staticmethod
    def extract_text(file_path: str) -> str:
        """
        Extract text from a PDF file using PyMuPDF
        """
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise
    
    @staticmethod
    def extract_text_from_bytes(pdf_bytes: bytes) -> str:
        """
        Extract text from PDF bytes
        """
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from PDF bytes: {str(e)}")
            raise
    
    @staticmethod
    def extract_metadata(file_path: str) -> Dict[str, Any]:
        """
        Extract metadata from PDF file
        """
        try:
            doc = fitz.open(file_path)
            metadata = doc.metadata
            doc.close()
            return {
                "title": metadata.get("title", ""),
                "author": metadata.get("author", ""),
                "subject": metadata.get("subject", ""),
                "creator": metadata.get("creator", ""),
                "producer": metadata.get("producer", ""),
                "pages": len(doc),
            }
        except Exception as e:
            logger.error(f"Error extracting PDF metadata: {str(e)}")
            return {}