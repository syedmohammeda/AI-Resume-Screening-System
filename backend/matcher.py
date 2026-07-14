from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match(resume_text, job_description):
    documents = [resume_text, job_description]

    tfidf = TfidfVectorizer(stop_words="english")
    matrix = tfidf.fit_transform(documents)

    similarity = cosine_similarity(matrix[0:1], matrix[1:2])

    score = round(similarity[0][0] * 100, 2)

    return score