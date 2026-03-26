#  roles with required skills
roles = {
    "Data Scientist": ["python", "machine learning", "statistics"],
    "Web Developer": ["html", "css", "javascript"],
    "Data Analyst": ["sql", "excel", "data analysis"]
}

# function to recommend role
def recommend_role(user_skills):
    scores = {}
    for role, skills in roles.items():
        match = len(set(user_skills) & set(skills))
        scores[role] = match

    # return best matching role
    return max(scores, key=scores.get)