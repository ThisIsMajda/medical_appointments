from datetime import date, datetime
from app.repositories.slot_repo import SlotRepo
from app.repositories.appointment_repo import AppointmentRepo

class AppointmentService:
    def __init__(self, slot_repo: SlotRepo, appt_repo: AppointmentRepo):
        self.slot_repo = slot_repo
        self.appt_repo = appt_repo

    def _now_time_str(self) -> str:
        return datetime.now().strftime("%H:%M")

    # ✅ added exclude_appointment_id
    def available_times(self, doctor_id: int, d: date, exclude_appointment_id: int | None = None):
        if d < date.today():
            raise ValueError("Date passée non autorisée.")

        dstr = d.isoformat()

        # Slots created by doctor
        created = self.slot_repo.get_slots_for_day(doctor_id, dstr)
        if not created:
            return []

        # ✅ exclude current appointment when modifying
        booked = self.appt_repo.booked_times(
            doctor_id,
            dstr,
            exclude_appointment_id
        )

        free = [t for t in created if t not in booked]

        # Block past timeslots if today
        if d == date.today():
            now_t = self._now_time_str()
            free = [t for t in free if t > now_t]

        return free

    def book(self, patient_id: int, doctor_id: int, d: date, t: str, urgent: bool, reason: str):
        if d < date.today():
            raise ValueError("Date passée non autorisée.")
        if d == date.today():
            if not t or t <= self._now_time_str():
                raise ValueError("Ce créneau est déjà passé. Veuillez choisir un autre.")

        if not t:
            raise ValueError("Veuillez sélectionner un créneau.")

        is_urgent = 1 if urgent else 0
        reason_clean = (reason or "").strip()

        if urgent:
            if len(reason_clean) < 5:
                raise ValueError("Veuillez préciser le motif de l’urgence (min 5 caractères).")
        else:
            reason_clean = None

        times = self.available_times(doctor_id, d)
        if t not in times:
            raise ValueError("Créneau indisponible. Veuillez rafraîchir et choisir un autre.")

        self.appt_repo.create(
            patient_id,
            doctor_id,
            d.isoformat(),
            t,
            is_urgent,
            reason_clean
        )

    def cancel(self, appointment_id: int, appt_date: str):
        d = date.fromisoformat(appt_date)
        if d < date.today():
            raise ValueError("Impossible d’annuler un rendez-vous passé.")
        self.appt_repo.cancel(appointment_id)

    def modify(self, appointment_id: int, doctor_id: int, new_date: date, new_time: str):
        if new_date < date.today():
            raise ValueError("Date passée non autorisée.")
        if new_date == date.today():
            if not new_time or new_time <= self._now_time_str():
                raise ValueError("Ce créneau est déjà passé. Veuillez choisir un autre.")

        if not new_time:
            raise ValueError("Veuillez sélectionner un créneau.")

        # ✅ pass exclude_appointment_id here
        times = self.available_times(
            doctor_id,
            new_date,
            exclude_appointment_id=appointment_id
        )

        if new_time not in times:
            raise ValueError("Créneau indisponible. Veuillez choisir un autre.")

        self.appt_repo.update_datetime(
            appointment_id,
            new_date.isoformat(),
            new_time
        )