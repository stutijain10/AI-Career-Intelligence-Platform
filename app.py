from dotenv import load_dotenv
from openai import OpenAI

import os
import streamlit as st
import matplotlib.pyplot as plt

from src.similarity import calculate_similarity
from src.skill_extractor import extract_skills
from src.recommendation import recommend_role

load_dotenv()

st.set_page_config(
    page_title="AI STEM Learning Platform",
    page_icon="🚀",
    layout="wide"
)

client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

# Title
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

st.markdown("Analyze your resume, learn STEM skills, and get AI-powered career guidance.")

# Sidebar
st.sidebar.title("🚀 Navigation")

st.sidebar.info("""
AI STEM Learning Platform

Features:
- 🤖 AI Doubt Solver
- 🧠 Quiz Generator
- 🗺️ Learning Roadmap
- 📄 Resume Analyzer
""")

# =========================
# AI DOUBT SOLVER
# =========================

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

st.markdown("---")
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

                st.success("Response Generated Successfully!")
                st.write(quiz)

            except Exception as e:

                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a quiz topic.")

# =========================
# LEARNING ROADMAP GENERATOR
# =========================

st.markdown("---")
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

                st.success("Response Generated Successfully!")
                st.write(roadmap)

            except Exception as e:

                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a roadmap topic.")

# =========================
# RESUME ANALYZER
# =========================

st.markdown("---")
st.header("📄 AI Resume Analyzer")

with st.form("resume_form"):

    st.subheader("📄 Resume Input")
    resume_text = st.text_area(
        "Paste your resume here"
    )

    st.subheader("💼 Job Description")
    job_text = st.text_area(
        "Paste job description here"
    )

    submit_resume = st.form_submit_button("Analyze Resume")

if submit_resume:

    try:

        if resume_text == "" or job_text == "":

            st.warning("Please enter both resume and job description")

        else:

            score = calculate_similarity(resume_text, job_text)

            st.success(f"Match Score: {score:.2f}%")

            if score > 70:
                st.success("Excellent match! You are a strong candidate.")

            elif score > 40:
                st.info("Good match, but you can improve your skills.")

            else:
                st.warning("Low match. Consider improving your skills for this role.")

            resume_skills = extract_skills(resume_text)
            job_skills = extract_skills(job_text)

            st.write("Your Skills: ", resume_skills)
            st.write("Required Skills: ", job_skills)

            common_skills = list(set(resume_skills) & set(job_skills))

            st.write("Matching Skills:", common_skills)

            missing_skills = list(set(job_skills) - set(resume_skills))

            st.write("Skills You Need:", missing_skills)

            recommended_role = recommend_role(resume_skills)

            st.subheader(f"Recommended Role: {recommended_role}")

            if len(missing_skills) > 0:

                st.subheader("Suggestions to Improve")

                for skill in missing_skills:
                    st.write(f"- Learn {skill}")

            else:
                st.success("Great! You have most of the required skills.")

            labels = ["Match Score (%)", "Number of Skills"]

            values = [score, len(resume_skills)]

            plt.figure()

            plt.bar(labels, values)

            st.subheader("Performance Overview")

            plt.title("Resume Performance Analysis")
            st.pyplot(plt)

            st.caption("This graph shows how well your resume matches the job and how many relevant skills you have.")

    except Exception as e:

        st.error(f"Error: {e}")

st.markdown("---")

st.markdown(
    "Made with ❤️ using Streamlit + Groq AI"
)