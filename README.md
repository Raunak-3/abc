# Resume Tailoring Application

This application helps you tailor your resume to specific job descriptions using AI-powered analysis and suggestions.

## Features

- Upload and manage multiple resumes
- Extract keywords from job descriptions using Gemini AI
- Get resume-job match scores
- Generate tailored resume sections
- Real-time PDF preview
- Automatic project generation based on job requirements
- Keyword matching and analysis
- LaTeX-based resume generation

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your environment:
- Copy `.env.example` to `.env`
- Add your Gemini API key to the `.env` file

## Running the Application

Run the Streamlit app:
```bash
streamlit run main.py
```

## Usage

1. Upload your resume or select an existing one
2. Enter job description and title
3. Analyze resume to get keyword matches
4. Use the Resume Tailor page to:
   - View and edit LaTeX source
   - See real-time PDF preview
   - Track keyword matches
   - Generate tailored projects
   - Update skills based on job requirements
