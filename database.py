import sqlite3

def create_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            password TEXT,
            mobile TEXT,
            dob TEXT,
            gender TEXT,
            email TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_user(username, password, mobile, dob, gender, email):

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Check existing user
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    if c.fetchone():
        conn.close()
        return "exists"

    # Insert
    c.execute("""
        INSERT INTO users(username, password, mobile, dob, gender, email)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (username, password, mobile, dob, gender, email))

    conn.commit()
    conn.close()

    return "success"


def login_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    data = c.fetchone()

    conn.close()
    return data