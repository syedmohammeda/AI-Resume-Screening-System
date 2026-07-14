import sqlite3

conn = sqlite3.connect("database/resume_screening.db")
cursor = conn.cursor()

try:
    cursor.execute("""
    ALTER TABLE candidates
    ADD COLUMN status TEXT DEFAULT 'Pending'
    """)
    print("Status column added successfully.")
except sqlite3.OperationalError:
    print("Status column already exists.")

conn.commit()
conn.close()