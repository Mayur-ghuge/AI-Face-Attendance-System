import customtkinter as ctk
import subprocess
import sys
import os
from datetime import datetime
from PIL import Image
from openpyxl import load_workbook

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("AI Face Recognition Attendance System")
app.geometry("900x550")
app.resizable(False, False)

# ---------- Sidebar ----------
sidebar = ctk.CTkFrame(app, width=220, corner_radius=0)
sidebar.pack(side="left", fill="y")

logo = ctk.CTkLabel(
    sidebar,
    text="🎓 Face AI",
    font=("Arial", 22, "bold")
)
logo.pack(pady=20)

# Profile Image (Put any image named profile.png in project folder)
if os.path.exists("profile.png"):
    img = ctk.CTkImage(Image.open("profile.png"), size=(100, 100))
    profile_label = ctk.CTkLabel(sidebar, image=img, text="")
    profile_label.pack(pady=10)

admin_label = ctk.CTkLabel(sidebar, text="Admin", font=("Arial", 14))
admin_label.pack(pady=5)


# ---------- Main Frame ----------
main_frame = ctk.CTkFrame(app, corner_radius=20)
main_frame.pack(side="right", expand=True, fill="both", padx=20, pady=20)

title = ctk.CTkLabel(
    main_frame,
    text="Dashboard",
    font=("Arial", 28, "bold")
)
title.pack(pady=10)

# ---------- Live Date & Time ----------
time_label = ctk.CTkLabel(main_frame, font=("Arial", 14))
time_label.pack(pady=5)

def update_time():
    now = datetime.now().strftime("%A, %d %B %Y  |  %H:%M:%S")
    time_label.configure(text=now)
    app.after(1000, update_time)

update_time()

# ---------- Attendance Stats ----------
stats_label = ctk.CTkLabel(main_frame, font=("Arial", 16, "bold"))
stats_label.pack(pady=10)

def update_stats():
    if os.path.exists("attendance.xlsx"):
        wb = load_workbook("attendance.xlsx")
        ws = wb.active
        total = ws.max_row - 1
        stats_label.configure(text=f"📊 Total Attendance Records: {total}")
    else:
        stats_label.configure(text="📊 Total Attendance Records: 0")

update_stats()


# ---------- Buttons ----------
def open_student():
    subprocess.run([sys.executable, "dataset_capture.py"])
    update_stats()

def open_recognition():
    subprocess.run([sys.executable, "face_recognition.py"])
    update_stats()

def open_attendance():
    if os.path.exists("attendance.xlsx"):
        subprocess.run(["open", "attendance.xlsx"])


btn1 = ctk.CTkButton(
    main_frame,
    text="📸 Capture Dataset",
    command=open_student,
    width=350,
    height=50
)
btn1.pack(pady=15)

btn2 = ctk.CTkButton(
    main_frame,
    text="🧠 Start Recognition",
    command=open_recognition,
    width=350,
    height=50
)
btn2.pack(pady=15)

btn3 = ctk.CTkButton(
    main_frame,
    text="📊 View Attendance",
    command=open_attendance,
    width=350,
    height=50
)
btn3.pack(pady=15)

btn4 = ctk.CTkButton(
    main_frame,
    text="🚪 Logout",
    command=app.destroy,
    width=350,
    height=50,
    fg_color="red",
    hover_color="darkred"
)
btn4.pack(pady=25)

app.mainloop()