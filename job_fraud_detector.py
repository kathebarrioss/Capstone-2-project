import streamlit as st
import google.generativeai as genai
import os

model = genai.GenerativeModel(model_name="gemini-2.5-pro")

os.environ["GOOGLE_API_KEY"] = "AIzaSyBasrqxqM8ET9UzdRKAIdowMOXen0qDpnY"

tab1, tab2, tab3 = st.tabs(["Home", "AI Tool", "About Us"])

with tab1:
    st.header("This program will help determinate fraudulent job listings.")
with tab2:
    st.title("AI Powered Job Fraud Detector (Powered by Gemini)")

    st.subheader("Job Information")

    job_title = st.text_input("Job Title")
    company_name = st.text_input("Company Name")
    location = st.text_input("Location")
    salary = st.text_input("Salary (if listed)")
    source = st.selectbox(
        "Where did you find this listing?",
        ["Indeed", "LinkedIn", "Company Website", "Referral", "Other"]
    )

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        st.error("Please set your GOOGLE_API_KEY environment variable.")
        st.stop()

    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel("gemini-2.5-pro")

    st.header("Copy and paste the job description into AI input box below")

    inputListing = st.text_area("Paste the job listing below:", height=300)
    
    job_metadata = f"""
    Job Title: {job_title or "Not specified"}
    Company: {company_name or "Not specified"}
    Location: {location or "Not specified"}
    Salary: {salary or "Not specified"}
    Source: {source or "Not specified"}
    """

    if st.button("Analyze Listing"):
        if not inputListing.strip():
            st.warning("Please input something into the prompt.")
        else:
            with st.spinner("Analyzing with Gemini..."):
                prompt = f"""
                    You are going to analyze this job listing to determine if it is fraudulent or not.

                    Job Information:
                    {job_metadata}

                    Job Listing:
                    \"\"\"
                    {inputListing}
                    \"\"\"

                    Score the listing based on these:
                    - Verdict: Fraudulent / Legitimate / Uncertain
                    - Confidence: (0-100)
                    - Margin of error: (percentage)
                    - Conclusion and explanation: (why this verdict)
                    """


                try:
                    response = model.generate_content(prompt)
                    st.success("Analysis Complete.")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
with tab3:
    st.header("About Us")
    st.markdown("""
        Welcome to the **AI-Powered Job Fraud Detector** 👩‍💻🕵️‍♂️

        This tool was developed by a group of students as part of an academic project. Our goal is to help job seekers quickly and safely evaluate job listings using the power of AI.

        ### 🎯 What This Tool Does:
        - Analyzes job listings using Google's Gemini AI
        - Flags suspicious language, unrealistic offers, or scam indicators
        - Provides a verdict with a confidence score and explanation

        We built this platform to raise awareness about online job scams, which are becoming increasingly common — especially among students and early-career professionals.

        ### 🧠 Built By Students, For Students
        Thanks for checking it out!
        """)
