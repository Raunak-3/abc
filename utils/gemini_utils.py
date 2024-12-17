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

def get_resume_match_score(job_description: str, resume_text: str) -> Dict[str, int]:
    """
    Calculates resume match scores using Gemini.
    
    Args:
        job_description (str): The job description text
        resume_text (str): The resume text
        
    Returns:
        Dict[str, int]: Dictionary containing overall and technical scores
        
    Raises:
        Exception: If Gemini API call fails
    """
    try:
        # Get overall match score
        overall_prompt = f"Calculate an overall match score (percentage 0-100) between this job description and resume. Return only the number:\nJob Description: {job_description}\nResume: {resume_text}"
        overall_response = gemini_model.generate_content(overall_prompt)
        overall_score = int(overall_response.text.strip())
        overall_score = max(0, min(100, overall_score))

        # Get technical skills match score
        technical_prompt = f"Calculate a technical skills match score (percentage 0-100) between this job description and resume, focusing only on technical skills, tools, and technologies. Return only the number:\nJob Description: {job_description}\nResume: {resume_text}"
        technical_response = gemini_model.generate_content(technical_prompt)
        technical_score = int(technical_response.text.strip())
        technical_score = max(0, min(100, technical_score))

        return {
            "overall_score": overall_score,
            "technical_score": technical_score
        }
    except Exception as e:
        # Return default scores if API fails
        return {
            "overall_score": 50,
            "technical_score": 50
        }

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
