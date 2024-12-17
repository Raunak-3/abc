from typing import List, Dict
import re
import spacy
from collections import Counter

# Load spaCy model for better text processing
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_keywords_from_text(text: str) -> List[str]:
    """
    Extract important keywords from text using spaCy
    """
    doc = nlp(text.lower())
    
    # Extract nouns, proper nouns, and technical terms
    keywords = []
    for token in doc:
        if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 2:
            keywords.append(token.text)
    
    # Add compound words (e.g., "machine learning")
    for chunk in doc.noun_chunks:
        if len(chunk.text.split()) > 1:
            keywords.append(chunk.text)
    
    # Clean and deduplicate keywords
    keywords = list(set(keywords))
    return keywords

def is_technical_skill(keyword: str) -> bool:
    """
    Determine if a keyword is likely a technical skill
    """
    technical_indicators = [
        'programming', 'language', 'framework', 'database', 'cloud',
        'software', 'development', 'engineering', 'api', 'code',
        'git', 'aws', 'azure', 'python', 'java', 'javascript',
        'react', 'node', 'sql', 'nosql', 'docker', 'kubernetes'
    ]
    
    return any(indicator in keyword.lower() for indicator in technical_indicators)

def categorize_keywords(keywords: List[str]) -> Dict[str, List[str]]:
    """
    Categorize keywords into technical (high priority) and soft skills (low priority)
    """
    categorized = {
        "high": [],
        "low": []
    }
    
    for keyword in keywords:
        if is_technical_skill(keyword):
            categorized["high"].append(keyword)
        else:
            categorized["low"].append(keyword)
    
    return categorized

def calculate_keyword_match_score(job_description: str, resume_text: str, keywords: List[str]) -> float:
    """
    Calculate the percentage of keywords from job description found in resume
    """
    resume_text = resume_text.lower()
    matched_keywords = 0
    
    for keyword in keywords:
        if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', resume_text):
            matched_keywords += 1
    
    return round((matched_keywords / len(keywords)) * 100, 1) if keywords else 0

def calculate_technical_skills_match_score(job_description: str, resume_text: str) -> float:
    """
    Calculate technical skills match score
    """
    keywords = extract_keywords_from_text(job_description)
    categorized = categorize_keywords(keywords)
    technical_keywords = categorized["high"]
    
    if not technical_keywords:
        return 0.0
        
    return calculate_keyword_match_score(job_description, resume_text, technical_keywords)

def get_keyword_matches(keywords: List[str], resume_text: str) -> Dict[str, bool]:
    """
    Get a dictionary of keywords and whether they match in the resume
    """
    matches = {}
    resume_text = resume_text.lower()
    
    for keyword in keywords:
        matches[keyword] = bool(re.search(r'\b' + re.escape(keyword.lower()) + r'\b', resume_text))
    
    return matches
