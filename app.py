import streamlit as st
from src.similarity import calculate_similarity 
from src.skill_extractor import extract_skills
from src.recommendation import recommend_role
import matplotlib.pyplot as plt

st.markdown("### Analyze your resume and get AI-powered career insights 🚀")

# This is the title of our app
st.title("AI Career Intelligence Platform")

# Taking resume input from user
st.subheader("📄 Resume Input")
resume_text = st.text_area("Paste your resume here")

# Taking job description input
st.subheader("💼 Job Description")
job_text = st.text_area("Paste job description here")

# Button to trigger analysis
if st.button("Analyze Resume"):

    # Checking if user entered both fields
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

        # extracting skills
        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_text)

        st.write("Your Skills: ", resume_skills)
        st.write("Required Skills: ", job_skills)

        common_skills = list(set(resume_skills) & set(job_skills))
        st.write("Matching Skills:", common_skills)

        # finding missing skills
        missing_skills = list(set(job_skills) - set(resume_skills))

        st.write("Skills You Need:", missing_skills)

        # recommend role
        recommended_role = recommend_role(resume_skills)

        st.subheader(f"Recommended Role: {recommended_role}")

        # suggestions based on missing skills
        if len(missing_skills) > 0:
            st.subheader("Suggestions to Improve")

            for skill in missing_skills:
                st.write(f"- Learn {skill}")

        else:
            st.success("Great! You have most of the required skills.")

        # simple bar chart
        labels = ["Match Score (%)", "Number of Skills"]
        values = [score, len(resume_skills)]

        plt.figure()
        plt.bar(labels, values)

        st.subheader("Performance Overview")
        st.pyplot(plt)
        st.caption("This graph shows how well your resume matches the job and how many relevant skills you have.")
            

st.markdown("---")  

