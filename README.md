# Medical Appointment Management System  
## Health Systems Project

### Overview
This project is a desktop-based Medical Appointment Management System developed using Python, Tkinter, and SQLite.  
The system allows administrators, doctors, and patients to manage medical appointments through a structured and role-based interface.

---

### Objectives
- Implement role-based access (Admin, Doctor, Patient)
- Prevent double booking of time slots
- Block past dates and expired time slots
- Apply clean layered architecture (GUI, Services, Repository, Database)
- Ensure data integrity and validation

---

### System Architecture

The application follows a layered design:

- **GUI Layer** → Tkinter user interface  
- **Service Layer** → Business logic and validation  
- **Repository Layer** → Database operations  
- **Database** → SQLite  

---

### Main Functionalities

**Patient**
- Register and login
- Book appointment
- Modify appointment
- Cancel appointment
- Mark appointment as urgent (with reason)

**Doctor**
- Login
- Create available time slots
- View schedule

**Administrator**
- Add doctors
- Delete doctors
- View doctor list

---

### Business Rules

- Appointments cannot be booked in the past.
- Past time slots (same day) are automatically blocked.
- Time slots cannot be double-booked.
- During modification, the system excludes the current appointment from availability checks.
- Urgent appointments require a minimum reason length.
- Past appointments cannot be cancelled.

---

### Technologies Used

- Python 3.x
- Tkinter
- SQLite
- tkcalendar

---

### Installation

Install dependency:
pip install tkcalendar


Run the application:
python main.py



---

### Conclusion

This project demonstrates the implementation of a structured healthcare scheduling system using a layered architecture and real-world validation rules.  
It ensures data consistency, role separation, and appointment integrity while maintaining a clean and professional interface.
