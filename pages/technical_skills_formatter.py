import re
from pathlib import Path
import streamlit as st

def format_technical_skills():
    """Format technical skills in resume.tex with proper line breaks and formatting"""
    resume_path = Path("resumes/resume.tex")
    if not resume_path.exists():
        st.error("resume.tex not found in resumes directory")
        return
    
    # Read the current resume content
    content = resume_path.read_text()
    
    # Extract all technical skills from the content
    skills = []
    
    # Extract from technical skills section
    tech_pattern = r'Technical:&(.*?)\\\\[\s\n]*&([^\\]*)'
    tech_match = re.search(tech_pattern, content, re.DOTALL)
    if tech_match:
        # Get skills from both lines
        skills.extend([s.strip() for s in tech_match.group(1).split(',')])
        if tech_match.group(2):
            skills.extend([s.strip() for s in tech_match.group(2).split(',')])
    
    # Extract from projects section
    project_pattern = r'Tech Stack:}([^\\]+)'
    project_matches = re.finditer(project_pattern, content)
    for match in project_matches:
        tech_stack = match.group(1).strip()
        skills.extend([s.strip() for s in tech_stack.split(',')])
    
    # Clean and deduplicate skills
    skills = list(set([skill for skill in skills if skill and not skill.startswith('&')]))
    skills.sort()  # Sort alphabetically
    
    # Format skills into lines of ~90 characters
    current_line = "Technical:&"
    lines = []
    
    for skill in skills:
        # Check if adding this skill would exceed 90 characters
        if len(current_line + skill) > 90:
            lines.append(current_line.rstrip(', ') + '\\\\')
            current_line = "&"
        
        current_line += skill + ", "
    
    # Add the last line without trailing comma and without \\
    if current_line != "&":
        lines.append(current_line.rstrip(', '))
    
    # Create the new skills section
    new_skills_section = '\n'.join(lines)
    
    # Update the technical skills section in the content
    skills_pattern = r'(Technical:&.*?)(?=\\end{tabular})'
    updated_content = re.sub(skills_pattern, new_skills_section, content, flags=re.DOTALL)
    
    # Save the updated content
    resume_path.write_text(updated_content)
    st.success("Technical skills formatted successfully!")
    return True
