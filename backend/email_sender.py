import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

def send_email(receiver_email, candidate_name):
    subject = "Interview Invitation"

    body = f"""
Dear {candidate_name},

Congratulations!

You have been shortlisted for the next round of our recruitment process.

We will contact you shortly with the interview schedule.

Best Regards,
HR Team
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = receiver_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL, APP_PASSWORD)
        server.send_message(msg)

    print("Email sent successfully!")