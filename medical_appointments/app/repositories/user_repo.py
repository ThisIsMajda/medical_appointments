import sqlite3
import bcrypt
from app.database.db import get_connection

class UserRepo:
    def get_by_username(self, username: str):
        con = get_connection()
        cur = con.cursor()
        cur.execute("""
            SELECT id, username, password_hash, role, full_name, specialty
            FROM users WHERE username=?
        """, (username,))
        row = cur.fetchone()
        con.close()
        return row

    def create_user(self, username: str, password_plain: str, role: str, full_name: str, specialty: str | None):
        con = get_connection()
        cur = con.cursor()
        pw_hash = bcrypt.hashpw(password_plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        try:
            cur.execute("""
                INSERT INTO users(username, password_hash, role, full_name, specialty)
                VALUES(?,?,?,?,?)
            """, (username, pw_hash, role, full_name, specialty))
            con.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Nom d’utilisateur déjà utilisé.")
        finally:
            con.close()

    def list_doctors(self):
        con = get_connection()
        cur = con.cursor()
        cur.execute("""
            SELECT id, full_name, specialty, username
            FROM users WHERE role='DOCTOR'
            ORDER BY full_name
        """)
        rows = cur.fetchall()
        con.close()
        return rows

    def delete_doctor(self, doctor_id: int):
        con = get_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM users WHERE id=? AND role='DOCTOR'", (doctor_id,))
        con.commit()
        con.close()