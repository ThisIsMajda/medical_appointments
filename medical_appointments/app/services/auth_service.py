import bcrypt
from app.repositories.user_repo import UserRepo

def normalize_username(u: str) -> str:
    return (u or "").strip().lower()

class AuthService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    def login(self, username: str, password: str, required_role: str):
        username = normalize_username(username)
        if not username or not password:
            raise ValueError("Veuillez remplir tous les champs.")

        row = self.user_repo.get_by_username(username)
        if not row:
            raise ValueError("Identifiants incorrects.")

        uid, uname, pw_hash, role, full_name, specialty = row

        if role != required_role:
            raise ValueError("Accès refusé.")

        if not bcrypt.checkpw(password.encode("utf-8"), pw_hash.encode("utf-8")):
            raise ValueError("Identifiants incorrects.")

        return {"id": uid, "username": uname, "role": role, "full_name": full_name, "specialty": specialty}

    def register_patient(self, full_name: str, username: str, password: str):
        full_name = (full_name or "").strip()
        username = normalize_username(username)
        if not full_name or not username or not password:
            raise ValueError("Veuillez remplir tous les champs.")
        if len(password) < 4:
            raise ValueError("Mot de passe trop court (min 4 caractères).")

        self.user_repo.create_user(username, password, "PATIENT", full_name, None)