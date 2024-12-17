import streamlit as st
from utils import resume_utils, ui_utils, local_match_utils
import PyPDF2
import io
import os
import re

st.set_page_config(layout="wide")
st.title("Resume Tailoring Application")

# Initialize session state
if 'resume_data' not in st.session_state:
    st.session_state['resume_data'] = {}
if 'resume_text' not in st.session_state:
    st.session_state['resume_text'] = None
if 'pdf_uploaded' not in st.session_state:
    st.session_state['pdf_uploaded'] = False
if 'resume_path' not in st.session_state:
    st.session_state['resume_path'] = None

# Load existing resumes
existing_resumes = resume_utils.list_resumes()

# Create two columns for the layout
col1, col2 = st.columns([1, 2])

with col1:
    # Option to select existing resume
    selected_resume = st.selectbox("Select Existing Resume", [""] + existing_resumes)

    if selected_resume:
        resume_path = os.path.join(resume_utils.RESUME_DIR, selected_resume)
        st.session_state['resume_path'] = resume_path
        st.session_state['resume_text'] = resume_utils.load_resume(resume_path).get('text', '')
        st.session_state['pdf_uploaded'] = True
        st.success(f"Resume '{selected_resume}' loaded successfully!")
    else:
        # File uploader for PDF resume
        uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=['pdf'])

        if uploaded_file is not None and not st.session_state['pdf_uploaded']:
            try:
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
                resume_text = ""
                for page in pdf_reader.pages:
                    resume_text += page.extract_text()
                
                # Save uploaded resume
                resume_name = uploaded_file.name.replace(".pdf", "")
                resume_path = resume_utils.save_uploaded_resume(uploaded_file, resume_name, resume_text)
                st.session_state['resume_path'] = resume_path
                st.session_state['resume_text'] = resume_text
                st.session_state['pdf_uploaded'] = True
                st.success("Resume uploaded successfully!")
            except Exception as e:
                st.error(f"Error reading PDF: {str(e)}")

with col2:
    # Only show the rest of the interface if PDF is uploaded
    if st.session_state['pdf_uploaded']:
        # Job details input
        job_title = st.text_input("Job Title")
        job_description = st.text_area("Job Description")

        if st.button("Analyze Resume"):
            if job_description and job_title:
                with st.spinner("Analyzing your resume..."):
                    # Process with local matching
                    keywords = local_match_utils.extract_keywords_from_text(job_description)
                    categorized_keywords = local_match_utils.categorize_keywords(keywords)
                    keyword_matches = local_match_utils.get_keyword_matches(keywords, st.session_state['resume_text'])
                    
                    # Calculate scores
                    overall_score = local_match_utils.calculate_keyword_match_score(
                        job_description, st.session_state['resume_text'], keywords)
                    technical_score = local_match_utils.calculate_technical_skills_match_score(
                        job_description, st.session_state['resume_text'])
                    
                    # Display overall match score with a progress bar
                    st.subheader("Overall Match Score")
                    st.progress(overall_score / 100)
                    st.write(f"{overall_score}% match with the job description")
                    
                    # Display technical skills score
                    st.subheader("Technical Skills Match")
                    st.progress(technical_score / 100)
                    st.write(f"{technical_score}% match on technical skills")
                    
                    # Count matched keywords
                    matched_count = sum(1 for v in keyword_matches.values() if v)
                    total_count = len(keyword_matches)
                    
                    # Display keyword match summary
                    st.subheader("Keyword Match Analysis")
                    status = "Excellent" if overall_score >= 70 else "Needs Work"
                    st.write(f"Status: {status}")
                    st.write(f"Your resume matches {matched_count} out of {total_count} keywords from the job description.")
                    
                    # Create two columns for high and low priority keywords
                    col_high, col_low = st.columns(2)
                    
                    with col_high:
                        st.subheader("High Priority Keywords")
                        for i, keyword in enumerate(categorized_keywords["high"]):
                            matched = keyword_matches.get(keyword, False)
                            st.checkbox(
                                keyword, 
                                value=matched,
                                key=f"high_{i}_{keyword}",
                                disabled=True
                            )
                    
                    with col_low:
                        st.subheader("Low Priority Keywords")
                        for i, keyword in enumerate(categorized_keywords["low"]):
                            matched = keyword_matches.get(keyword, False)
                            st.checkbox(
                                keyword,
                                value=matched,
                                key=f"low_{i}_{keyword}",
                                disabled=True
                            )
                    
                    if overall_score < 70:
                        st.warning("Try to get your score above 70% to increase your chances!")
                        st.write("Tips to improve your score:")
                        st.write("1. Add missing keywords naturally in your resume")
                        st.write("2. Focus on adding technical skills that are missing")
                        st.write("3. Use similar terminology as the job description")
            else:
                st.warning("Please enter both job description and job title to analyze.")
    else:
        st.info("Please upload your resume or select an existing one to begin the analysis.")
