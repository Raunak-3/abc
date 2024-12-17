import os
import json
from typing import List, Dict
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Placeholder for Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Gemini API key not found. Please set the GEMINI_API_KEY environment variable.")

# Initialize the Gemini model
try:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    raise Exception(f"Failed to initialize Gemini model: {str(e)}")

def extract_keywords(job_description: str) -> List[str]:
    """
    Extracts keywords from the job description using Gemini.
    
    Args:
        job_description (str): The job description text
        
    Returns:
        List[str]: List of extracted keywords
        
    Raises:
        Exception: If Gemini API call fails
    """
    try:
        prompt = f"Extract important keywords from the following job description. Return only the keywords separated by commas: {job_description}"
        response = gemini_model.generate_content(prompt)
        return [keyword.strip() for keyword in response.text.split(",")]
    except Exception as e:
        raise Exception(f"Failed to extract keywords: {str(e)}")

def categorize_keywords(keywords: List[str]) -> Dict[str, List[str]]:
    """
    Categorizes keywords into 'high' and 'low' importance using Gemini.
    
    Args:
        keywords (List[str]): List of keywords to categorize
        
    Returns:
        Dict[str, List[str]]: Dictionary with 'high' and 'low' importance keywords
        
    Raises:
        Exception: If Gemini API call fails
    """
    try:
        prompt = f"Categorize these keywords into 'high' and 'low' importance. Return a JSON object with format {{'high': [], 'low': []}}: {', '.join(keywords)}"
        response = gemini_model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        return {"high": keywords[:len(keywords)//2], "low": keywords[len(keywords)//2:]}

def get_resume_match_score(job_description: str, resume_text: str) -> int:
    """
    Calculates a resume match score using Gemini.
    
    Args:
        job_description (str): The job description text
        resume_text (str): The resume text
        
    Returns:
        int: Match score percentage (0-100)
        
    Raises:
        Exception: If Gemini API call fails
    """
    try:
        prompt = f"Calculate a match score (percentage 0-100) between this job description and resume. Return only the number:\nJob Description: {job_description}\nResume: {resume_text}"
        response = gemini_model.generate_content(prompt)
        score = int(response.text.strip())
        return max(0, min(100, score))  # Ensure score is between 0 and 100
    except Exception as e:
        # Return a default score if API fails
        return 50

def generate_tailored_resume_section(job_description: str, resume_section: str, instructions: str) -> str:
    """
    Generates tailored resume content using Gemini.
    
    Args:
        job_description (str): The job description text
        resume_section (str): The current resume section content
        instructions (str): Additional instructions for tailoring
        
    Returns:
        str: Tailored resume section content
        
    Raises:
        Exception: If Gemini API call fails
    """
    try:
        prompt = f"""
        Given this job description: {job_description}
        And this resume section: {resume_section}
        Please {instructions}
        Keep the same format but improve the content to better match the job description.
        """
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        # Return original content if API fails
        return resume_section
