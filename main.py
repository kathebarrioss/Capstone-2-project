import streamlit as st
import google.generativeai as genai
import os

model = genai.GenerativeModel(model_name="gemini-2.5-pro")

os.environ["GOOGLE_API_KEY"] = "AIzaSyCDI91--v7boVCzsDGHhOX03vhe6oNW3Bs"

tab1, tab2, tab3 = st.tabs(["Home", "AI Tool", "Questionnaire"])

with tab1:
    st.header("This program will help determinate fraudulent job listings.")
with tab2:
    st.header("copy and paste the job description into AI input box below")

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        st.error("Please set your GOOGLE_API_KEY environment variable.")
        st.stop()

    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel("gemini-2.5-pro")

    st.title("AI Powered Job Fraud Detector (Powered by Gemini)")

    inputListing = st.text_area("Paste the job listing below:", height=300)

    if st.button("Analyze Listing"):
        if not inputListing.strip():
            st.warning("Please input something into the prompt.")
        else:
            with st.spinner("Analyzing with Gemini..."):
                prompt = f"""
    You are going to analyze this job listing if it is fraudulent or not.
    Provide a brief summary, then go into detail as to what's wrong with the listing.

    Job Listing:
    \"\"\"
    {inputListing}
    \"\"\"

    Score the listing based on these scores:
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
    st.header("This questionnaire will help determine if a job listing is a scam or not")
