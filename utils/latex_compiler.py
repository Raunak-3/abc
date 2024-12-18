import os
import subprocess
import tempfile
import streamlit as st
from pathlib import Path

def compile_latex_to_pdf(tex_content, output_dir=None):
    """
    Compiles LaTeX content to PDF and returns the path to the generated PDF file.
    
    Args:
        tex_content (str): The LaTeX content to compile
        output_dir (str, optional): Directory to save the output files. Defaults to a temp directory.
        
    Returns:
        str: Path to the generated PDF file, or None if compilation failed
    """
    try:
        # Create a temporary directory if output_dir is not specified
        if output_dir is None:
            temp_dir = tempfile.mkdtemp()
            output_dir = temp_dir
        else:
            temp_dir = None
            os.makedirs(output_dir, exist_ok=True)

        # Create a temporary .tex file
        tex_file = os.path.join(output_dir, "resume.tex")
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(tex_content)

        # Run pdflatex twice to ensure all references are resolved
        for _ in range(2):
            process = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', '-output-directory=' + output_dir, tex_file],
                capture_output=True,
                text=True
            )
            
            if process.returncode != 0:
                st.error(f"LaTeX compilation error: {process.stderr}")
                return None

        # Path to the generated PDF
        pdf_path = os.path.join(output_dir, "resume.pdf")
        
        if os.path.exists(pdf_path):
            return pdf_path
        else:
            st.error("PDF file was not generated")
            return None

    except Exception as e:
        st.error(f"Error compiling LaTeX: {str(e)}")
        return None

def update_latex_content(template_path, replacements):
    """
    Updates the LaTeX template with new content.
    
    Args:
        template_path (str): Path to the LaTeX template file
        replacements (dict): Dictionary of replacements to make
        
    Returns:
        str: Updated LaTeX content
    """
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Make replacements
        for key, value in replacements.items():
            placeholder = f"{{{{ {key} }}}}"
            content = content.replace(placeholder, value)
            
        return content
    except Exception as e:
        st.error(f"Error updating LaTeX content: {str(e)}")
        return None
