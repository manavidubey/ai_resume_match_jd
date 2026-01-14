from typing import Dict, Any, Tuple
from pathlib import Path
import tempfile
import os
from parsers.pdf_parser import PDFParser
from parsers.docx_parser import DocxParser
import logging

logger = logging.getLogger(__name__)

class ParsingService:
    def __init__(self):
        self.pdf_parser = PDFParser()
        self.docx_parser = DocxParser()
    
    def parse_resume(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a resume file and extract its content
        """
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension == '.pdf':
            content = self.pdf_parser.extract_text(file_path)
            metadata = self.pdf_parser.extract_metadata(file_path)
        elif file_extension in ['.docx', '.doc']:
            content = self.docx_parser.extract_text(file_path)
            metadata = self.docx_parser.extract_document_properties(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        return {
            "content": content,
            "metadata": metadata,
            "file_type": file_extension,
        }
    
    def parse_resume_from_bytes(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        """
        Parse a resume file from bytes and extract its content
        """
        file_extension = Path(filename).suffix.lower()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            temp_file.write(file_bytes)
            temp_file_path = temp_file.name
        
        try:
            parsed_data = self.parse_resume(temp_file_path)
        finally:
            os.unlink(temp_file_path)  # Clean up temporary file
        
        return parsed_data
    
    def validate_file_type(self, filename: str) -> bool:
        """
        Validate if the file type is supported
        """
        valid_extensions = {'.pdf', '.docx', '.doc'}
        return Path(filename).suffix.lower() in valid_extensions
    
    def get_file_size(self, file_path: str) -> int:
        """
        Get the size of a file in bytes
        """
        return os.path.getsize(file_path)
    
    def is_file_size_valid(self, file_path: str, max_size: int = 16 * 1024 * 1024) -> bool:
        """
        Check if file size is within the allowed limit
        """
        return self.get_file_size(file_path) <= max_size