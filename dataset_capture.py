import cv2
import os

# Load Haar Cascade
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Student name input
student_name = input("Enter Student Name: ")

# Folder path
path = f"images/student_photos/{student_name}"

if not os.path.exists(path):
    os.makedirs(path)

# Mac M2 backend
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

if not cap.isOpened():
    print("Camera not working")
    exit()

count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1
        face = frame[y:y+h, x:x+w]

        cv2.imwrite(f"{path}/{count}.jpg", face)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 3)
        cv2.putText(frame, f"Images Captured: {count}", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.imshow("Dataset Capture - Press Q to Exit", frame)

    if cv2.waitKey(1) & 0xFF == ord('q') or count == 100:
        break

cap.release()
cv2.destroyAllWindows()

print("Dataset Collection Completed!")