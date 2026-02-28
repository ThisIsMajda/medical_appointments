import tkinter as tk
from tkinter import ttk

from app.config import APP_TITLE, APP_SIZE
from app.repositories.user_repo import UserRepo
from app.repositories.slot_repo import SlotRepo
from app.repositories.appointment_repo import AppointmentRepo
from app.services.auth_service import AuthService
from app.services.admin_service import AdminService
from app.services.doctor_service import DoctorService
from app.services.appointment_service import AppointmentService
from app.services.reminder_service import ReminderService
from app.gui.screens import build_screens


# =========================
# Dark hospital / startup style (TTK)
# =========================
def apply_dark_ttk_style(root: tk.Tk):
    style = ttk.Style(root)

    # "clam" is the most customizable cross-platform theme
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    bg = "#0F172A"       # app background
    surface = "#1E293B"  # card/surface
    border = "#334155"
    text = "#F1F5F9"
    muted = "#94A3B8"
    primary = "#2563EB"

    # Combobox
    style.configure(
        "TCombobox",
        fieldbackground=surface,
        background=surface,
        foreground=text,
        arrowcolor=muted,
        bordercolor=border,
        lightcolor=border,
        darkcolor=border,
        relief="flat",
        padding=6
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", surface), ("disabled", surface)],
        foreground=[("readonly", text), ("disabled", muted)],
        background=[("readonly", surface), ("active", surface)]
    )

    # Scrollbar
    style.configure(
        "TScrollbar",
        troughcolor=bg,
        background=border,
        bordercolor=bg,
        arrowcolor=muted
    )

    # Optional: tweak classic ttk labels/buttons if you use them
    style.configure("TLabel", background=bg, foreground=text)
    style.configure("TFrame", background=bg)
    style.configure("TButton", padding=8)


class TkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(APP_SIZE)

        # ✅ Dark + professional
        self.configure(bg="#0F172A")

        # ✅ Allow resize so nothing is hidden
        self.resizable(True, True)

        # ✅ Apply ttk theme (Combobox/Scrollbar)
        apply_dark_ttk_style(self)

        # repos
        self.user_repo = UserRepo()
        self.slot_repo = SlotRepo()
        self.appt_repo = AppointmentRepo()

        # services
        self.auth_service = AuthService(self.user_repo)
        self.admin_service = AdminService(self.user_repo, self.appt_repo)
        self.doctor_service = DoctorService(self.slot_repo, self.appt_repo)
        self.appt_service = AppointmentService(self.slot_repo, self.appt_repo)
        self.reminder_service = ReminderService(self.appt_repo)

        self.current_user = None

        # ✅ container background + expands correctly
        container = tk.Frame(self, bg="#0F172A")
        container.pack(fill="both", expand=True)

        # ✅ CRITICAL: frames expand with sticky="nsew"
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = build_screens(container, self)
        self.show("MainMenu")

    def show(self, name: str):
        frame = self.frames[name]
        if hasattr(frame, "on_show"):
            frame.on_show()
        frame.tkraise()

    def logout(self):
        self.current_user = None
        self.show("MainMenu")