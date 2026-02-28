from app.repositories.user_repo import UserRepo
from app.repositories.appointment_repo import AppointmentRepo
from app.services.auth_service import normalize_username

class AdminService:
    def __init__(self, user_repo: UserRepo, appt_repo: AppointmentRepo):
        self.user_repo = user_repo
        self.appt_repo = appt_repo

    def add_doctor(self, full_name: str, specialty: str, username: str, password: str):
        full_name = (full_name or "").strip()
        specialty = (specialty or "").strip()
        username = normalize_username(username)

        if not full_name or not specialty or not username or not password:
            raise ValueError("Veuillez remplir tous les champs.")
        if len(password) < 4:
            raise ValueError("Mot de passe trop court (min 4 caractères).")

        self.user_repo.create_user(username, password, "DOCTOR", full_name, specialty)

    def delete_doctor(self, doctor_id: int):
        # Policy: block deletion if future appointments exist
        if self.appt_repo.exists_future_for_doctor(doctor_id):
            raise ValueError("Suppression impossible : ce médecin a des rendez-vous à venir.")
        self.user_repo.delete_doctor(doctor_id)