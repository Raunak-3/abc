import streamlit as st
import google.generativeai as genai
from typing import Dict, List, Tuple
import os
from pathlib import Path

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

def classify_skills(keywords: List[str]) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    """
    Classify keywords into technical and soft skills using Gemini API
    Returns two dictionaries: high priority and low priority, each containing technical and soft skills
    """
    prompt = f"""
    Classify the following keywords into technical skills and soft skills. 
    For each category, also indicate if they are high priority (essential/core skills) or low priority (nice-to-have skills).
    Keywords: {', '.join(keywords)}
    
    Please format your response exactly as follows:
    HIGH PRIORITY:
    Technical Skills:
    - [list technical skills]
    Soft Skills:
    - [list soft skills]
    
    LOW PRIORITY:
    Technical Skills:
    - [list technical skills]
    Soft Skills:
    - [list soft skills]
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text
        
        # Parse the response
        high_priority = {"technical": [], "soft": []}
        low_priority = {"technical": [], "soft": []}
        
        current_section = None
        current_category = None
        
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if "HIGH PRIORITY:" in line:
                current_section = "high"
            elif "LOW PRIORITY:" in line:
                current_section = "low"
            elif "Technical Skills:" in line:
                current_category = "technical"
            elif "Soft Skills:" in line:
                current_category = "soft"
            elif line.startswith('-') and current_section and current_category:
                skill = line.replace('-', '').strip()
                if current_section == "high":
                    high_priority[current_category].append(skill)
                else:
                    low_priority[current_category].append(skill)
        
        return high_priority, low_priority
        
    except Exception as e:
        st.error(f"Error classifying skills: {str(e)}")
        return {"technical": [], "soft": []}, {"technical": [], "soft": []}

def render_skill_classification():
    st.title("Skill Classification")
    
    if 'categorized_keywords' not in st.session_state:
        st.warning("Please analyze a job description first to get keywords")
        return
        
    # Get all keywords
    high_priority = st.session_state['categorized_keywords']['high']
    low_priority = st.session_state['categorized_keywords']['low']
    all_keywords = high_priority + low_priority
    
    # Classify skills
    high_priority_skills, low_priority_skills = classify_skills(all_keywords)
    
    # Display classifications
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("High Priority Skills")
        
        st.write("Technical Skills")
        for skill in high_priority_skills['technical']:
            st.markdown(f"✓ {skill}")
            
        st.write("Soft Skills")
        for skill in high_priority_skills['soft']:
            st.markdown(f"✓ {skill}")
    
    with col2:
        st.subheader("Low Priority Skills")
        
        st.write("Technical Skills")
        for skill in low_priority_skills['technical']:
            st.markdown(f"○ {skill}")
            
        st.write("Soft Skills")
        for skill in low_priority_skills['soft']:
            st.markdown(f"○ {skill}")
    
    # Display original keyword matches below
    st.markdown("---")
    st.subheader("Original Keyword Matches")
    
    col3, col4 = st.columns(2)
    with col3:
        st.write("High Priority Keywords")
        for keyword in high_priority:
            st.markdown(f"• {keyword}")
            
    with col4:
        st.write("Low Priority Keywords")
        for keyword in low_priority:
            st.markdown(f"• {keyword}")

if __name__ == "__main__":
    render_skill_classification()
