import sqlite3
from app.database.db import get_connection

class SlotRepo:
    def create_day_slots(self, doctor_id: int, dstr: str, times: list[str]):
        con = get_connection()
        cur = con.cursor()
        for t in times:
            try:
                cur.execute("""
                    INSERT INTO doctor_slots(doctor_id, date, time)
                    VALUES(?,?,?)
                """, (doctor_id, dstr, t))
            except sqlite3.IntegrityError:
                pass
        con.commit()
        con.close()

    def get_slots_for_day(self, doctor_id: int, dstr: str):
        con = get_connection()
        cur = con.cursor()
        cur.execute("""
            SELECT time FROM doctor_slots
            WHERE doctor_id=? AND date=?
            ORDER BY time
        """, (doctor_id, dstr))
        times = [r[0] for r in cur.fetchall()]
        con.close()
        return times