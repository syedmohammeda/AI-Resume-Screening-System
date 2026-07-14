import re

def find_missing_skills(job_description, resume_text):
    job_words = set(re.findall(r"\b[a-zA-Z+\#]+\b", job_description.lower()))
    resume_words = set(re.findall(r"\b[a-zA-Z+\#]+\b", resume_text.lower()))

    return sorted(list(job_words - resume_words))