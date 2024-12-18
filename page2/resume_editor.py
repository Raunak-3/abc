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
        st.image("assets/logo.png", width=150)  # Replace with your logo
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
            st.text_area("Technical Skills", key="tech_skills", height=100)
            st.text_area("Soft Skills", key="soft_skills", height=100)

    with col_preview:
        st.markdown("### Preview")
        # Create LaTeX content based on form inputs
        latex_content = generate_latex()
        
        # Save LaTeX content to a temporary file
        with tempfile.NamedTemporaryFile(suffix='.tex', delete=False, mode='w') as f:
            f.write(latex_content)
            tex_path = f.name

        # Compile LaTeX to PDF
        pdf_path = compile_latex(tex_path)
        
        if pdf_path:
            # Display PDF preview (you'll need to implement PDF display)
            st.markdown(f"PDF generated successfully at {pdf_path}")
            
            # Add download button
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="Download Resume",
                    data=pdf_file,
                    file_name="resume.pdf",
                    mime="application/pdf"
                )

def generate_latex():
    # Generate LaTeX content based on form inputs
    latex_content = r"""
    \documentclass[11pt,a4paper]{article}
    \usepackage[utf8]{inputenc}
    \usepackage[margin=1in]{geometry}
    \usepackage{hyperref}
    \begin{document}
    
    % Header
    \begin{center}
        \huge\textbf{""" + st.session_state.get('name', '') + r"""}\\[0.3cm]
        \normalsize
        """ + st.session_state.get('email', '') + r" | " + st.session_state.get('phone', '') + r" | " + st.session_state.get('location', '') + r"""\\
        """ + st.session_state.get('linkedin', '') + r" | " + st.session_state.get('github', '') + r"""
    \end{center}
    
    % Rest of the resume content...
    \end{document}
    """
    return latex_content

def compile_latex(tex_path):
    try:
        # Ensure the output directory exists
        output_dir = os.path.dirname(tex_path)
        
        # Run pdflatex
        subprocess.run([
            'pdflatex',
            '-interaction=nonstopmode',
            f'-output-directory={output_dir}',
            tex_path
        ], check=True)
        
        # Return the path to the generated PDF
        return tex_path.replace('.tex', '.pdf')
    except subprocess.CalledProcessError as e:
        st.error(f"Error compiling LaTeX: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

if __name__ == "__main__":
    render_resume_editor()
