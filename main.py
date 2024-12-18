import streamlit as st
st.set_page_config(layout="wide")
from utils import resume_utils, ui_utils, local_match_utils, resume_generator
import PyPDF2
import io
import os
import re

# Initialize session state for persistence
if 'initialized' not in st.session_state:
    st.session_state['initialized'] = True
    st.session_state['resume_data'] = {}
    st.session_state['resume_text'] = None
    st.session_state['pdf_uploaded'] = False
    st.session_state['resume_path'] = None
    st.session_state['categorized_keywords'] = None
    st.session_state['job_description'] = None
    st.session_state['job_title'] = None
    st.session_state['analysis_complete'] = False
    st.session_state['high_priority'] = []
    st.session_state['low_priority'] = []
    st.session_state['technical_score'] = 0
    st.session_state['overall_score'] = 0

def clear_analysis():
    """Clear all analysis related session state"""
    st.session_state['categorized_keywords'] = None
    st.session_state['job_description'] = None
    st.session_state['job_title'] = None
    st.session_state['analysis_complete'] = False
    st.session_state['high_priority'] = []
    st.session_state['low_priority'] = []
    st.session_state['technical_score'] = 0
    st.session_state['overall_score'] = 0

# Page Header
col_title, col_clear = st.columns([5,1])
with col_title:
    st.title("Resume Tailoring Application")
with col_clear:
    if st.session_state.get('analysis_complete'):
        if st.button("Clear Analysis"):
            clear_analysis()

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
        job_title = st.text_input("Job Title", value=st.session_state.get('job_title', ''))
        job_description = st.text_area("Job Description", value=st.session_state.get('job_description', ''))

        if st.button("Analyze Resume") or st.session_state.get('analysis_complete'):
            if job_description and job_title:
                # Update session state
                st.session_state['job_title'] = job_title
                st.session_state['job_description'] = job_description
                
                # Only run analysis if not already complete
                if not st.session_state.get('analysis_complete'):
                    with st.spinner("Analyzing your resume..."):
                        # Process with local matching using Gemini model
                        high_priority, low_priority = local_match_utils.categorize_keywords(job_description)
                        
                        # Store in session state
                        st.session_state['categorized_keywords'] = {"high": high_priority, "low": low_priority}
                        st.session_state['high_priority'] = high_priority
                        st.session_state['low_priority'] = low_priority
                        
                        # Calculate scores
                        technical_score = local_match_utils.calculate_technical_skills_match_score(
                            job_description, st.session_state['resume_text'])
                        st.session_state['technical_score'] = technical_score
                        
                        # Count matched keywords
                        matched_count_high = sum(1 for k in high_priority if local_match_utils.get_keyword_matches([k], st.session_state['resume_text']).get(k, False))
                        matched_count_low = sum(1 for k in low_priority if local_match_utils.get_keyword_matches([k], st.session_state['resume_text']).get(k, False))
                        total_count = len(high_priority) + len(low_priority)
                        overall_score = round(((matched_count_high + matched_count_low) / total_count) * 100, 1) if total_count > 0 else 0
                        st.session_state['overall_score'] = overall_score
                        st.session_state['analysis_complete'] = True
                
                # Display results from session state
                st.subheader("Technical Skills Match")
                st.progress(st.session_state['technical_score'] / 100)
                st.write(f"{st.session_state['technical_score']}% match on technical skills")
                
                st.subheader("Overall Match Score")
                st.progress(st.session_state['overall_score'] / 100)
                st.write(f"{st.session_state['overall_score']}% match with the job description")
                
                # Create columns for keyword display
                col_high, col_low = st.columns(2)
                
                with col_high:
                    st.subheader("High Priority Keywords")
                    matched_high = []
                    unmatched_high = []
                    for keyword in st.session_state['high_priority']:
                        if local_match_utils.get_keyword_matches([keyword], st.session_state['resume_text']).get(keyword, False):
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
                    for keyword in st.session_state['low_priority']:
                        if local_match_utils.get_keyword_matches([keyword], st.session_state['resume_text']).get(keyword, False):
                            matched_low.append(keyword)
                        else:
                            unmatched_low.append(keyword)
                    
                    if matched_low:
                        st.write("✅ Found:")
                        st.write(", ".join(matched_low))
                    if unmatched_low:
                        st.write("❌ Missing:")
                        st.write(", ".join(unmatched_low))
            else:
                st.warning("Please enter both job description and job title to analyze.")
    else:
        st.info("Please upload your resume or select an existing one to begin the analysis.")
