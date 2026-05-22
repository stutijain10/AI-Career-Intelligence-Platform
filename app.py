from dotenv import load_dotenv
from openai import OpenAI

import os
import streamlit as st
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader

from src.similarity import calculate_similarity
from src.skill_extractor import extract_skills
from src.recommendation import recommend_role

# =========================
# LOAD ENV VARIABLES
# =========================

load_dotenv()

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI STEM Learning Platform",
    page_icon="🚀",
    layout="wide"
)

# =========================
# GROQ CLIENT
# =========================

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# =========================
# TABS
# =========================

tabs = st.tabs([
    "🏠 Home",
    "🤖 Doubt Solver",
    "🧠 Quiz Generator",
    "🗺️ Roadmap",
    "📄 Resume Analyzer"
])

# =========================
# HOME PAGE
# =========================

with tabs[0]:

    st.title("🚀 AI STEM Learning & Career Intelligence Platform")

    st.markdown("""
    Welcome to the AI-powered STEM Learning & Career Intelligence Platform 🎓

    This platform helps students:

    - Learn STEM topics
    - Generate quizzes
    - Create learning roadmaps
    - Analyze resumes
    - Get AI-powered career insights
    """)

    st.markdown(
        "Analyze your resume, learn STEM skills, and get AI-powered career guidance."
    )

# =========================
# AI DOUBT SOLVER
# =========================

with tabs[1]:

    st.header("🤖 AI Doubt Solver")

    with st.form("doubt_form"):

        question = st.text_input(
            "Ask any STEM question",
            placeholder="Example: Explain Newton's Laws"
        )

        submit_question = st.form_submit_button("Get Answer")

    if submit_question:

        if question:

            with st.spinner("Generating response..."):

                try:

                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a friendly STEM teacher who explains concepts simply."
                            },
                            {
                                "role": "user",
                                "content": question
                            }
                        ]
                    )

                    answer = response.choices[0].message.content

                    st.success("Response Generated Successfully!")
                    st.write(answer)

                except Exception as e:

                    st.error(f"Error: {e}")

        else:

            st.warning("Please enter a question.")

# =========================
# AI QUIZ GENERATOR
# =========================

with tabs[2]:

    st.header("🧠 AI Quiz Generator")

    with st.form("quiz_form"):

        quiz_topic = st.text_input(
            "Enter a topic for quiz",
            placeholder="Example: Python Basics"
        )

        submit_quiz = st.form_submit_button("Generate Quiz")

    if submit_quiz:

        if quiz_topic:

            with st.spinner("Generating quiz..."):

                try:

                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {
                                "role": "system",
                                "content": "Generate 3 simple MCQ quiz questions with answers for students."
                            },
                            {
                                "role": "user",
                                "content": f"Create quiz on {quiz_topic}"
                            }
                        ]
                    )

                    quiz = response.choices[0].message.content

                    st.success("Quiz Generated Successfully!")
                    st.write(quiz)

                except Exception as e:

                    st.error(f"Error: {e}")

        else:

            st.warning("Please enter a quiz topic.")

# =========================
# LEARNING ROADMAP GENERATOR
# =========================

with tabs[3]:

    st.header("🗺️ AI Learning Roadmap")

    with st.form("roadmap_form"):

        roadmap_topic = st.text_input(
            "Enter a topic to generate roadmap",
            placeholder="Example: Data Science"
        )

        submit_roadmap = st.form_submit_button("Generate Roadmap")

    if submit_roadmap:

        if roadmap_topic:

            with st.spinner("Generating roadmap..."):

                try:

                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {
                                "role": "system",
                                "content": "Generate a beginner-friendly step-by-step learning roadmap for STEM students."
                            },
                            {
                                "role": "user",
                                "content": f"Create roadmap for {roadmap_topic}"
                            }
                        ]
                    )

                    roadmap = response.choices[0].message.content

                    st.success("Roadmap Generated Successfully!")
                    st.write(roadmap)

                except Exception as e:

                    st.error(f"Error: {e}")

        else:

            st.warning("Please enter a roadmap topic.")

# =========================
# RESUME ANALYZER
# =========================

with tabs[4]:

    st.header("📄 AI Resume Analyzer")

    with st.form("resume_form"):
        st.subheader("📄 Upload Resume")

        uploaded_file = st.file_uploader(
            "Upload Resume PDF",
            type=["pdf"]
        )

        resume_text = ""

        if uploaded_file is not None:

            pdf_reader = PdfReader(uploaded_file)

            for page in pdf_reader.pages:

                resume_text += page.extract_text()
                
        st.subheader("💼 Job Description")

        job_text = st.text_area(
            "Paste job description here",
            height=250
        )

        submit_resume = st.form_submit_button("Analyze Resume")

    if submit_resume:

        try:

            if resume_text == "" or job_text == "":

                st.warning("Please enter both resume and job description")

            else:

                with st.spinner("Analyzing resume..."):

                    score = calculate_similarity(resume_text, job_text)

                    st.success(f"Match Score: {score:.2f}%")

                    if score > 70:

                        st.success("Excellent match! You are a strong candidate.")

                    elif score > 40:

                        st.info("Good match, but you can improve your skills.")

                    else:

                        st.warning("Low match. Consider improving your skills for this role.")

                    # =========================
                    # SKILLS ANALYSIS
                    # =========================

                    resume_skills = extract_skills(resume_text)
                    job_skills = extract_skills(job_text)

                    st.write("### Your Skills")
                    st.write(resume_skills)

                    st.write("### Required Skills")
                    st.write(job_skills)

                    common_skills = list(
                        set(resume_skills) & set(job_skills)
                    )

                    st.write("### Matching Skills")
                    st.write(common_skills)

                    missing_skills = list(
                        set(job_skills) - set(resume_skills)
                    )

                    st.write("### Skills You Need")
                    st.write(missing_skills)

                    # =========================
                    # ROLE RECOMMENDATION
                    # =========================

                    recommended_role = recommend_role(resume_skills)

                    st.subheader(
                        f"🎯 Recommended Role: {recommended_role}"
                    )

                    # =========================
                    # IMPROVEMENT SUGGESTIONS
                    # =========================

                    if len(missing_skills) > 0:

                        st.subheader("📚 Suggestions to Improve")

                        for skill in missing_skills:

                            st.write(f"• Learn {skill}")

                    else:

                        st.success(
                            "Great! You have most of the required skills."
                        )

                    # =========================
                    # CHART
                    # =========================

                    labels = [
                        "Match Score (%)",
                        "Number of Skills"
                    ]

                    values = [
                        score,
                        len(resume_skills)
                    ]

                    fig, ax = plt.subplots()

                    ax.bar(labels, values)

                    ax.set_title("Resume Performance Analysis")

                    st.subheader("📊 Performance Overview")

                    st.pyplot(fig)

                    st.caption(
                        "This graph shows how well your resume matches the job and how many relevant skills you have."
                    )

        except Exception as e:

            st.error(f"Error: {e}")

# =========================
# FOOTER
# =========================

st.markdown("---")

st.markdown(
    "Made with ❤️ using Streamlit + Groq AI"
)