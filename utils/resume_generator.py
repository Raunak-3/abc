import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import streamlit as st
import subprocess
import tempfile

# Load environment variables
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:
    st.error("""Google API Key not found! Please follow these steps:
    1. Create a file named '.env' (not '.env.example') in your project directory
    2. Add this line to the file: GOOGLE_API_KEY=your_actual_api_key_here
    3. Get an API key from https://makersuite.google.com/app/apikey if you don't have one
    """)
else:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
    except Exception as e:
        st.error(f"Error configuring Gemini AI: {str(e)}")

def generate_projects(job_description: str, job_title: str, technical_skills: list) -> list:
    """Generate relevant projects based on job description and skills"""
    try:
        prompt = f"""Generate 3 industrial-level projects that match this job description and title:
        Job Title: {job_title}
        Job Description: {job_description}
        Technical Skills: {', '.join(technical_skills)}

        Rules for projects:
        1. Projects should be simple but industrial level
        2. Project names should explicitly mention the main technologies used
        3. Each project should use multiple skills from the job description
        4. Include specific technical details and metrics where possible
        5. Format each project as a dictionary with:
           - name: Project name
           - description: Project description
           - tech_stack: List of technologies used

        Return the projects in this exact JSON format:
        [
            {
                "name": "Project Name",
                "description": "Project Description",
                "tech_stack": ["Tech1", "Tech2"]
            }
        ]"""

        response = model.generate_content(prompt)
        try:
            # Extract JSON from response
            projects = json.loads(response.text)
            return projects
        except json.JSONDecodeError as e:
            st.error(f"Failed to parse Gemini response as JSON: {str(e)}")
            st.text("Response received:")
            st.text(response.text)
            return []
    except Exception as e:
        st.error(f"Error generating projects: {str(e)}")
        return []

def generate_latex_resume(personal_info: dict, education: dict, job_description: str, 
                         job_title: str, technical_skills: list, soft_skills: list) -> str:
    """Generate LaTeX resume content and compile to PDF"""
    try:
        # Generate projects using Gemini
        st.info("Generating projects with AI...")
        projects = generate_projects(job_description, job_title, technical_skills)
        
        if not projects:
            st.warning("No projects were generated. Using placeholder projects...")
            projects = [
                {
                    "name": "Sample Project 1",
                    "description": "A placeholder project description.",
                    "tech_stack": technical_skills[:3] if technical_skills else ["Python"]
                }
            ]
        
        # Standard skills to include in every resume
        standard_skills = [
            "C++", "Data Structures and Algorithms", "SQL", "Python",
            "REST API", "Object-Oriented Programming", "Computer Networking"
        ]
        
        # Combine standard skills with job-specific skills
        all_technical_skills = list(set(technical_skills + standard_skills))
        
        st.info("Generating LaTeX content...")
        # Create the LaTeX content with proper escaping
        latex_content = f"""\\documentclass{{resume}}
\\usepackage[left=0.4 in,top=0.3in,right=0.4 in,bottom=0.3in]{{geometry}}
\\newcommand{{\\tab}}[1]{{\\hspace{{.2667\\textwidth}}\\rlap{{#1}}}}
\\newcommand{{\\itab}}[1]{{\\hspace{{0em}}\\rlap{{#1}}}}

\\name{{{personal_info['name']}}}
\\address{{{personal_info['location']}}} \\quad {{\\textbf{{{personal_info['phone']}}}}} \\quad 
\\href{{mailto:{personal_info['email']}}}{{{personal_info['email']}}} \\\\ 
\\href{{{personal_info['linkedin']}}}{{LinkedIn}} \\quad
\\href{{{personal_info['github']}}}{{GitHub}} \\quad
\\href{{{personal_info['website']}}}{{Website}}

\\begin{{document}}

\\begin{{rSection}}{{Education}}
{{\\bf {education['institute']}}}, {education['degree']} \\hfill {{{education['duration']}}}\\\\
{education['major']} \\hfill {{CGPA: {education['cgpa']}}}
\\end{{rSection}}

\\begin{{rSection}}{{SKILLS}}
\\begin{{tabular}}{{@{{}} >{{\\bfseries}}l @{{\\hspace{{2ex}}}} l}}
Technical Skills: & {', '.join(all_technical_skills[:len(all_technical_skills)//2])} \\\\
                 & {', '.join(all_technical_skills[len(all_technical_skills)//2:])} \\\\
\\end{{tabular}}\\\\[2mm]
\\begin{{tabular}}{{@{{}} >{{\\bfseries}}l @{{\\hspace{{2ex}}}} l}}
Soft Skills: & {', '.join(soft_skills)} \\\\
\\end{{tabular}}
\\end{{rSection}}

\\begin{{rSection}}{{PROJECTS}}
"""

        # Add projects
        for project in projects:
            latex_content += f"""\\item \\textbf{{{project['name']}: }}
{project['description']}\\\\
\\textbf{{Tech Stack:}} {', '.join(project['tech_stack'])}
\\vspace{{-1.5mm}}
"""

        # Close the document
        latex_content += """
\\end{rSection}
\\end{document}
"""
        
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            tex_file_path = os.path.join(temp_dir, "resume.tex")
            pdf_file_path = os.path.join(temp_dir, "resume.pdf")

            # Write LaTeX content to a .tex file
            with open(tex_file_path, "w", encoding="utf-8") as tex_file:
                tex_file.write(latex_content)

            # Compile LaTeX to PDF using pdflatex
            try:
                subprocess.run(["pdflatex", "-output-directory", temp_dir, tex_file_path], check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                 st.error(f"Error compiling LaTeX to PDF: {e.stderr.decode()}")
                 return ""

            return pdf_file_path

    except Exception as e:
        st.error(f"Error generating resume: {str(e)}")
        return ""
