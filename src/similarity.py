from sklearn.feature_extraction.text import TfidfVectorizer
from  sklearn.metrics.pairwise import cosine_similarity

# function to calculate similarity score
def calculate_similarity(resume, job_desc):

    # create object
    vectorizer = TfidfVectorizer()

    # converting text into numerical form
    vectors = vectorizer.fit_transform([resume, job_desc])

    # compare both texts 
    score = cosine_similarity(vectors[0], vectors[1])

    # return percentage
    return score[0][0] * 100