import streamlit as st
import os
import tempfile
import subprocess
from pathlib import Path

def render_resume_editor():
    st.set_page_config(layout="wide")
    
    # Header with logo and match stats
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Resume Editor")
    with col2:
        if 'matched_keywords' in st.session_state and 'total_keywords' in st.session_state:
            st.metric(
                f"{st.session_state.matched_keywords} of {st.session_state.total_keywords} keywords",
                f"{st.session_state.match_percentage}%",
                "resume match"
            )

    # Main content area with editor and preview
    col_editor, col_preview = st.columns([1, 1])

    with col_editor:
        # Tabs for different sections
        tabs = st.tabs(["Resume Header", "Professional Summary", "Experience", "Education", "Skills"])
        
        with tabs[0]:
            st.text_input("Name", key="name", value=st.session_state.get('name', ''))
            st.text_input("Email", key="email", value=st.session_state.get('email', ''))
            st.text_input("Phone", key="phone", value=st.session_state.get('phone', ''))
            st.text_input("Location", key="location", value=st.session_state.get('location', ''))
            st.text_input("LinkedIn", key="linkedin", value=st.session_state.get('linkedin', ''))
            st.text_input("GitHub", key="github", value=st.session_state.get('github', ''))
            st.text_input("Portfolio", key="portfolio", value=st.session_state.get('portfolio', ''))

        with tabs[1]:
            st.text_area("Professional Summary", key="summary", height=200)

        with tabs[2]:
            st.text_area("Experience", key="experience", height=400)

        with tabs[3]:
            st.text_input("University", key="university")
            st.text_input("Degree", key="degree")
            st.text_input("Major", key="major")
            st.text_input("Graduation Date", key="grad_date")
            st.text_input("GPA", key="gpa")

        with tabs[4]:
            st.text_area("Technical Skills", key="technical_skills", height=100)
            st.text_area("Soft Skills", key="soft_skills", height=100)

    with col_preview:
        st.subheader("Resume Preview")
        if st.button("Generate Resume"):
            try:
                latex_content = generate_latex()
                pdf_path = compile_latex(latex_content)
                if pdf_path:
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            "Download Resume",
                            f,
                            file_name="resume.pdf",
                            mime="application/pdf"
                        )
                    st.success("Resume generated successfully!")
            except Exception as e:
                st.error(f"Error generating resume: {str(e)}")

def generate_latex():
    # Generate LaTeX content from form inputs
    latex_template = """\\documentclass{resume}
\\usepackage[left=0.4 in,top=0.3in,right=0.4 in,bottom=0.3in]{geometry}
\\name{%s}
\\address{%s \\quad \\textbf{%s} \\quad \\href{mailto:%s}{%s}}

\\begin{document}

\\begin{rSection}{Education}
%s
\\end{rSection}

\\begin{rSection}{Skills}
\\begin{tabular}{ @{} >{\\bfseries}l @{\\hspace{2ex}} l }
Technical:&%s\\\\
Soft Skills:&%s\\\\
\\end{tabular}\\\\
\\end{rSection}

\\begin{rSection}{Experience}
%s
\\end{rSection}

\\end{document}
"""
    return latex_template % (
        st.session_state.get('name', ''),
        st.session_state.get('location', ''),
        st.session_state.get('phone', ''),
        st.session_state.get('email', ''),
        st.session_state.get('email', ''),
        st.session_state.get('education', ''),
        st.session_state.get('technical_skills', ''),
        st.session_state.get('soft_skills', ''),
        st.session_state.get('experience', '')
    )

def compile_latex(latex_content):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Write tex content to temporary file
            tex_path = os.path.join(temp_dir, "resume.tex")
            with open(tex_path, "w", encoding="utf-8") as f:
                f.write(latex_content)
            
            # Copy resume.cls to temp directory
            cls_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resumes", "resume.cls")
            if os.path.exists(cls_path):
                subprocess.run(["copy", cls_path, temp_dir], shell=True, check=True)
            
            # Compile LaTeX
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", tex_path],
                cwd=temp_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                raise Exception(f"LaTeX compilation failed: {result.stderr}")
            
            pdf_path = os.path.join(temp_dir, "resume.pdf")
            if os.path.exists(pdf_path):
                return pdf_path
            else:
                raise Exception("PDF file not generated")
    except Exception as e:
        raise Exception(f"Error compiling LaTeX: {str(e)}")

if __name__ == "__main__":
    render_resume_editor()
