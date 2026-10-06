import sqlite3

DB_NAME = "complaints.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            category TEXT NOT NULL,
            complaint TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            response TEXT DEFAULT ''
        )
    """)

    conn.commit()
    conn.close()


def add_complaint(name, email, category, complaint):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO complaints
        (name, email, category, complaint, status, response)
        VALUES (?, ?, ?, ?, 'Pending', '')
    """, (name, email, category, complaint))

    conn.commit()
    conn.close()


def get_complaints():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, category, complaint, status, response
        FROM complaints
        ORDER BY id DESC
    """)

    complaints = cursor.fetchall()

    conn.close()

    return complaints


def update_complaint(complaint_id, status, response):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE complaints
        SET status = ?, response = ?
        WHERE id = ?
    """, (status, response, complaint_id))

    conn.commit()
    conn.close()