import re
from typing import List


def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespaces, special characters, etc.
    """
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep alphanumeric, spaces, and common punctuation
    text = re.sub(r'[^\w\s\-\.\,\!\?\;\:\(\)]', ' ', text)
    
    # Trim leading/trailing whitespace
    text = text.strip()
    
    return text


def remove_code_blocks(text: str) -> str:
    """
    Remove code blocks from markdown text
    """
    # Remove fenced code blocks (```...```)
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    
    # Remove inline code (backticks)
    text = re.sub(r'`[^`]*`', '', text)
    
    return text


def remove_links_and_images(text: str) -> str:
    """
    Remove markdown links and images
    """
    # Remove images ![alt](url)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    
    # Remove links [text](url)
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    
    return text


def preprocess_document(text: str) -> str:
    """
    Full preprocessing pipeline for a document
    """
    # Remove code blocks first
    text = remove_code_blocks(text)
    
    # Remove links and images
    text = remove_links_and_images(text)
    
    # Clean remaining text
    text = clean_text(text)
    
    return text