# list of common skills
skills_list = [
    "python", "java", "sql", "machine learning", "data analysis", "pandas", 
    "numpy", "html", "css", "javascript", "react", "statistics", "excel", "power bi"
]

# function to find skills in text
def extract_skills(text):

    found_skills = []

    for skill in skills_list:
        if skill in text.lower():
            found_skills.append(skill)

    return found_skills