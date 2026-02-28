import sqlite3
import bcrypt
from app.config import DB_PATH

def get_connection():
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON;")
    return con

def init_db():
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('PATIENT','DOCTOR','ADMIN')),
        full_name TEXT NOT NULL,
        specialty TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS doctor_slots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        UNIQUE(doctor_id, date, time),
        FOREIGN KEY(doctor_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        is_urgent INTEGER NOT NULL DEFAULT 0,
        reason TEXT,
        UNIQUE(doctor_id, date, time),
        FOREIGN KEY(patient_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY(doctor_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # Default admin: admin/admin
    cur.execute("SELECT id FROM users WHERE role='ADMIN' LIMIT 1;")
    if cur.fetchone() is None:
        pw_hash = bcrypt.hashpw(b"admin", bcrypt.gensalt()).decode("utf-8")
        cur.execute("""
            INSERT INTO users(username, password_hash, role, full_name, specialty)
            VALUES(?,?,?,?,?)
        """, ("admin", pw_hash, "ADMIN", "Administrateur", None))

    con.commit()
    con.close()