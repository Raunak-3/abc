# Resume Tailoring Application

This application helps you tailor your resume to specific job descriptions using AI-powered analysis and suggestions.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your environment:
- Copy `.env.example` to `.env`
- Add your Gemini API key to the `.env` file

3. Create a `resumes` directory and add your base resume(s) as JSON files with the following structure:
```json
{
    "work_experience": "Your work experience here",
    "education": "Your education details here",
    "skills": "Your skills here"
}
```

## Running the Application

Run the Streamlit app:
```bash
streamlit run main.py
```

## Features

- Upload and manage multiple resumes
- Extract keywords from job descriptions
- Get resume-job match scores
- Generate tailored resume sections
- Preview and save tailored resumes
