from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the model once when the app starts
model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_match(resume_text, job_description):
    resume_embedding = model.encode([resume_text])
    job_embedding = model.encode([job_description])

    score = cosine_similarity(resume_embedding, job_embedding)[0][0]

    return round(score * 100, 2)