import customtkinter as ctk
from tkinter import messagebox
import subprocess
import sys

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Login - AI Face Attendance System")
app.geometry("500x450")
app.resizable(False, False)

# Background Frame
frame = ctk.CTkFrame(app, corner_radius=20)
frame.pack(pady=60, padx=60, fill="both", expand=True)

title = ctk.CTkLabel(
    frame,
    text="Welcome 👋",
    font=("Arial", 28, "bold")
)
title.pack(pady=20)

subtitle = ctk.CTkLabel(
    frame,
    text="Login to continue",
    font=("Arial", 14)
)
subtitle.pack(pady=5)

username_entry = ctk.CTkEntry(
    frame,
    placeholder_text="Username",
    width=250,
    height=40
)
username_entry.pack(pady=10)

password_entry = ctk.CTkEntry(
    frame,
    placeholder_text="Password",
    show="*",
    width=250,
    height=40
)
password_entry.pack(pady=10)


def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "1234":
        app.destroy()
        subprocess.run([sys.executable, "main.py"])
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")


login_btn = ctk.CTkButton(
    frame,
    text="Login",
    command=login,
    width=200,
    height=40
)
login_btn.pack(pady=20)

app.mainloop()