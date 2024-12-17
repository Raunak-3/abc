import streamlit as st
from utils import gemini_utils, resume_utils, ui_utils

st.title("Resume Tailoring Application")

# Initialize session state
if 'resume_data' not in st.session_state:
    st.session_state['resume_data'] = {}
if 'selected_resume' not in st.session_state:
    st.session_state['selected_resume'] = None

# Input fields
job_description = st.text_area("Enter Job Description")
job_title = st.text_input("Enter Job Title")

# Load existing resumes
available_resumes = resume_utils.list_resumes()
if available_resumes:
    selected_resume = st.selectbox("Select a base resume", available_resumes)
    if selected_resume:
        st.session_state['selected_resume'] = selected_resume
        st.session_state['resume_data'] = resume_utils.load_resume(f"resumes/{selected_resume}")

if st.button("Process"):
    if job_description:
        # Process with Gemini
        keywords = gemini_utils.extract_keywords(job_description)
        categorized_keywords = gemini_utils.categorize_keywords(keywords)
        match_score = gemini_utils.get_resume_match_score(job_description, str(st.session_state['resume_data']))

        # Display results
        ui_utils.display_keywords(keywords)
        ui_utils.display_match_score(match_score)

        if st.session_state['resume_data']:
            # Display editable resume
            ui_utils.get_editable_resume_layout(st.session_state['resume_data'])

            # Generate tailored sections
            if st.button("Generate Tailored Sections"):
                for section in st.session_state['resume_data'].keys():
                    instructions = f"Tailor this section to the job description: {job_description}"
                    tailored_section = gemini_utils.generate_tailored_resume_section(job_description, str(st.session_state['resume_data'][section]), instructions)
                    st.session_state['resume_data'] = resume_utils.integrate_tailored_section(st.session_state['resume_data'], section, tailored_section)
                ui_utils.get_editable_resume_layout(st.session_state['resume_data'])

            # Format and display resume preview
            latex_resume = resume_utils.format_resume_latex(st.session_state['resume_data'])
            ui_utils.display_resume_preview(latex_resume)

            # Save resume
            if st.button("Save Resume"):
                resume_utils.save_resume(st.session_state['resume_data'], f"{job_title}_tailored_resume")
                st.success("Resume saved successfully!")
    else:
        st.warning("Please enter a job description.")
