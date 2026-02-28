# app/config.py

DB_PATH = "medical_appointments.db"
APP_TITLE = "Système de gestion des rendez-vous médicaux"
APP_SIZE = "860x520"

# Full-day time slots (08:00 → 18:00 every 30 min)
SLOT_TIMES = [f"{h:02d}:{m:02d}" for h in range(8, 19) for m in (0, 30)]

# Common medical specialties (you can extend this list)
SPECIALTIES = [
    "Cardiologie",
    "Dermatologie",
    "Endocrinologie",
    "Gastro-entérologie",
    "Généraliste",
    "Gynécologie",
    "Neurologie",
    "Ophtalmologie",
    "ORL",
    "Pédiatrie",
    "Pneumologie",
    "Psychiatrie",
    "Radiologie",
    "Rhumatologie",
    "Urologie",
]