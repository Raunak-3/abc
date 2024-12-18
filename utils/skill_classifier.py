import google.generativeai as genai
from typing import Tuple, List, Dict
import os
from dotenv import load_dotenv
import json

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

SKILL_PROMPT = """
Given a job description, classify all mentioned skills into two categories and generate 3 industry-level projects.
Return your response in the following JSON format ONLY (no other text):
{
    "technical_skills": ["skill1", "skill2"],
    "soft_skills": ["skill1", "skill2"],
    "projects": [
        {
            "title": "Project name that includes key technologies",
            "description": "Detailed description highlighting technical skills",
            "tech_stack": ["tech1", "tech2"]
        }
    ]
}

Job Description: """

def classify_skills_and_generate_projects(job_title: str, job_description: str) -> Dict:
    """
    Classify skills from job description and generate matching projects
    """
    try:
        full_prompt = f"Job Title: {job_title}\n\n{SKILL_PROMPT}\n{job_description}"
        response = model.generate_content(full_prompt)
        
        # Parse the JSON response
        try:
            result = json.loads(response.text)
        except json.JSONDecodeError:
            # If JSON parsing fails, try to clean the response
            cleaned_response = response.text.strip()
            # Remove any markdown code block markers if present
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            result = json.loads(cleaned_response.strip())
        
        # Add mandatory technical skills
        result['technical_skills'].extend([
            "C++",
            "Data Structures and Algorithms",
            "SQL",
            "Python",
            "REST API",
            "Object-Oriented Programming",
            "Computer Networking"
        ])
        
        # Remove duplicates while preserving order
        result['technical_skills'] = list(dict.fromkeys(result['technical_skills']))
        
        return result
    except Exception as e:
        print(f"Error in skill classification: {str(e)}")
        return {
            "technical_skills": [],
            "soft_skills": [],
            "projects": []
        }
