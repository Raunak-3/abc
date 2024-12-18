import streamlit as st
import os
import tempfile
import subprocess
from pathlib import Path
import base64
from utils.skill_classifier import classify_skills_and_generate_projects
from utils.local_match_utils import get_keyword_matches, calculate_technical_skills_match_score
import shutil
import re

def extract_section(tex_content, section_name):
    # Escape special characters in the section name
    section_name = re.escape(section_name)
    pattern = r'\\begin{rSection}{' + section_name + r'}.*?\\end{rSection}'
    match = re.search(pattern, tex_content, re.DOTALL)
    return match.group(0) if match else ""

def update_section(tex_content, section_name, new_content):
    """Update a specific section in the LaTeX content"""
    # Escape special characters in the section name
    section_name = re.escape(section_name)
    pattern = r'\\begin{rSection}{' + section_name + r'}.*?\\end{rSection}'
    
    # Format the new content if it doesn't already have the rSection tags
    if not new_content.strip().startswith('\\begin{rSection}'):
        new_content = f'\\begin{{rSection}}{{{section_name}}}\n{new_content}\n\\end{{rSection}}'
    
    # Escape backslashes in the new content
    new_content = new_content.replace('\\', '\\\\')
    return re.sub(pattern, new_content, tex_content, flags=re.DOTALL)

def render_latex_preview(tex_content: str) -> str:
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            
            # Copy resume.cls to temp directory
            cls_path = Path("resumes/resume.cls")
            if cls_path.exists():
                shutil.copy2(cls_path, temp_dir_path / "resume.cls")
            else:
                st.error("resume.cls not found. Please ensure it exists in the resumes directory.")
                return None
            
            # Write the LaTeX content to a temporary file
            tex_file = temp_dir_path / "resume.tex"
            tex_file.write_text(tex_content)
            
            # Run pdflatex twice to resolve references
            for _ in range(2):
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', 'resume.tex'],
                    cwd=temp_dir,
                    capture_output=True,
                    text=True
                )
            
            pdf_path = temp_dir_path / "resume.pdf"
            if pdf_path.exists():
                return base64.b64encode(pdf_path.read_bytes()).decode()
            else:
                error_msg = result.stderr if result.stderr else result.stdout
                st.error(f"LaTeX compilation failed. Error: {error_msg}")
                return None
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        return None

def render_resume_tailor():
    st.title("Resume Tailor")
    
    # Read original resume content
    resume_path = Path("resumes/resume.tex")
    if not resume_path.exists():
        st.error("resume.tex not found in resumes directory")
        return
    
    if 'edited_content' not in st.session_state:
        st.session_state['edited_content'] = resume_path.read_text()
    
    # Calculate and display match scores at the top
    if 'job_description' in st.session_state and 'categorized_keywords' in st.session_state:
        technical_score = calculate_technical_skills_match_score(
            st.session_state['job_description'], st.session_state['edited_content'])
        
        high_priority = st.session_state['categorized_keywords']['high']
        low_priority = st.session_state['categorized_keywords']['low']
        matches_high = get_keyword_matches(high_priority, st.session_state['edited_content'])
        matches_low = get_keyword_matches(low_priority, st.session_state['edited_content'])
        
        matched_count_high = sum(1 for v in matches_high.values() if v)
        matched_count_low = sum(1 for v in matches_low.values() if v)
        total_count = len(high_priority) + len(low_priority)
        overall_score = round(((matched_count_high + matched_count_low) / total_count) * 100, 1) if total_count > 0 else 0
        
        # Display scores at the top with metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Technical Skills Match", f"{technical_score}%")
        with col2:
            st.metric("Overall Match Score", f"{overall_score}%")
    
    # Create columns for the layout
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Edit Resume Sections")
        
        # Button to reset to original content
        col_reset, col_format = st.columns(2)
        with col_reset:
            if st.button("Reset to Original"):
                st.session_state['edited_content'] = resume_path.read_text()
                st.session_state['should_render'] = True
                st.rerun()
        
        with col_format:
            if st.button("Format Technical Skills"):
                # Only use skills from keywords
                all_skills = set()
                
                # Define soft skills to filter out
                soft_skills = {
                    'problem-solving', 'real-time', 'game logic', 'Technical Communication',
                    'Attention to Detail', 'Problem Analysis', 'communication', 'teamwork',
                    'leadership', 'time management', 'project management', 'analytical',
                    'problem solving', 'detail-oriented', 'organization', 'multitasking',
                    'critical thinking', 'creativity', 'adaptability', 'flexibility',
                    'collaboration', 'interpersonal', 'verbal communication',
                    'written communication', 'presentation', 'documentation'
                }
                
                # Only add skills from high and low priority keywords
                if 'categorized_keywords' in st.session_state:
                    # Filter out soft skills when adding to all_skills
                    for skill in st.session_state['categorized_keywords']['high']:
                        if skill.lower() not in {s.lower() for s in soft_skills}:
                            all_skills.add(skill)
                    for skill in st.session_state['categorized_keywords']['low']:
                        if skill.lower() not in {s.lower() for s in soft_skills}:
                            all_skills.add(skill)
                else:
                    st.error("Please analyze a job description first to get keywords")
                    return
                
                # Sort skills
                sorted_skills = sorted(list(all_skills))
                
                # Format skills into lines
                current_line = "Technical:&"
                lines = []
                line_length = 0
                
                for i, skill in enumerate(sorted_skills):
                    # Check if adding this skill would exceed 90 characters
                    if line_length + len(skill) > 90:
                        # Add \\ to all lines except the very last one
                        lines.append(current_line.rstrip(', ') + '\\\\')
                        current_line = "&"
                        line_length = 1  # Account for &
                    
                    current_line += skill + ", "
                    line_length = len(current_line)
                
                # Add the last line without trailing comma
                if current_line != "&":
                    lines.append(current_line.rstrip(', '))
                
                # Create the new skills section with \\ at the end of each line except the last
                new_skills = ""
                for i, line in enumerate(lines):
                    if i < len(lines) - 1:  # All lines except the last
                        new_skills += line + '\\\\' + '\n'
                    else:  # Last line
                        new_skills += line
                
                # Update only the Technical: line, preserving everything else
                pattern = r'(Technical:)([^}]*?)(?=\\end{tabular})'
                new_content = re.sub(pattern, new_skills, st.session_state['edited_content'], flags=re.DOTALL)
                
                # Save changes
                resume_path.write_text(new_content)
                st.session_state['edited_content'] = new_content
                st.session_state['should_render'] = True
                st.success("Technical skills formatted successfully!")
                st.rerun()
        
        # Create a form for editing
        with st.form("resume_edit_form"):
            # Extract current sections for editing
            current_content = st.session_state['edited_content']
            skills_section = extract_section(current_content, "SKILLS")
            projects_section = extract_section(current_content, "PROJECTS")
            
            # Remove the rSection tags for editing
            skills_content = skills_section.replace('\\begin{rSection}{SKILLS}\n', '').replace('\n\\end{rSection}', '')
            projects_content = projects_section.replace('\\begin{rSection}{PROJECTS}\n', '').replace('\n\\end{rSection}', '')
            
            # Edit Skills section
            st.subheader("Skills Section")
            edited_skills = st.text_area("Edit Skills", skills_content, height=200)
            
            # Edit Projects section
            st.subheader("Projects Section")
            edited_projects = st.text_area("Edit Projects", projects_content, height=300)
            
            # Form submit button
            if st.form_submit_button("Update Resume"):
                try:
                    # Update each section
                    new_content = current_content
                    new_content = update_section(new_content, "SKILLS", edited_skills)
                    new_content = update_section(new_content, "PROJECTS", edited_projects)
                    
                    # Save the changes
                    resume_path.write_text(new_content)
                    st.session_state['edited_content'] = new_content
                    st.session_state['should_render'] = True
                    st.success("Resume updated successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error updating resume: {str(e)}")
    
    with col2:
        st.subheader("PDF Preview")
        # Only render PDF when should_render is True
        if 'should_render' not in st.session_state:
            st.session_state['should_render'] = True
            
        if st.session_state['should_render']:
            pdf_base64 = render_latex_preview(st.session_state['edited_content'])
            if pdf_base64:
                pdf_display = f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="100%" height="800" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
            st.session_state['should_render'] = False
        
        # Display keyword matches
        if 'categorized_keywords' in st.session_state:
            # Create columns for high and low priority keywords
            col_high, col_low = st.columns(2)
            
            with col_high:
                st.subheader("High Priority Keywords")
                high_priority = st.session_state['categorized_keywords']['high']
                matches_high = get_keyword_matches(high_priority, st.session_state['edited_content'])
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
                low_priority = st.session_state['categorized_keywords']['low']
                matches_low = get_keyword_matches(low_priority, st.session_state['edited_content'])
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
