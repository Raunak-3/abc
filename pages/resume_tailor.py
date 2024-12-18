import streamlit as st
import os
import tempfile
import subprocess
from pathlib import Path
import base64
from utils.skill_classifier import classify_skills_and_generate_projects
from utils.local_match_utils import get_keyword_matches, calculate_technical_skills_match_score
import shutil

def render_latex_preview(tex_content: str) -> str:
    """
    Compile LaTeX content and return the path to the generated PDF
    """
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Write tex content to temporary file
            tex_path = os.path.join(temp_dir, "resume.tex")
            with open(tex_path, "w", encoding="utf-8") as f:
                f.write(tex_content)
            
            # Copy resume.cls and any other necessary files to temp directory
            cls_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resumes", "resume.cls")
            if os.path.exists(cls_path):
                shutil.copy2(cls_path, temp_dir)
            else:
                st.error(f"Could not find resume.cls at {cls_path}")
                return None
            
            # Run pdflatex twice to resolve references
            for _ in range(2):
                result = subprocess.run(
                    ["pdflatex", "-interaction=nonstopmode", "resume.tex"],
                    cwd=temp_dir,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    error_log = result.stdout + "\n" + result.stderr
                    st.error("LaTeX Compilation Error:")
                    # Extract relevant error message
                    error_lines = error_log.split('\n')
                    for i, line in enumerate(error_lines):
                        if "!" in line:  # LaTeX error lines start with !
                            context = error_lines[i:i+3]  # Show error and next 2 lines
                            st.code("\n".join(context))
                            break
                    return None
            
            # Read the generated PDF
            pdf_path = os.path.join(temp_dir, "resume.pdf")
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    return base64.b64encode(f.read()).decode()
            else:
                st.error("PDF file was not generated")
                return None
                
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        return None

def update_resume_content(original_content: str, skills_data: dict) -> str:
    """
    Update the resume content with new skills and projects
    """
    lines = original_content.split('\n')
    new_content = []
    in_skills_section = False
    in_projects_section = False
    skills_added = False
    projects_added = False

    for line in lines:
        if '\\begin{rSection}{SKILLS}' in line:
            in_skills_section = True
            new_content.append(line)
            # Add technical skills
            new_content.append('\\begin{tabular}{ @{} >{\\bfseries}l @{\\hspace{2ex}} l }')
            new_content.append(f'Technical:&{", ".join(skills_data["technical_skills"])}\\\\')
            new_content.append('\\end{tabular}\\\\')
            new_content.append('\\vspace{-3mm}')
            new_content.append('\\begin{tabular}{ @{} >{\\bfseries}l @{\\hspace{2ex}} l }')
            new_content.append(f'Soft Skills:&{", ".join(skills_data["soft_skills"])}\\\\')
            new_content.append('\\end{tabular}\\\\')
            skills_added = True
            continue
        elif '\\begin{rSection}{PROJECTS}' in line:
            in_projects_section = True
            new_content.append(line)
            # Add projects
            for project in skills_data['projects']:
                new_content.append('\\item')
                new_content.append(f'\\textbf{{{project["title"]}: }}')
                new_content.append(f'{{{project["description"]}}}\\\\')
                new_content.append(f'\\textbf{{Tech Stack:}} {", ".join(project["tech_stack"])}')
                new_content.append('\\vspace{-1.5mm}')
            projects_added = True
            continue
        
        if in_skills_section and '\\end{rSection}' in line:
            in_skills_section = False
            new_content.append(line)
        elif in_projects_section and '\\end{rSection}' in line:
            in_projects_section = False
            new_content.append(line)
        elif not in_skills_section and not in_projects_section:
            new_content.append(line)
    
    return '\n'.join(new_content)

def render_resume_tailor():
    st.title("Resume Tailoring")
    
    # Get job details from session state
    job_title = st.session_state.get('job_title', '')
    job_description = st.session_state.get('job_description', '')
    
    if not job_title or not job_description:
        st.error("Please analyze a job description first on the previous page")
        return
    
    # Create two columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Resume Editor")
        
        # Load original resume
        resume_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resumes", "resume.tex")
        try:
            with open(resume_path, "r", encoding="utf-8") as f:
                original_content = f.read()
        except Exception as e:
            st.error(f"Error loading resume: {str(e)}")
            return
        
        # Classify skills and generate projects
        skills_data = classify_skills_and_generate_projects(job_title, job_description)
        
        # Update resume content
        new_content = update_resume_content(original_content, skills_data)
        
        # Show the LaTeX source
        edited_content = st.text_area("LaTeX Source", new_content, height=400)
        
        if st.button("Update Resume"):
            try:
                with open(resume_path, "w", encoding="utf-8") as f:
                    f.write(edited_content)
                st.success("Resume updated successfully!")
            except Exception as e:
                st.error(f"Error saving resume: {str(e)}")
    
    with col2:
        st.subheader("Preview")
        
        # Generate and display PDF preview
        pdf_base64 = render_latex_preview(edited_content)
        if pdf_base64:
            st.markdown(
                f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="100%" height="800px"></iframe>',
                unsafe_allow_html=True
            )
        
        # Display keyword matches
        if 'categorized_keywords' in st.session_state:
            high_priority = st.session_state['categorized_keywords']['high']
            low_priority = st.session_state['categorized_keywords']['low']
            
            # Calculate technical score
            technical_score = calculate_technical_skills_match_score(
                st.session_state['job_description'], edited_content)
            
            # Calculate overall match score
            matches_high = get_keyword_matches(high_priority, edited_content)
            matches_low = get_keyword_matches(low_priority, edited_content)
            
            matched_count_high = sum(1 for v in matches_high.values() if v)
            matched_count_low = sum(1 for v in matches_low.values() if v)
            total_count = len(high_priority) + len(low_priority)
            overall_score = round(((matched_count_high + matched_count_low) / total_count) * 100, 1) if total_count > 0 else 0
            
            # Display scores with progress bars
            st.subheader("Technical Skills Match")
            st.progress(technical_score / 100)
            st.write(f"{technical_score}% match on technical skills")
            
            st.subheader("Overall Match Score")
            st.progress(overall_score / 100)
            st.write(f"{overall_score}% match with the job description")
            
            # Create columns for high and low priority keywords
            col_high, col_low = st.columns(2)
            
            with col_high:
                st.subheader("High Priority Keywords")
                matched_high = []
                unmatched_high = []
                for keyword in high_priority:
                    if matches_high.get(keyword, False):
                        matched_high.append(keyword)
                    else:
                        unmatched_high.append(keyword)
                
                if matched_high:
                    st.write("✅ Found:")
                    st.write(", ".join(matched_high))
                if unmatched_high:
                    st.write("❌ Missing:")
                    st.write(", ".join(unmatched_high))
            
            with col_low:
                st.subheader("Low Priority Keywords")
                matched_low = []
                unmatched_low = []
                for keyword in low_priority:
                    if matches_low.get(keyword, False):
                        matched_low.append(keyword)
                    else:
                        unmatched_low.append(keyword)
                
                if matched_low:
                    st.write("✅ Found:")
                    st.write(", ".join(matched_low))
                if unmatched_low:
                    st.write("❌ Missing:")
                    st.write(", ".join(unmatched_low))

if __name__ == "__main__":
    render_resume_tailor()
