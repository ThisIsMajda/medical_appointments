import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import date, datetime, time
from app.config import SPECIALTIES, SLOT_TIMES

# ================= THEME (Dark / Hospital / Minimal) =================

COLORS = {
    "bg": "#0B1220",          # darker + more serious
    "surface": "#101A2E",     # app surfaces
    "card": "#0F1B2D",        # cards
    "border": "#22314A",
    "text": "#EAF0FF",
    "muted": "#9AA7C0",
    "primary": "#2563EB",
    "primary_hover": "#1D4ED8",
    "danger": "#DC2626",
    "input_bg": "#0B1628",
    "slot_bg": "#0C1729",
    "slot_active": "#16335A",
}

FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_H2 = ("Segoe UI", 13, "bold")
FONT_TEXT = ("Segoe UI", 10)
FONT_BTN = ("Segoe UI", 10, "bold")

# ---------- Helpers ----------

def parse_date_str(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()

def _parse_hhmm(s: str) -> time | None:
    try:
        return datetime.strptime(s, "%H:%M").time()
    except Exception:
        return None

def _is_past_slot(day: date, slot_str: str) -> bool:
    """
    Block past dates and past time slots for today.
    """
    now = datetime.now()
    if day < now.date():
        return True
    if day > now.date():
        return False
    t = _parse_hhmm(slot_str)
    if not t:
        return False
    return datetime.combine(day, t) <= now

def card_frame(parent):
    f = tk.Frame(
        parent,
        bg=COLORS["card"],
        bd=1,
        highlightbackground=COLORS["border"],
        highlightthickness=1
    )
    f.pack(padx=60, pady=26, fill="both", expand=False)
    return f

def section_title(parent, text):
    tk.Label(
        parent, text=text,
        fg=COLORS["text"], bg=COLORS["bg"],
        font=FONT_TITLE
    ).pack(pady=(18, 10))

def big_button(parent, text, command, kind="primary"):

    if kind == "primary":
        bg = COLORS["primary"]
        fg = "white"
        active = COLORS["primary_hover"]

    elif kind == "danger":
        bg = COLORS["danger"]
        fg = "white"
        active = "#B91C1C"

    else:  # secondary
        bg = COLORS["card"]
        fg = COLORS["text"]
        active = COLORS["slot_active"]

    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        activebackground=active,
        activeforeground=fg,
        relief="flat",
        bd=0,
        padx=18,
        pady=12,
        font=FONT_BTN,
        cursor="hand2"
    )

def labeled_entry(parent, label, show=None):
    row = tk.Frame(parent, bg=COLORS["card"])
    row.pack(pady=8, fill="x")

    tk.Label(
        row,
        text=label,
        fg=COLORS["muted"],
        bg=COLORS["card"],
        font=FONT_TEXT,
        width=18,
        anchor="w"
    ).pack(side="left")

    e = tk.Entry(
        row,
        show=show,
        font=FONT_TEXT,
        bg=COLORS["input_bg"],
        fg=COLORS["text"],
        insertbackground=COLORS["text"],
        relief="flat",
        bd=0
    )
    e.pack(side="left", fill="x", expand=True, ipady=8, padx=(8, 0))

    # subtle border effect
    wrapper = tk.Frame(row, bg=COLORS["border"], height=1)
    wrapper.pack(fill="x", padx=(18 + 8, 0), pady=(2, 0))
    return e

def add_top_back(frame: tk.Frame, text="← Retour", command=None):
    top = tk.Frame(frame, bg=COLORS["bg"])
    top.pack(fill="x", side="top")

    tk.Button(
        top,
        text=text,
        command=command,
        bg=COLORS["bg"],
        fg=COLORS["muted"],
        activebackground=COLORS["bg"],
        activeforeground=COLORS["text"],
        relief="flat",
        font=FONT_TEXT,
        cursor="hand2"
    ).pack(side="left", padx=18, pady=14)

    return top

def apply_ttk_dark_style(widget: tk.Widget):
    """
    Minimal ttk styling for Combobox / Scrollbar.
    Call once from any screen init (safe to call many times).
    """
    root = widget.winfo_toplevel()
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(
        "TCombobox",
        fieldbackground=COLORS["card"],
        background=COLORS["card"],
        foreground=COLORS["text"],
        arrowcolor=COLORS["muted"],
        bordercolor=COLORS["border"],
        lightcolor=COLORS["border"],
        darkcolor=COLORS["border"],
        relief="flat",
        padding=6
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", COLORS["card"]), ("disabled", COLORS["card"])],
        foreground=[("readonly", COLORS["text"]), ("disabled", COLORS["muted"])],
        background=[("readonly", COLORS["card"]), ("active", COLORS["card"])]
    )

    style.configure(
        "TScrollbar",
        troughcolor=COLORS["bg"],
        background=COLORS["border"],
        bordercolor=COLORS["bg"],
        arrowcolor=COLORS["muted"]
    )

class FilterableCombobox(ttk.Combobox):
    """Combobox with type-to-filter behavior."""
    def __init__(self, master, values_source, **kwargs):
        apply_ttk_dark_style(master)
        super().__init__(master, **kwargs)
        self.values_source = list(values_source)
        self["values"] = self.values_source
        self.bind("<KeyRelease>", self._on_keyrelease)

    def _on_keyrelease(self, event):
        typed = self.get().strip().lower()
        if not typed:
            self["values"] = self.values_source
            return
        filtered = [v for v in self.values_source if typed in v.lower()]
        self["values"] = filtered


# ================= MAIN MENU =================

class MainMenu(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        section_title(self, "Système de gestion des rendez-vous médicaux")

        c = card_frame(self)

        big_button(c, "Espace Patient", lambda: app.show("PatientLogin")).pack(pady=8, fill="x")
        big_button(c, "Espace Médecin", lambda: app.show("DoctorLogin")).pack(pady=8, fill="x")
        big_button(c, "Espace Administrateur", lambda: app.show("AdminLogin")).pack(pady=8, fill="x")
        big_button(c, "Quitter", app.destroy, kind="secondary").pack(pady=(14, 8), fill="x")


# ================= ADMIN =================

class AdminLogin(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        add_top_back(self, command=lambda: app.show("MainMenu"))

        section_title(self, "Connexion Administrateur")

        c = card_frame(self)

        self.username = labeled_entry(c, "Nom d'utilisateur :")
        self.password = labeled_entry(c, "Mot de passe :", show="*")

        big_button(c, "Connexion", self.login).pack(pady=10, fill="x")

    def login(self):
        try:
            user = self.app.auth_service.login(self.username.get(), self.password.get(), "ADMIN")
            self.app.current_user = user
            self.username.delete(0, "end")
            self.password.delete(0, "end")
            self.app.show("AdminHome")
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))


class AdminHome(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        add_top_back(self, command=lambda: app.show("MainMenu"))

        section_title(self, "Espace Administrateur")

        c = card_frame(self)

        big_button(c, "Ajouter un médecin", lambda: app.show("AdminAddDoctor")).pack(pady=8, fill="x")
        big_button(c, "Supprimer un médecin", lambda: app.show("AdminDeleteDoctor"), kind="danger").pack(pady=8, fill="x")
        big_button(c, "Voir les médecins", lambda: app.show("AdminListDoctors")).pack(pady=8, fill="x")
        big_button(c, "Quitter", app.logout, kind="secondary").pack(pady=(14, 8), fill="x")


class AdminListDoctors(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        add_top_back(self, command=lambda: app.show("AdminHome"))

        section_title(self, "Liste des médecins")

        c = card_frame(self)

        self.listbox = tk.Listbox(
            c,
            width=80,
            height=12,
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            bg=COLORS["input_bg"],
            fg=COLORS["text"],
            selectbackground=COLORS["slot_active"],
            selectforeground=COLORS["text"]
        )
        self.listbox.pack(pady=10, fill="both", expand=True)

    def on_show(self):
        self.listbox.delete(0, "end")
        docs = self.app.user_repo.list_doctors()
        if not docs:
            self.listbox.insert("end", "Aucun médecin.")
            return
        for _, full_name, specialty, username in docs:
            self.listbox.insert("end", f"{full_name} — {specialty} ({username})")


class AdminAddDoctor(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        add_top_back(self, command=lambda: app.show("AdminHome"))

        section_title(self, "Ajouter un médecin")

        c = card_frame(self)

        self.full_name = labeled_entry(c, "Nom complet :")

        row = tk.Frame(c, bg=COLORS["card"])
        row.pack(pady=8, fill="x")
        tk.Label(row, text="Spécialité :", fg=COLORS["muted"], bg=COLORS["card"],
                 width=18, anchor="w", font=FONT_TEXT).pack(side="left")

        self.specialty = FilterableCombobox(row, SPECIALTIES, width=37)
        self.specialty.pack(side="left", fill="x", expand=True, padx=(8, 0))

        self.username = labeled_entry(c, "Nom d'utilisateur :")
        self.password = labeled_entry(c, "Mot de passe :", show="*")

        big_button(c, "Enregistrer", self.save).pack(pady=10, fill="x")

    def save(self):
        try:
            self.app.admin_service.add_doctor(
                self.full_name.get(),
                self.specialty.get(),
                self.username.get(),
                self.password.get()
            )
            messagebox.showinfo("OK", "Médecin ajouté.")
            self.full_name.delete(0, "end")
            self.specialty.set("")
            self.username.delete(0, "end")
            self.password.delete(0, "end")
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))


class AdminDeleteDoctor(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        add_top_back(self, command=lambda: app.show("AdminHome"))

        section_title(self, "Supprimer un médecin")

        c = card_frame(self)

        row = tk.Frame(c, bg=COLORS["card"])
        row.pack(pady=10, fill="x")
        tk.Label(row, text="Médecin :", fg=COLORS["muted"], bg=COLORS["card"],
                 width=18, anchor="w", font=FONT_TEXT).pack(side="left")

        apply_ttk_dark_style(self)
        self.combo = ttk.Combobox(row, width=45, state="readonly")
        self.combo.pack(side="left", fill="x", expand=True, padx=(8, 0))

        big_button(c, "Supprimer", self.delete, kind="danger").pack(pady=10, fill="x")

        self._doctor_map = {}

    def on_show(self):
        self._doctor_map.clear()
        docs = self.app.user_repo.list_doctors()
        labels = []
        for did, full_name, specialty, _ in docs:
            label = f"{full_name} ({specialty})"
            labels.append(label)
            self._doctor_map[label] = did
        self.combo["values"] = labels
        self.combo.set(labels[0] if labels else "")

    def delete(self):
        label = self.combo.get()
        if not label:
            messagebox.showerror("Erreur", "Veuillez sélectionner un médecin.")
            return
        if not messagebox.askyesno("Confirmation", f"Supprimer {label} ?"):
            return
        try:
            self.app.admin_service.delete_doctor(self._doctor_map[label])
            messagebox.showinfo("OK", f"{label} supprimé.")
            self.on_show()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))


# ================= PATIENT =================

class PatientLogin(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        add_top_back(self, command=lambda: app.show("MainMenu"))

        section_title(self, "Espace Patient — Connexion")

        c = card_frame(self)

        self.username = labeled_entry(c, "Nom d'utilisateur :")
        self.password = labeled_entry(c, "Mot de passe :", show="*")

        big_button(c, "Se connecter", self.login).pack(pady=10, fill="x")
        big_button(c, "Créer un compte", lambda: app.show("PatientRegister"), kind="secondary").pack(pady=6, fill="x")

    def login(self):
        try:
            user = self.app.auth_service.login(self.username.get(), self.password.get(), "PATIENT")
            self.app.current_user = user
            self.username.delete(0, "end")
            self.password.delete(0, "end")

            reminders = self.app.reminder_service.reminders_on_login(user["id"])
            if reminders:
                lines = []
                for doc_name, t, is_urgent, reason in reminders:
                    line = f"⏰ Vous avez un rendez-vous demain à {t} avec Dr {doc_name}."
                    if is_urgent:
                        line += f" (URGENT : {reason})"
                    lines.append(line)
                messagebox.showinfo("Rappel", "\n".join(lines))

            self.app.show("PatientHome")
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))


class PatientRegister(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        add_top_back(self, command=lambda: app.show("PatientLogin"))

        section_title(self, "Créer un compte Patient")

        c = card_frame(self)

        self.full_name = labeled_entry(c, "Nom complet :")
        self.username = labeled_entry(c, "Nom d'utilisateur :")
        self.password = labeled_entry(c, "Mot de passe :", show="*")

        big_button(c, "Créer mon compte", self.create).pack(pady=10, fill="x")

    def create(self):
        try:
            self.app.auth_service.register_patient(self.full_name.get(), self.username.get(), self.password.get())
            messagebox.showinfo("OK", "Compte créé avec succès.")
            self.full_name.delete(0, "end")
            self.username.delete(0, "end")
            self.password.delete(0, "end")
            self.app.show("PatientLogin")
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))


class PatientHome(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        add_top_back(self, command=lambda: app.show("MainMenu"))

        self.title = tk.Label(self, text="Espace Patient",
                              fg=COLORS["text"], bg=COLORS["bg"], font=FONT_TITLE)
        self.title.pack(pady=(18, 10))

        c = card_frame(self)

        big_button(c, "Prendre un rendez-vous", lambda: app.show("PatientBook")).pack(pady=8, fill="x")
        big_button(c, "Gérer mes rendez-vous", lambda: app.show("PatientManage")).pack(pady=8, fill="x")
        big_button(c, "Quitter", app.logout, kind="secondary").pack(pady=(14, 8), fill="x")

    def on_show(self):
        u = self.app.current_user
        if u:
            self.title.config(text=f"Espace Patient — {u['username']}")


class PatientBook(tk.Frame):
    """
    Clean 2-column layout:
    - Left: specialty/doctor/urgent/reason + actions
    - Right: calendar
    - Bottom: fixed-height scrollable slots
    """
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        add_top_back(self, command=lambda: app.show("PatientHome"))
        section_title(self, "Prendre un rendez-vous")

        apply_ttk_dark_style(self)

        # Main card
        card = tk.Frame(self, bg=COLORS["card"], bd=1,
                        highlightbackground=COLORS["border"], highlightthickness=1)
        card.pack(padx=40, pady=(0, 18), fill="both", expand=True)

        # Use grid INSIDE card for a structured layout
        card.grid_columnconfigure(0, weight=2)   # left
        card.grid_columnconfigure(1, weight=1)   # right
        card.grid_rowconfigure(1, weight=1)

        # ---------------- Top Area (2 columns) ----------------
        top = tk.Frame(card, bg=COLORS["card"])
        top.grid(row=0, column=0, columnspan=2, sticky="ew", padx=18, pady=(18, 10))
        top.grid_columnconfigure(0, weight=2)
        top.grid_columnconfigure(1, weight=1)

        # Left column (form)
        left = tk.Frame(top, bg=COLORS["card"])
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 18))

        # Right column (calendar)
        right = tk.Frame(top, bg=COLORS["card"])
        right.grid(row=0, column=1, sticky="n")

        # ---- Specialty row
        row1 = tk.Frame(left, bg=COLORS["card"])
        row1.pack(fill="x", pady=(0, 10))
        tk.Label(row1, text="Spécialité", fg=COLORS["muted"], bg=COLORS["card"],
                 font=FONT_TEXT).pack(anchor="w")
        self.spec_combo = FilterableCombobox(row1, SPECIALTIES, width=40)
        self.spec_combo.pack(fill="x", pady=(6, 0))
        self.spec_combo.bind("<<ComboboxSelected>>", lambda e: self._load_doctors_filtered())
        self.spec_combo.bind("<KeyRelease>", lambda e: self._load_doctors_filtered())

        # ---- Doctor row
        row2 = tk.Frame(left, bg=COLORS["card"])
        row2.pack(fill="x", pady=(0, 12))
        tk.Label(row2, text="Médecin", fg=COLORS["muted"], bg=COLORS["card"],
                 font=FONT_TEXT).pack(anchor="w")
        self.doctor_combo = ttk.Combobox(row2, width=40, state="readonly")
        self.doctor_combo.pack(fill="x", pady=(6, 0))
        self._doctor_map = {}

        # ---- Urgent + reason (group)
        urg_group = tk.Frame(left, bg=COLORS["card"])
        urg_group.pack(fill="x", pady=(0, 12))

        self.urgent_var = tk.IntVar(value=0)
        tk.Checkbutton(
            urg_group,
            text="Demande urgente (prioritaire)",
            variable=self.urgent_var,
            bg=COLORS["card"],
            fg=COLORS["text"],
            selectcolor=COLORS["card"],
            activebackground=COLORS["card"],
            activeforeground=COLORS["text"],
            command=self._toggle_reason
        ).pack(anchor="w")

        tk.Label(urg_group, text="Motif (obligatoire si urgent)", fg=COLORS["muted"],
                 bg=COLORS["card"], font=FONT_TEXT).pack(anchor="w", pady=(10, 0))

        self.reason_entry = tk.Entry(
            urg_group,
            state="disabled",
            bg=COLORS["input_bg"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
            bd=0
        )
        self.reason_entry.pack(fill="x", pady=(6, 0), ipady=8)

        # ---- Actions (show slots + confirm)
        actions = tk.Frame(left, bg=COLORS["card"])
        actions.pack(fill="x", pady=(6, 0))

        self.show_btn = big_button(actions, "Afficher les créneaux", self.show_slots, kind="secondary")
        self.show_btn.pack(fill="x")

        self.confirm_btn = big_button(actions, "Confirmer le rendez-vous", self.confirm, kind="primary")
        self.confirm_btn.config(state="disabled")
        self.confirm_btn.pack(fill="x", pady=(10, 0))

        # ---- Calendar (right column)
        tk.Label(right, text="Date", fg=COLORS["muted"], bg=COLORS["card"],
                 font=FONT_TEXT).pack(anchor="w")
        self.cal = Calendar(right, selectmode="day", date_pattern="yyyy-mm-dd")
        self.cal.pack(pady=(6, 0))

        # ---------------- Slots Area (full width) ----------------
        slots_container = tk.Frame(card, bg=COLORS["card"])
        slots_container.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=18, pady=(10, 18))
        slots_container.grid_rowconfigure(1, weight=1)
        slots_container.grid_columnconfigure(0, weight=1)

        tk.Label(slots_container, text="Créneaux disponibles", fg=COLORS["muted"],
                 bg=COLORS["card"], font=FONT_TEXT).grid(row=0, column=0, sticky="w", pady=(0, 8))

        # fixed-height scroll area (nice + stable)
        slots_outer = tk.Frame(slots_container, bg=COLORS["card"])
        slots_outer.grid(row=1, column=0, sticky="nsew")

        self.slots_canvas = tk.Canvas(
            slots_outer,
            bg=COLORS["card"],
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            height=160
        )
        self.slots_canvas.pack(side="left", fill="both", expand=True)

        self.slots_scroll = ttk.Scrollbar(slots_outer, orient="vertical", command=self.slots_canvas.yview)
        self.slots_scroll.pack(side="right", fill="y")
        self.slots_canvas.configure(yscrollcommand=self.slots_scroll.set)

        self.slots_frame = tk.Frame(self.slots_canvas, bg=COLORS["card"])
        self._slots_window = self.slots_canvas.create_window((0, 0), window=self.slots_frame, anchor="nw")

        def _on_inner_configure(_):
            self.slots_canvas.configure(scrollregion=self.slots_canvas.bbox("all"))

        def _on_canvas_configure(event):
            self.slots_canvas.itemconfig(self._slots_window, width=event.width)

        self.slots_frame.bind("<Configure>", _on_inner_configure)
        self.slots_canvas.bind("<Configure>", _on_canvas_configure)

        # selection state
        self.selected_time = None
        self._slot_buttons = {}

    def on_show(self):
        self.spec_combo.set("")
        self._load_doctors_filtered()
        self._clear_slots()

    def _toggle_reason(self):
        if self.urgent_var.get() == 1:
            self.reason_entry.config(state="normal")
        else:
            self.reason_entry.delete(0, "end")
            self.reason_entry.config(state="disabled")

    def _load_doctors_filtered(self):
        self._doctor_map.clear()
        all_docs = self.app.user_repo.list_doctors()

        wanted = self.spec_combo.get().strip().lower()
        docs = all_docs
        if wanted:
            docs = [d for d in all_docs if wanted in (d[2] or "").lower()]

        labels = []
        for did, full_name, specialty, _ in docs:
            label = f"{full_name} ({specialty})"
            labels.append(label)
            self._doctor_map[label] = did

        self.doctor_combo["values"] = labels
        self.doctor_combo.set(labels[0] if labels else "")

    def _clear_slots(self):
        for w in self.slots_frame.winfo_children():
            w.destroy()
        self.selected_time = None
        self._slot_buttons.clear()
        self.confirm_btn.config(state="disabled")
        self.slots_canvas.yview_moveto(0)

    def _select_time(self, t: str):
        self.selected_time = t
        for tt, btn in self._slot_buttons.items():
            if tt == t:
                btn.config(bg=COLORS["primary"], fg="white", activebackground=COLORS["primary_hover"])
            else:
                btn.config(bg=COLORS["slot_bg"], fg=COLORS["text"], activebackground=COLORS["slot_active"])
        self.confirm_btn.config(state="normal")

    def show_slots(self):
        self._clear_slots()
        label = self.doctor_combo.get()
        if not label:
            messagebox.showerror("Erreur", "Veuillez sélectionner un médecin.")
            return

        d = parse_date_str(self.cal.get_date())
        if d < datetime.now().date():
            messagebox.showerror("Erreur", "Vous ne pouvez pas réserver une date passée.")
            return

        doctor_id = self._doctor_map[label]
        try:
            times = self.app.appt_service.available_times(doctor_id, d)
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
            return

        times = [t for t in times if not _is_past_slot(d, t)]
        if not times:
            messagebox.showinfo("Info", "Aucun créneau disponible.")
            return

        # wrap grid: looks clean, compact
        cols = 8
        for i, t in enumerate(times):
            r = i // cols
            c = i % cols
            btn = tk.Button(
                self.slots_frame,
                text=t,
                bg=COLORS["slot_bg"],
                fg=COLORS["text"],
                activebackground=COLORS["slot_active"],
                activeforeground=COLORS["text"],
                relief="flat",
                bd=0,
                padx=10,
                pady=10,
                cursor="hand2",
                command=lambda tt=t: self._select_time(tt)
            )
            btn.grid(row=r, column=c, padx=6, pady=6, sticky="ew")
            self._slot_buttons[t] = btn

        for c in range(cols):
            self.slots_frame.grid_columnconfigure(c, weight=1)

        self.slots_canvas.yview_moveto(0)

    def confirm(self):
        label = self.doctor_combo.get()
        if not label:
            messagebox.showerror("Erreur", "Veuillez sélectionner un médecin.")
            return
        if not self.selected_time:
            messagebox.showerror("Erreur", "Veuillez sélectionner un créneau.")
            return

        doctor_id = self._doctor_map[label]
        d = parse_date_str(self.cal.get_date())

        if _is_past_slot(d, self.selected_time):
            messagebox.showerror("Erreur", "Ce créneau est déjà passé.")
            return

        urgent = self.urgent_var.get() == 1
        reason = self.reason_entry.get().strip()

        if urgent and not reason:
            messagebox.showerror("Erreur", "Veuillez saisir un motif pour une demande urgente.")
            return

        try:
            self.app.appt_service.book(
                patient_id=self.app.current_user["id"],
                doctor_id=doctor_id,
                d=d,
                t=self.selected_time,
                urgent=urgent,
                reason=reason
            )
            messagebox.showinfo("OK", f"Rendez-vous confirmé le {d.isoformat()} à {self.selected_time}.")
            self.app.show("PatientHome")
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))



class PatientManage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        add_top_back(self, command=lambda: app.show("PatientHome"))

        section_title(self, "Gérer mes rendez-vous")

        c = card_frame(self)

        row = tk.Frame(c, bg=COLORS["card"])
        row.pack(pady=(14, 10), fill="x")
        tk.Label(row, text="Rendez-vous :", fg=COLORS["muted"], bg=COLORS["card"],
                 width=18, anchor="w", font=FONT_TEXT).pack(side="left")

        apply_ttk_dark_style(self)
        self.combo = ttk.Combobox(row, width=50, state="readonly")
        self.combo.pack(side="left", fill="x", expand=True, padx=(8, 0))

        btns = tk.Frame(c, bg=COLORS["card"])
        btns.pack(pady=(10, 16), fill="x")
        big_button(btns, "Annuler", self.cancel, kind="danger").pack(side="left", padx=8)
        big_button(btns, "Modifier", self.modify, kind="secondary").pack(side="left", padx=8)

        self._appt_map = {}

    def on_show(self):
        self.refresh()

    def refresh(self):
        self._appt_map.clear()
        appts = self.app.appt_repo.list_for_patient(self.app.current_user["id"])
        labels = []
        for appt_id, doc_name, d, t, is_urgent, _reason in appts:
            label = f"{doc_name} — {d} {t}"
            if is_urgent:
                label += " (PRIO)"
            labels.append(label)
            self._appt_map[label] = (appt_id, d)
        self.combo["values"] = labels
        self.combo.set(labels[0] if labels else "")

    def cancel(self):
        label = self.combo.get()
        if not label:
            messagebox.showinfo("Info", "Aucun rendez-vous.")
            return
        appt_id, d = self._appt_map[label]
        if not messagebox.askyesno("Confirmation", "Confirmer l’annulation ?"):
            return
        try:
            self.app.appt_service.cancel(appt_id, d)
            messagebox.showinfo("OK", "Rendez-vous annulé.")
            self.refresh()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def modify(self):
        label = self.combo.get()
        if not label:
            messagebox.showinfo("Info", "Aucun rendez-vous.")
            return
        appt_id, _ = self._appt_map[label]
        self.app.frames["PatientModify"].set_context(appt_id, label)
        self.app.show("PatientModify")


class PatientModify(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        add_top_back(self, command=lambda: app.show("PatientManage"))

        section_title(self, "Modifier le rendez-vous")

        c = card_frame(self)

        self.info = tk.Label(c, text="", fg=COLORS["muted"], bg=COLORS["card"], font=FONT_TEXT)
        self.info.pack(pady=(10, 6))

        self.cal = Calendar(c, selectmode="day", date_pattern="yyyy-mm-dd")
        self.cal.pack(pady=8)

        big_button(c, "Afficher créneaux", self.show_slots, kind="secondary").pack(pady=10, fill="x")

        self.slots_frame = tk.Frame(c, bg=COLORS["card"])
        self.slots_frame.pack(pady=4, fill="x")

        self.selected_time = None
        self._slot_buttons = {}

        self.save_btn = big_button(c, "Enregistrer la modification", self.save)
        self.save_btn.config(state="disabled")
        self.save_btn.pack(pady=(10, 14), fill="x")

        self.appt_id = None
        self.doctor_id = None

    def set_context(self, appt_id: int, label_text: str):
        self.appt_id = appt_id
        self.doctor_id = self.app.appt_repo.get_doctor_id_for_appointment(appt_id)
        self.info.config(text=f"Sélection : {label_text}")
        self._clear_slots()

    def _clear_slots(self):
        for w in self.slots_frame.winfo_children():
            w.destroy()
        self.selected_time = None
        self._slot_buttons.clear()
        self.save_btn.config(state="disabled")

    def _select_time(self, t: str):
        self.selected_time = t
        for tt, btn in self._slot_buttons.items():
            if tt == t:
                btn.config(bg=COLORS["primary"], fg="white", activebackground=COLORS["primary_hover"])
            else:
                btn.config(bg=COLORS["slot_bg"], fg=COLORS["text"], activebackground=COLORS["slot_active"])
        self.save_btn.config(state="normal")

    def show_slots(self):
        self._clear_slots()
        if not self.doctor_id:
            messagebox.showerror("Erreur", "Rendez-vous introuvable.")
            return
        d = parse_date_str(self.cal.get_date())

        if d < datetime.now().date():
            messagebox.showerror("Erreur", "Vous ne pouvez pas choisir une date passée.")
            return

        try:
            times = self.app.appt_service.available_times(self.doctor_id, d)
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
            return

        times = [t for t in times if not _is_past_slot(d, t)]

        if not times:
            messagebox.showinfo("Info", "Aucun créneau disponible.")
            return

        cols = 10
        for i, t in enumerate(times):
            r = i // cols
            c = i % cols
            btn = tk.Button(
                self.slots_frame,
                text=t,
                width=7,
                bg=COLORS["slot_bg"],
                fg=COLORS["text"],
                activebackground=COLORS["slot_active"],
                activeforeground=COLORS["text"],
                relief="flat",
                bd=0,
                padx=6,
                pady=10,
                cursor="hand2",
                command=lambda tt=t: self._select_time(tt)
            )
            btn.grid(row=r, column=c, padx=6, pady=6, sticky="ew")
            self._slot_buttons[t] = btn

        for c in range(cols):
            self.slots_frame.grid_columnconfigure(c, weight=1)

    def save(self):
        d = parse_date_str(self.cal.get_date())
        if not self.selected_time:
            messagebox.showerror("Erreur", "Veuillez sélectionner un créneau.")
            return
        if _is_past_slot(d, self.selected_time):
            messagebox.showerror("Erreur", "Ce créneau est déjà passé.")
            return
        try:
            self.app.appt_service.modify(self.appt_id, self.doctor_id, d, self.selected_time)
            messagebox.showinfo("OK", f"Déplacé au {d.isoformat()} à {self.selected_time}.")
            self.app.show("PatientManage")
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))


# ================= DOCTOR =================

class DoctorLogin(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        add_top_back(self, command=lambda: app.show("MainMenu"))

        section_title(self, "Connexion Médecin")

        c = card_frame(self)

        self.username = labeled_entry(c, "Nom d'utilisateur :")
        self.password = labeled_entry(c, "Mot de passe :", show="*")

        big_button(c, "Connexion", self.login).pack(pady=10, fill="x")

    def login(self):
        try:
            user = self.app.auth_service.login(self.username.get(), self.password.get(), "DOCTOR")
            self.app.current_user = user
            self.username.delete(0, "end")
            self.password.delete(0, "end")
            self.app.show("DoctorHome")
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))


class DoctorHome(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        add_top_back(self, command=lambda: app.show("MainMenu"))

        self.title = tk.Label(self, text="Espace Médecin",
                              fg=COLORS["text"], bg=COLORS["bg"], font=FONT_TITLE)
        self.title.pack(pady=(18, 10))

        c = card_frame(self)

        big_button(c, "Créer des créneaux disponibles", lambda: app.show("DoctorCreateSlots")).pack(pady=8, fill="x")
        big_button(c, "Consulter mon emploi du temps", lambda: app.show("DoctorSchedule")).pack(pady=8, fill="x")
        big_button(c, "Quitter", app.logout, kind="secondary").pack(pady=(14, 8), fill="x")

    def on_show(self):
        u = self.app.current_user
        if u:
            self.title.config(text=f"Espace Médecin — Dr {u['full_name']}")


class DoctorCreateSlots(tk.Frame):
    """
    Doctor creates available time slots for a given day.
    Past-time filtering is applied ONLY for today (not future dates).
    """
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        add_top_back(self, command=lambda: app.show("DoctorHome"))

        tk.Label(self, text="Créer des créneaux",
                 fg=COLORS["text"], bg=COLORS["bg"], font=FONT_TITLE).pack(pady=(6, 10))

        c = tk.Frame(self, bg=COLORS["card"], bd=1, highlightbackground=COLORS["border"], highlightthickness=1)
        c.pack(padx=40, pady=(0, 14), fill="both", expand=True)
        c.grid_columnconfigure(0, weight=1)
        c.grid_rowconfigure(2, weight=1)

        # Calendar
        self.cal = Calendar(c, selectmode="day", date_pattern="yyyy-mm-dd")
        self.cal.grid(row=0, column=0, pady=(16, 10))

        tk.Label(c, text="Sélectionnez les créneaux :", fg=COLORS["muted"],
                 bg=COLORS["card"], font=FONT_TEXT).grid(row=1, column=0, pady=(6, 6))

        # Scrollable slots area
        self.vars = {}
        self.checkbuttons = {}

        slots_outer = tk.Frame(c, bg=COLORS["card"])
        slots_outer.grid(row=2, column=0, sticky="nsew", padx=14, pady=6)
        slots_outer.grid_rowconfigure(0, weight=1)
        slots_outer.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(slots_outer, bg=COLORS["card"], highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(slots_outer, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)

        inner = tk.Frame(canvas, bg=COLORS["card"])
        canvas.create_window((0, 0), window=inner, anchor="nw")

        def _on_configure(_):
            canvas.configure(scrollregion=canvas.bbox("all"))

        inner.bind("<Configure>", _on_configure)

        # Build checkboxes ONCE (they will be enabled/disabled later)
        for i, t in enumerate(SLOT_TIMES):
            v = tk.IntVar(value=0)
            self.vars[t] = v

            cb = tk.Checkbutton(
                inner,
                text=t,
                variable=v,
                bg=COLORS["card"],
                fg=COLORS["text"],
                selectcolor=COLORS["card"],
                activebackground=COLORS["card"],
                activeforeground=COLORS["text"]
            )
            cb.grid(row=i // 8, column=i % 8, padx=12, pady=8, sticky="w")
            self.checkbuttons[t] = cb

        # Bottom buttons
        bottom = tk.Frame(c, bg=COLORS["card"])
        bottom.grid(row=3, column=0, sticky="ew", pady=(10, 16), padx=14)

        big_button(bottom, "Tout sélectionner", self.select_all, kind="secondary").pack(side="left", padx=8)
        big_button(bottom, "Tout désélectionner", self.clear_all, kind="secondary").pack(side="left", padx=8)
        big_button(bottom, "Créer les créneaux", self.create).pack(side="right", padx=8)

        # ✅ Update enable/disable when date changes
        self.cal.bind("<<CalendarSelected>>", lambda e: self._refresh_disabled_slots())

        # Initial refresh
        self._refresh_disabled_slots()

    def _refresh_disabled_slots(self):
        """Enable/disable checkboxes based on selected date."""
        d = parse_date_str(self.cal.get_date())

        for t, cb in self.checkbuttons.items():
            if d < date.today():
                # past day -> disable all
                cb.config(state="disabled", fg=COLORS["muted"])
                self.vars[t].set(0)
            elif d == date.today() and _is_past_slot(d, t):
                # today -> disable only past times
                cb.config(state="disabled", fg=COLORS["muted"])
                self.vars[t].set(0)
            else:
                # future day OR valid time today
                cb.config(state="normal", fg=COLORS["text"])

    def select_all(self):
        d = parse_date_str(self.cal.get_date())
        for t, v in self.vars.items():
            if d < date.today():
                continue
            if d == date.today() and _is_past_slot(d, t):
                continue
            v.set(1)

    def clear_all(self):
        for v in self.vars.values():
            v.set(0)

    def create(self):
        d = parse_date_str(self.cal.get_date())

        if d < date.today():
            messagebox.showerror("Erreur", "Impossible de créer des créneaux sur une date passée.")
            return

        selected = []
        for t, v in self.vars.items():
            if v.get() == 1:
                # Only block past time slots if it's today
                if d == date.today() and _is_past_slot(d, t):
                    continue
                selected.append(t)

        if not selected:
            messagebox.showinfo("Info", "Veuillez sélectionner au moins un créneau valide.")
            return

        try:
            self.app.doctor_service.create_day_slots(self.app.current_user["id"], d, selected)
            messagebox.showinfo("OK", f"Créneaux créés pour {d.isoformat()}.")
            self.clear_all()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))


class DoctorSchedule(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        add_top_back(self, command=lambda: app.show("DoctorHome"))

        section_title(self, "Emploi du temps")

        c = card_frame(self)
        self.listbox = tk.Listbox(
            c,
            width=95,
            height=14,
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            bg=COLORS["input_bg"],
            fg=COLORS["text"],
            selectbackground=COLORS["slot_active"],
            selectforeground=COLORS["text"]
        )
        self.listbox.pack(pady=10, fill="both", expand=True)

    def on_show(self):
        self.listbox.delete(0, "end")
        rows = self.app.doctor_service.list_schedule(self.app.current_user["id"])
        if not rows:
            self.listbox.insert("end", "Aucun rendez-vous.")
            return
        for _, d, t, patient_name, is_urgent, reason in rows:
            if is_urgent:
                self.listbox.insert("end", f"{d} {t} — {patient_name} (PRIO) | Motif : {reason}")
            else:
                self.listbox.insert("end", f"{d} {t} — {patient_name}")


# ---------------- Builder ----------------

def build_screens(container, app):
    frames = {}
    classes = [
        MainMenu,
        AdminLogin, AdminHome, AdminAddDoctor, AdminDeleteDoctor, AdminListDoctors,
        PatientLogin, PatientRegister, PatientHome, PatientBook, PatientManage, PatientModify,
        DoctorLogin, DoctorHome, DoctorCreateSlots, DoctorSchedule,
    ]
    for C in classes:
        f = C(container, app)
        frames[C.__name__] = f
        f.grid(row=0, column=0, sticky="nsew")
    return frames