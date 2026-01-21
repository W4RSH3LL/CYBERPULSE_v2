import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("auth.db")
c = conn.cursor()

c.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

# Default admin account
c.execute(
    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
    ("admin", generate_password_hash("admin123"), "admin")
)

conn.commit()
conn.close()

print("Database initialized successfully.")
