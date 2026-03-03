import cv2
import os
from deepface import DeepFace
from attendance import mark_attendance

# Load Haar Cascade
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Mac M2 Camera Backend
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

dataset_path = "images/student_photos"

if not cap.isOpened():
    print("Camera not working")
    exit()

print("Starting Face Recognition...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]
        temp_image = "temp.jpg"
        cv2.imwrite(temp_image, face)

        recognized = "Unknown"

        # Loop through each student folder
        for student in os.listdir(dataset_path):
            student_folder = os.path.join(dataset_path, student)

            if not os.path.isdir(student_folder):
                continue

            for img in os.listdir(student_folder):
                img_path = os.path.join(student_folder, img)

                try:
                    result = DeepFace.verify(
                        temp_image,
                        img_path,
                        enforce_detection=False
                    )

                    if result["verified"]:
                        recognized = student
                        mark_attendance(student)   # ✅ Auto mark attendance
                        break

                except:
                    pass

            if recognized != "Unknown":
                break

        # Draw Rectangle
        if recognized == "Unknown":
            color = (0, 0, 255)  # Red
        else:
            color = (0, 255, 0)  # Green

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 3)
        cv2.putText(frame, recognized, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow("Face Recognition - Press Q to Exit", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Remove temp image if exists
if os.path.exists("temp.jpg"):
    os.remove("temp.jpg")

print("System Closed.")