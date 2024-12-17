import streamlit as st
from typing import List, Dict

def display_keywords(keywords: List[str]) -> None:
    """
    Displays keywords in the UI.
    """
    st.subheader("Keywords")
    st.write(", ".join(keywords))

def display_match_score(score: int) -> None:
    """
    Displays the resume match score in the UI.
    """
    st.subheader("Match Score")
    st.write(f"{score}%")

def display_resume_preview(resume_latex: str) -> None:
    """
    Displays a preview of the resume in PDF format.
    """
    st.subheader("Resume Preview")
    st.write("PDF Preview Placeholder")

def get_editable_resume_layout(resume_data: Dict) -> None:
    """
    Returns the layout for an editable resume.
    """
    st.subheader("Editable Resume")
    for section, content in resume_data.items():
        st.subheader(section)
        st.text_area(f"Edit {section}", value=str(content), key=section)

def get_side_by_side_layout(left_content, right_content):
    """
    Returns a side-by-side layout for comparison.
    """
    col1, col2 = st.columns(2)
    with col1:
        st.write(left_content)
    with col2:
        st.write(right_content)
