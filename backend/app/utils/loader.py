import os
import asyncio
from pathlib import Path
from typing import List, Dict, Any
import markdown
from bs4 import BeautifulSoup
import aiofiles


async def load_docusaurus_docs(docs_dir: str) -> List[Dict[str, Any]]:
    """
    Load all .md and .mdx files from a Docusaurus docs directory
    Args:
        docs_dir: Path to the Docusaurus docs folder
    Returns:
        List of dictionaries containing document info
    """
    files = []
    docs_path = Path(docs_dir)
    
    # Get all markdown and mdx files
    doc_extensions = ['.md', '.mdx']
    for ext in doc_extensions:
        for file_path in docs_path.rglob(f'*{ext}'):
            if file_path.is_file():
                relative_path = file_path.relative_to(docs_path)
                
                # Extract document title from the file
                title = await extract_title_from_markdown(file_path)
                
                # Read the file content
                content = await read_file_async(file_path)
                
                files.append({
                    'source_path': str(relative_path),
                    'content': content,
                    'title': title or file_path.stem,
                    'checksum': hash(content)
                })
    
    return files


async def extract_title_from_markdown(file_path: Path) -> str:
    """Extract title from markdown file (from heading or frontmatter)"""
    content = await read_file_async(file_path)
    
    # Look for frontmatter title (common in Docusaurus)
    lines = content.split('\n')
    for line in lines[:10]:  # Check first 10 lines for frontmatter
        if line.startswith('title:'):
            title = line.replace('title:', '', 1).strip().strip('"\'')
            return title
    
    # If no frontmatter title, look for H1
    for line in lines:
        if line.startswith('# '):
            return line.replace('# ', '', 1).strip()
    
    return ""


async def read_file_async(path: Path) -> str:
    """Read file asynchronously"""
    async with aiofiles.open(path, 'r', encoding='utf-8') as f:
        content = await f.read()
    return content


def extract_text_from_markdown(md_content: str) -> str:
    """Convert markdown to plain text using BeautifulSoup"""
    html = markdown.markdown(md_content)
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()