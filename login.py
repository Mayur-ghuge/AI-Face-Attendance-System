import customtkinter as ctk
from tkinter import messagebox
import subprocess
import sys

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("FACE AI - Login")
app.state("zoomed")


# -------------------------
# LOGIN FUNCTION
# -------------------------

def login():

    username = username_entry.get()
    password = password_entry.get()

    if username == "mayur" and password == "1234":

        subprocess.Popen([sys.executable, "main.py"])
        app.destroy()

    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")


# -------------------------
# BACKGROUND FRAME
# -------------------------

background = ctk.CTkFrame(app, fg_color="#0f172a")
background.pack(fill="both", expand=True)


# -------------------------
# TITLE
# -------------------------

title = ctk.CTkLabel(
    background,
    text="🤖 FACE AI",
    font=("Arial", 48, "bold"),
    text_color="#38bdf8"
)
title.pack(pady=(80,10))


subtitle = ctk.CTkLabel(
    background,
    text="Face Recognition Attendance System",
    font=("Arial",18),
    text_color="gray"
)
subtitle.pack(pady=(0,40))


# -------------------------
# LOGIN CARD
# -------------------------

frame = ctk.CTkFrame(
    background,
    corner_radius=20,
    width=420,
    height=350,
    fg_color="#1e293b"
)
frame.pack(pady=20)

frame.pack_propagate(False)


login_title = ctk.CTkLabel(
    frame,
    text="Admin Login",
    font=("Arial",24,"bold")
)
login_title.pack(pady=(30,20))


# username
username_entry = ctk.CTkEntry(
    frame,
    placeholder_text="Username",
    width=260,
    height=40,
    corner_radius=10
)
username_entry.pack(pady=10)


# password
password_entry = ctk.CTkEntry(
    frame,
    placeholder_text="Password",
    show="*",
    width=260,
    height=40,
    corner_radius=10
)
password_entry.pack(pady=10)


# login button
login_btn = ctk.CTkButton(
    frame,
    text="Login",
    width=220,
    height=45,
    corner_radius=12,
    command=login
)
login_btn.pack(pady=25)


# -------------------------
# FOOTER
# -------------------------

footer = ctk.CTkLabel(
    background,
    text="AI Powered Attendance System | Developed by Mayur",
    font=("Arial",12),
    text_color="gray"
)
footer.pack(side="bottom", pady=20)


# ENTER key login
app.bind("<Return>", lambda event: login())

app.mainloop()