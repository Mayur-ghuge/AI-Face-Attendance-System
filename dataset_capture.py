import customtkinter as ctk
import cv2
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Capture Dataset")
app.geometry("400x250")

def capture():

    name = name_entry.get()

    if name == "":
        return

    path = f"images/student_photos/{name}"

    if not os.path.exists(path):
        os.makedirs(path)

    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

    count = 0

    while True:

        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray,1.3,5)

        for (x,y,w,h) in faces:

            count += 1

            face = frame[y:y+h,x:x+w]

            cv2.imwrite(f"{path}/{count}.jpg", face)

            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        cv2.imshow("Capturing Dataset",frame)

        if cv2.waitKey(1) == 13 or count == 100:
            break

    cap.release()
    cv2.destroyAllWindows()
    app.destroy()


label = ctk.CTkLabel(app,text="Enter Student Name",font=("Arial",16))
label.pack(pady=20)

name_entry = ctk.CTkEntry(app,width=220)
name_entry.pack(pady=10)

btn = ctk.CTkButton(app,text="Start Capture",command=capture)
btn.pack(pady=20)

app.mainloop()