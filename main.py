import streamlit as st
import google.generativeai as genai
import os

model = genai.GenerativeModel(model_name="gemini-2.5-pro")

os.environ["GOOGLE_API_KEY"] = "AIzaSyBVcbH2b0j7BEmVkv26Z2HQx-kXOHKdROQ"

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
    
    Score the listing based on these scores:
    - Verdict: Fraudulent / Legitimate / Uncertain
    - Confidence: (0-100)
    - Margin of error: (percentage)
    - Conclusion and explanation: (why this verdict)
    
    Order the output by scores first, then short summary, and lastly detailed summary.

    Job Listing:
    \"\"\"
    {inputListing}
    \"\"\"
    """
                try:
                    response = model.generate_content(prompt)
                    st.success("Analysis Complete.")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
with tab3:
    st.header("This questionnaire will help determine if a job listing is a scam or not")

    questions = {
        "q1": st.radio("Did the job offer come unsolicited or you didn't apply for it?", ('No', 'Yes')),
        "q2": st.radio("Does the job listing or recruiter use a generic email such as yahoo or gmail?", ('No', 'Yes')),
        "q3": st.radio("Does the company avoid giving you a physical address or phone number?", ('No', 'Yes')),
        "q4": st.radio("Is the job description vague or full of spelling or grammar errors?", ('No', 'Yes')),
        "q5": st.radio("Does the job promise very high pay for little or no experience?", ('No', 'Yes')),
        "q6": st.radio("Is the company unwilling to do a video or an in-person interview?", ('No', 'Yes')),
        "q7": st.radio("Does the job ask you to pay upfront for training or equipment?", ('No', 'Yes')),
        "q8": st.radio("Are you asked to provide your bank account information or Social Security number early in the application process?", ('No', 'Yes')),
        "q9": st.radio("Do they want you to cash in a check and send money to another place?", ('No', 'Yes')),
        "q10": st.radio("Is the company name or branding hard to find online or doesn't have a website?", ('No', 'Yes')),
        "q11": st.radio("Does the company avoid giving details about who the boss or coworkers will be?", ('No', 'Yes')),
        "q12": st.radio("Are they pressuring you into making a decision urgently?", ('No', 'Yes'))
    }

    st.header("Conclusions")

    if questions["q1"] == 'Yes':
        st.write("A company will usually almost never directly message you for a job. This tactic is commonly used by scammers to look for victims.")
    if questions["q2"] == 'Yes':
        st.write("Legitimate companies will use an email from their own website, such as manager@legitcompany.com")
    if questions["q3"] == 'Yes':
        st.write("Legitimate companies won't ever hesitate to give you an address or phone number.")
    if questions["q4"] == 'Yes':
        st.write("Scammers who don't speak English will have poor English skills.")
    if questions["q5"] == 'Yes':
        st.write("If it's too good to be true, it's because it is. McDonald's isn't going to pay you six figures.")
    if questions["q6"] == 'Yes':
        st.write("Scammers avoid showing their faces since they are technically criminals.")
    if questions["q7"] == 'Yes':
        st.write("A real job will give you proper equipment free of charge.")
    if questions["q8"] == 'Yes':
        st.write("Scammers will take sensitive information such as that and use that for identity theft.")
    if questions["q9"] == 'Yes':
        st.write("This is potentially a trick to launder money for the scammers.")
    if questions["q10"] == 'Yes':
        st.write("All legit businesses will have some sort of online presence")
    if questions["q11"] == 'Yes':
        st.write("This could suggest that the company doesn't exist if there is no boss or employees.")
    if questions["q12"] == 'Yes':
        st.write("Scammers will try and pressure you into doing something now so they can make fast money.")
