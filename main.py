import customtkinter as ctk
import subprocess
import sys
import os
from datetime import datetime
from openpyxl import load_workbook
from PIL import Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("FACE AI - Attendance System")
app.state("zoomed")

# Deep dark background
app.configure(fg_color="#0f172a")

# =========================
# Sidebar
# =========================

sidebar = ctk.CTkFrame(app, width=260, corner_radius=0, fg_color="#020617")
sidebar.pack(side="left", fill="y")

logo = ctk.CTkLabel(
    sidebar,
    text="FACE AI",
    font=("Arial",30,"bold")
)
logo.pack(pady=(30,10))

# Profile Image
if os.path.exists("profile.png"):
    img = ctk.CTkImage(Image.open("profile.png"), size=(120,120))
    profile = ctk.CTkLabel(sidebar, image=img, text="")
    profile.pack(pady=10)

admin = ctk.CTkLabel(
    sidebar,
    text="Mayur",
    font=("Arial",18,"bold")
)
admin.pack(pady=(5,30))

# =========================
# Sidebar Buttons
# =========================

def capture_dataset():
    subprocess.Popen([sys.executable,"dataset_capture.py"])


def start_recognition():
    subprocess.Popen([sys.executable,"face_recognition.py"])


def view_attendance():
    if os.path.exists("attendance.xlsx"):
        subprocess.Popen(["open","attendance.xlsx"])


def exit_app():
    app.destroy()


btn1 = ctk.CTkButton(
    sidebar,
    text="📸 Capture Dataset",
    command=capture_dataset,
    width=200,
    height=45
)
btn1.pack(pady=10)

btn2 = ctk.CTkButton(
    sidebar,
    text="🧠 Start Recognition",
    command=start_recognition,
    width=200,
    height=45
)
btn2.pack(pady=10)

btn3 = ctk.CTkButton(
    sidebar,
    text="📊 View Attendance",
    command=view_attendance,
    width=200,
    height=45
)
btn3.pack(pady=10)

btn4 = ctk.CTkButton(
    sidebar,
    text="🚪 Exit",
    command=exit_app,
    fg_color="red",
    hover_color="#8b0000",
    width=200,
    height=45
)
btn4.pack(pady=30)

# =========================
# Main Dashboard
# =========================

main = ctk.CTkFrame(app, fg_color="#0f172a")
main.pack(side="right", expand=True, fill="both", padx=40, pady=40)

title = ctk.CTkLabel(
    main,
    text="Dashboard",
    font=("Arial",40,"bold")
)
title.pack(pady=10)

# =========================
# Live Time
# =========================

time_label = ctk.CTkLabel(main,font=("Arial",18))
time_label.pack()

def update_time():
    now = datetime.now().strftime("%A, %d %B %Y | %H:%M:%S")
    time_label.configure(text=now)
    app.after(1000, update_time)

update_time()

# =========================
# Statistics Cards
# =========================

stats_frame = ctk.CTkFrame(main, fg_color="#0f172a")
stats_frame.pack(pady=50)

total_card = ctk.CTkFrame(stats_frame,width=260,height=150,fg_color="#1e293b")
total_card.grid(row=0,column=0,padx=25)

present_card = ctk.CTkFrame(stats_frame,width=260,height=150,fg_color="#1e293b")
present_card.grid(row=0,column=1,padx=25)

absent_card = ctk.CTkFrame(stats_frame,width=260,height=150,fg_color="#1e293b")
absent_card.grid(row=0,column=2,padx=25)

total_label = ctk.CTkLabel(total_card,text="Total Students",font=("Arial",18))
total_label.pack(pady=10)

present_label = ctk.CTkLabel(present_card,text="Present Today",font=("Arial",18))
present_label.pack(pady=10)

absent_label = ctk.CTkLabel(absent_card,text="Absent Today",font=("Arial",18))
absent_label.pack(pady=10)

total_value = ctk.CTkLabel(total_card,font=("Arial",36,"bold"))
total_value.pack()

present_value = ctk.CTkLabel(present_card,font=("Arial",36,"bold"))
present_value.pack()

absent_value = ctk.CTkLabel(absent_card,font=("Arial",36,"bold"))
absent_value.pack()

# =========================
# Attendance Table
# =========================

table_frame = ctk.CTkFrame(main, fg_color="#1e293b")
table_frame.pack(pady=20)

table_title = ctk.CTkLabel(
    table_frame,
    text="Today's Attendance",
    font=("Arial",22,"bold")
)
table_title.pack(pady=10)

table_box = ctk.CTkTextbox(
    table_frame,
    width=750,
    height=230
)
table_box.pack()

# =========================
# Data Paths
# =========================

DATASET = "images/student_photos"
ATTENDANCE = "attendance.xlsx"

# =========================
# Update Stats
# =========================

def update_stats():

    total_students = 0
    present_today = 0

    today = datetime.now().strftime("%d/%m/%Y")

    table_box.delete("1.0","end")

    if os.path.exists(DATASET):
        total_students = len(os.listdir(DATASET))

    if os.path.exists(ATTENDANCE):

        wb = load_workbook(ATTENDANCE)
        ws = wb.active

        for row in ws.iter_rows(min_row=2, values_only=True):

            name = row[0]
            date = row[1]
            time = row[2]

            if date == today:

                present_today += 1
                table_box.insert("end",f"{name}   |   {time}\n")

    absent_today = max(total_students-present_today,0)

    total_value.configure(text=total_students)
    present_value.configure(text=present_today)
    absent_value.configure(text=absent_today)

update_stats()

app.mainloop()