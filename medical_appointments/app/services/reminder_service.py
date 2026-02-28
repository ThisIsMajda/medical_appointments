from app.repositories.appointment_repo import AppointmentRepo

class ReminderService:
    def __init__(self, appt_repo: AppointmentRepo):
        self.appt_repo = appt_repo

    def reminders_on_login(self, patient_id: int):
        return self.appt_repo.get_tomorrow_for_patient(patient_id)