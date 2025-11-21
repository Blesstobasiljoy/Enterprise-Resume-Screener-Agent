import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AutoHR | AI Recruitment Agent",
    page_icon="👔",
    layout="wide"
)

# --- SIDEBAR (Configuration) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=100)
    st.title("AutoHR Agent")
    st.markdown("---")
    
    # Secure API Key Input
    api_key = st.text_input("Enter Gemini API Key", type="password")
    
    st.markdown("### How it works")
    st.info(
        "1. Upload a Resume (PDF)\n"
        "2. Paste the Job Description\n"
        "3. The Agent analyzes the fit\n"
        "4. The Agent drafts the email"
    )
    st.markdown("---")
    st.caption("Built for Kaggle Agents Capstone")

# --- CUSTOM FUNCTIONS (Tools) ---

def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from a Streamlit uploaded file object.
    """
    try:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def analyze_candidate(model, resume_text, job_desc):
    """
    Agent 1: Evaluator - Scores the candidate.
    """
    prompt = f"""
    Act as a Senior HR Manager.
    
    JOB DESCRIPTION:
    {job_desc}
    
    CANDIDATE RESUME:
    {resume_text}
    
    Task:
    1. Assign a match score (0-100).
    2. Provide a 1-sentence reasoning.
    
    Output strictly in this format:
    SCORE: [number]
    REASONING: [text]
    """
    response = model.generate_content(prompt)
    return response.text

def draft_email(model, evaluation, candidate_name):
    """
    Agent 2: Communicator - Writes the email based on the score.
    """
    prompt = f"""
    You are an HR Assistant. Based on this evaluation:
    {evaluation}
    
    Rules:
    - If SCORE > 60: Write an invite to interview.
    - If SCORE < 60: Write a polite rejection.
    - Use the name "{candidate_name}".
    
    Output ONLY the email body.
    """
    response = model.generate_content(prompt)
    return response.text

# --- MAIN UI ---

st.header("🚀 Enterprise Resume Screener Agent")
st.markdown("Automate your first-round recruitment process using **Sequential AI Agents**.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Job Details")
    job_description = st.text_area(
        "Paste Job Description", 
        height=200, 
        placeholder="e.g. Senior Python Developer with 5 years experience..."
    )

with col2:
    st.subheader("2. Candidate Resume")
    uploaded_file = st.file_uploader("Upload PDF Resume", type="pdf")
    candidate_name = st.text_input("Candidate Name", placeholder="e.g. John Doe")

# --- EXECUTION LOGIC ---

if st.button("Run Agent Workflow", type="primary"):
    if not api_key:
        st.warning("Please enter your Google API Key in the sidebar.")
        st.stop()
        
    if not uploaded_file or not job_description or not candidate_name:
        st.warning("Please fill in all fields.")
        st.stop()

    # Configure Gemini
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash') # Using the latest fast model
    except Exception as e:
        st.error(f"API Key Error: {e}")
        st.stop()

    with st.status("🤖 Agents are working...", expanded=True) as status:
        
        # Step 1: Tool Use
        st.write("📂 Extractor Agent: Parsing PDF...")
        resume_text = extract_text_from_pdf(uploaded_file)
        
        if resume_text:
            # Step 2: Evaluation
            st.write("🧠 Evaluator Agent: Analyzing match...")
            evaluation = analyze_candidate(model, resume_text, job_description)
            
            # Extract score for visual display (simple string parsing)
            try:
                score_part = evaluation.split("SCORE:")[1].split("\n")[0].strip()
                score_int = int(score_part)
            except:
                score_int = 0 # Fallback
            
            # Step 3: Drafting
            st.write("✍️ Communicator Agent: Drafting email...")
            email_draft = draft_email(model, evaluation, candidate_name)
            
            status.update(label="✅ Workflow Complete!", state="complete", expanded=False)

            # --- RESULTS DISPLAY ---
            st.divider()
            
            res_col1, res_col2 = st.columns([1, 2])
            
            with res_col1:
                st.subheader("Analysis")
                # Dynamic Color based on score
                if score_int >= 60:
                    st.success(f"**Match Score: {score_int}/100**")
                else:
                    st.error(f"**Match Score: {score_int}/100**")
                
                st.info(f"**Reasoning:**\n\n{evaluation}")

            with res_col2:
                st.subheader("Generated Action")
                st.markdown("### Drafted Email")
                st.code(email_draft, language="markdown")
                
                st.button("📋 Copy to Clipboard") # Visual placeholder