from backend.resume_parser import extract_text
from backend.information_extractor import extract_information
from backend.matcher import calculate_match

from backend.skill_gap import find_missing_skills
from backend.export_excel import export_to_excel
from backend.export_pdf import export_to_pdf
from backend.email_sender import send_email

from database.database import create_database,save_candidate,get_all_candidates,search_candidates,update_candidate_status,get_candidate_by_id

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import LoginManager,login_required,login_user,logout_user,UserMixin

from flask import Flask,render_template,request,redirect,url_for,send_file

import os
create_database()
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
   def __init__(self,id):
      self.id = id 

@login_manager.user_loader
def load_user(user_id):
   return User(user_id)

UPLOAD_FOLDER = "resumes"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
@login_required
def dashboard():

    search = request.args.get("search", "")
    min_score = request.args.get("min_score", "")
    skill = request.args.get("skill", "")
    sort = request.args.get("sort", "score")

    candidates = get_all_candidates()

    if search:
        candidates = [
            c for c in candidates
            if search.lower() in c["name"].lower()
        ]

    if min_score:
        candidates = [
            c for c in candidates
            if c["score"] >= float(min_score)
        ]

    if skill:
        candidates = [
            c for c in candidates
            if skill.lower() in c["skills"].lower()
        ]

    if sort == "score":
        candidates.sort(key=lambda x: x["score"], reverse=True)

    elif sort == "name":
        candidates.sort(key=lambda x: x["name"])

    return render_template(
        "dashboard.html",
        candidates=candidates
    )

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("database/resume_screening.db")
        cursor = conn.cursor()

        # Check if the username already exists
        cursor.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return "Username already exists!"

        # Insert the new user
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hashed_password)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database/resume_screening.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT password_hash FROM users WHERE username=?",
            (username,)
        )

        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[0], password):
            login_user(User(username))
            return redirect(url_for("dashboard"))
        else:
            return "Invalid Username or Password"

    return render_template("login.html")
   
@app.route("/logout")
@login_required

def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/upload", methods=["POST"])
@login_required
def upload_resume():

    if "resumes" not in request.files:
        return "No file selected"
    
    job_description = request.form["job_description"]

    files = request.files.getlist("resumes")

    results = []

    for file in files:
        
        if file.filename == "":
            continue
    
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        text = extract_text(filepath)
        info = extract_information(text)
        score = calculate_match(text, job_description)

        save_candidate(
          file.filename,
          info["Email"],
          info["Phone"],
          info["Skills"],
          score
        )

        results.append({
          "name": file.filename,
          "score": score,
          "email": info["Email"],
          "phone": info["Phone"],
          "skills": info["Skills"]
        })
    
    results.sort(key=lambda x:x["score"],reverse=True)

    return render_template("result.html",results=results)

@app.route("/analytics")
@login_required
def analytics():

    candidates = get_all_candidates()   # Fetch from SQLite

    names = [c["name"] for c in candidates]
    scores = [c["score"] for c in candidates]

    total = len(candidates)
    average = round(sum(scores)/total, 2) if total else 0
    highest = max(scores) if scores else 0
    lowest = min(scores) if scores else 0

    return render_template(
        "analytics.html",
        candidates=candidates,
        labels=names,
        scores=scores,
        total=total,
        average_score=average,
        highest_score=highest,
        lowest_score=lowest
    )

@app.route("/shortlist", methods=["POST"])
@login_required
def shortlist():
    candidate_ids = request.form.getlist("candidate_ids")

    for candidate_id in candidate_ids:

        # Update status
        update_candidate_status(candidate_id, "Shortlisted")

        # Get candidate details
        candidate = get_candidate_by_id(candidate_id)

        if candidate:
            send_email(
                candidate["email"],
                candidate["name"]
            )

    return redirect("/dashboard")

@app.route("/export/excel")
@login_required
def export_excel():

    results = get_all_candidates()
    export_to_excel(results)

    return send_file(
        "Candidate_Report.xlsx",
        as_attachment=True
    )

@app.route("/export/pdf")
@login_required
def export_pdf_route():

    results = get_all_candidates()
    export_to_pdf(results)

    return send_file(
        "Candidate_Report.pdf",
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)



