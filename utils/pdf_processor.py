import fitz  # PyMuPDF
import re
from typing import Optional, List

def extract_text_from_pdf(pdf_path: str) -> Optional[str]:
    """Extract text from PDF with error handling and cleanup"""
    try:
        text_blocks = []
        with fitz.open(pdf_path) as doc:
            for page in doc:
                page_text = page.get_text()
                # Clean up common OCR/PDF extraction issues
                page_text = re.sub(r'\s+', ' ', page_text)  # Remove excessive whitespace
                page_text = re.sub(r'(\w)-\s+(\w)', r'\1\2', page_text)  # Fix hyphenated words
                text_blocks.append(page_text)
        
        return "\n".join(text_blocks)
    except Exception as e:
        print(f"PDF Error: {e}")
        return None

def chunk_text(text: str, max_words: int = 1500, overlap: int = 200) -> List[str]:
    """
    Split text into word-based chunks with overlap to maintain context
    
    Args:
        text: The text to split
        max_words: Maximum words per chunk
        overlap: Number of words to overlap between chunks
    
    Returns:
        List of text chunks
    """
    words = text.split()
    
    if len(words) <= max_words:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(words):
        end = min(start + max_words, len(words))
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        
        # Move start pointer with overlap
        start += max_words - overlap
        if start >= len(words):
            break
    
    return chunks