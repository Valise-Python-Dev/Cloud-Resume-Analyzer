import io
import docx
from pdfminer.high_level import extract_text
import logging

logger = logging.getLogger(__name__)

def extract_text_from_file(file_path: str, content_type: str = "") -> str:
    """
    Determines file type and extracts text from local file path.
    """
    try:
        if file_path.endswith(".pdf"):
            return extract_text(file_path)
            
        elif file_path.endswith(".docx"):
            doc = docx.Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
            
        else:
            raise ValueError("Unsupported file format")
            
    except Exception as e:
        logger.error(f"Text extraction failed for {file_path}: {e}")
        return ""