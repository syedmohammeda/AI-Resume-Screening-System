import sqlite3

def create_database():
    conn = sqlite3.connect("database/resume_screening.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        skills TEXT,
        score REAL,
        status TEXT DEFAULT 'Pending'
    )
    """)
    cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)
""")

    conn.commit()
    conn.close()

def save_candidate(name, email, phone, skills, score):
    conn = sqlite3.connect("database/resume_screening.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO candidates(name,email,phone,skills,score,status)
    VALUES(?,?,?,?,?,?)
    """, (
        name,
        email,
        phone,
        ",".join(skills),
        score,
        "Pending"
    ))

    conn.commit()
    conn.close()

def search_candidates(search):
    conn = sqlite3.connect("database/resume_screening.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, email, phone, skills, score
        FROM candidates
        WHERE name LIKE ?
    """, ('%' + search + '%',))

    rows = cursor.fetchall()
    conn.close()

    candidates = []

    for row in rows:
        candidates.append({
            "name": row["name"],
            "email": row["email"],
            "phone": row["phone"],
            "skills": row["skills"],
            "score": row["score"]
        })

    return candidates

def get_all_candidates():

    import sqlite3

    conn = sqlite3.connect("database/resume_screening.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""SELECT id,name,email,phone,skills,score,status FROM candidates ORDER BY score DESC""" )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

def update_candidate_status(candidate_id, status):
    conn = sqlite3.connect("database/resume_screening.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE candidates SET status = ? WHERE id = ?",
        (status, candidate_id)
    )

    conn.commit()
    conn.close()

def get_candidate_by_id(candidate_id):
    conn = sqlite3.connect("database/resume_screening.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM candidates WHERE id = ?",
        (candidate_id,)
    )

    candidate = cursor.fetchone()

    conn.close()

    return candidate