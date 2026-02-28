from datetime import date
from app.repositories.slot_repo import SlotRepo
from app.repositories.appointment_repo import AppointmentRepo

def is_weekend(d: date) -> bool:
    return d.weekday() >= 5

class DoctorService:
    def __init__(self, slot_repo: SlotRepo, appt_repo: AppointmentRepo):
        self.slot_repo = slot_repo
        self.appt_repo = appt_repo

    def create_day_slots(self, doctor_id: int, d: date, times: list[str]):
        if d < date.today():
            raise ValueError("Date passée non autorisée.")
        if is_weekend(d):
            raise ValueError("Week-end (fermé).")
        if not times:
            raise ValueError("Veuillez sélectionner au moins un créneau.")
        self.slot_repo.create_day_slots(doctor_id, d.isoformat(), times)

    def list_schedule(self, doctor_id: int):
        return self.appt_repo.list_for_doctor(doctor_id)