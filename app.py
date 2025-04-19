import streamlit as st
import openai
import pdfplumber
from io import BytesIO
import os
openai.api_key = os.getenv("OPENAI_API_KEY")


# --- Set your OpenAI API key here ---


# --- Streamlit App ---
st.set_page_config(page_title="Resume Roast 🔥", page_icon="🔥")
st.title("Resume Roast 🔥")
st.subheader("Upload your resume and get roasted by AI. ")
st.subheader("Brutally honest, hilariously savage.")

uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])



if uploaded_file is not None:
    with pdfplumber.open(BytesIO(uploaded_file.read())) as pdf:
        resume_text = "\n".join([page.extract_text() or "" for page in pdf.pages])
        tone = st.radio("Choose your roast style:", ["Brutal & Funny", "Constructive & Honest", "Sarcastic & Light"])


    with st.spinner("Cooking your roast..."):
        roast_prompt = f"""Use a '{tone}' tone.
        You're a savage career coach with the wit of a stand-up comedian and the knowledge of a recruiter who's seen 10,000 bad resumes.

        Your job is to:
        1. Roast the clichés, buzzwords, and inconsistencies.
        2. Highlight where the resume is boring, weak, or trying too hard.
        3. Suggest brutally honest improvements.
        4. Add a final punchline summary titled: \"Verdict:\"

        Use humor, be cheeky, but also helpful. Use natural human language and don't sound computerish.

        Resume:
        {resume_text}
        """


        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a brutally honest, witty resume critic."},
                    {"role": "user", "content": roast_prompt}
                ]
            )
            roast_output = response.choices[0].message.content
            st.success("Here's your roast! 🔥")
            st.markdown(
                f"""
                <div style='
                    background-color:#1e1e2f;
                    color:#e6e6e6;
                    padding:25px;
                    border-radius:12px;
                    box-shadow:0 4px 15px rgba(0, 0, 0, 0.3);
                    font-family:monospace;
                    line-height:1.6;
                    font-size:16px;
                '>
                <h3 style='color:#ff4d4f;'>AI Roast Report</h3>
                <hr style='border-color:#ff4d4f;' />
                {roast_output}
                </div>
                """,
                unsafe_allow_html=True
            )


        except Exception as e:
            st.error("Something went wrong while roasting. Check your API key or try again later.")
            st.code(str(e))

st.markdown("---")
st.markdown("Disclaimer: This is just for fun!")
st.markdown("Made with 🌶️ by Yukti")

