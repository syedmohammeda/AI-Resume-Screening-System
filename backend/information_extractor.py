import re

SKILLS = [
    "python", "java", "c", "c++", "sql", "html", "css",
    "javascript", "react", "flask", "django",
    "machine learning", "deep learning", "nlp",
    "tensorflow", "pytorch", "aws", "git"
]

def extract_information(text):

    email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)

    phone = re.findall(r"\+?\d[\d\s-]{8,}\d", text)

    skills = []

    lower = text.lower()

    for skill in SKILLS:
        if skill in lower:
            skills.append(skill)

    return {
        "Email": email[0] if email else "Not Found",
        "Phone": phone[0] if phone else "Not Found",
        "Skills": skills
    }