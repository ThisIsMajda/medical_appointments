import sqlite3
from datetime import date, timedelta
from app.database.db import get_connection

class AppointmentRepo:
    def create(self, patient_id: int, doctor_id: int, dstr: str, tstr: str, is_urgent: int, reason: str | None):
        con = get_connection()
        cur = con.cursor()
        try:
            cur.execute("""
                INSERT INTO appointments(patient_id, doctor_id, date, time, is_urgent, reason)
                VALUES(?,?,?,?,?,?)
            """, (patient_id, doctor_id, dstr, tstr, is_urgent, reason))
            con.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Ce créneau vient d’être pris. Veuillez choisir un autre créneau.")
        finally:
            con.close()

    def list_for_patient(self, patient_id: int):
        con = get_connection()
        cur = con.cursor()
        cur.execute("""
            SELECT a.id, u.full_name, a.date, a.time, a.is_urgent, COALESCE(a.reason,'')
            FROM appointments a
            JOIN users u ON u.id = a.doctor_id
            WHERE a.patient_id=?
            ORDER BY a.date, a.time
        """, (patient_id,))
        rows = cur.fetchall()
        con.close()
        return rows

    def list_for_doctor(self, doctor_id: int):
        con = get_connection()
        cur = con.cursor()
        cur.execute("""
            SELECT a.id, a.date, a.time, u.full_name, a.is_urgent, COALESCE(a.reason,'')
            FROM appointments a
            JOIN users u ON u.id = a.patient_id
            WHERE a.doctor_id=?
            ORDER BY a.date, a.time
        """, (doctor_id,))
        rows = cur.fetchall()
        con.close()
        return rows

    def cancel(self, appointment_id: int):
        con = get_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM appointments WHERE id=?", (appointment_id,))
        con.commit()
        con.close()

    def update_datetime(self, appointment_id: int, new_date: str, new_time: str):
        con = get_connection()
        cur = con.cursor()
        try:
            cur.execute("""
                UPDATE appointments
                SET date=?, time=?
                WHERE id=?
            """, (new_date, new_time, appointment_id))
            con.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Créneau indisponible. Veuillez choisir un autre.")
        finally:
            con.close()

    # ✅ FIXED: allow excluding the appointment being modified
    def booked_times(self, doctor_id: int, dstr: str, exclude_appointment_id: int | None = None):
        con = get_connection()
        cur = con.cursor()

        if exclude_appointment_id is None:
            cur.execute("""
                SELECT time FROM appointments
                WHERE doctor_id=? AND date=?
            """, (doctor_id, dstr))
        else:
            cur.execute("""
                SELECT time FROM appointments
                WHERE doctor_id=? AND date=? AND id<>?
            """, (doctor_id, dstr, exclude_appointment_id))

        booked = {r[0] for r in cur.fetchall()}
        con.close()
        return booked

    def exists_future_for_doctor(self, doctor_id: int):
        today = date.today().isoformat()
        con = get_connection()
        cur = con.cursor()
        cur.execute("""
            SELECT COUNT(*) FROM appointments
            WHERE doctor_id=? AND date>=?
        """, (doctor_id, today))
        count = cur.fetchone()[0]
        con.close()
        return count > 0

    def get_tomorrow_for_patient(self, patient_id: int):
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        con = get_connection()
        cur = con.cursor()
        cur.execute("""
            SELECT u.full_name, a.time, a.is_urgent, COALESCE(a.reason,'')
            FROM appointments a
            JOIN users u ON u.id = a.doctor_id
            WHERE a.patient_id=? AND a.date=?
            ORDER BY a.time
        """, (patient_id, tomorrow))
        rows = cur.fetchall()
        con.close()
        return rows

    def get_doctor_id_for_appointment(self, appointment_id: int):
        con = get_connection()
        cur = con.cursor()
        cur.execute("SELECT doctor_id FROM appointments WHERE id=?", (appointment_id,))
        row = cur.fetchone()
        con.close()
        return row[0] if row else None