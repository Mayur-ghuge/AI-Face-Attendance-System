import cv2
import os
from deepface import DeepFace
from attendance import mark_attendance

# Load Haar Cascade
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Dataset path
dataset_path = "images/student_photos"

# Camera (Mac M2)
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

# Track recognized people
marked = set()

# Frame counter for skipping
frame_count = 0

print("🚀 Face Recognition Started...")

while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # 🔥 Skip frames (performance boost)
    if frame_count % 5 != 0:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:

        face = frame[y:y+h, x:x+w]

        # 🔥 Resize (faster processing)
        face = cv2.resize(face, (224, 224))

        temp_path = "temp.jpg"
        cv2.imwrite(temp_path, face)

        recognized = "Unknown"

        try:
            result = DeepFace.find(
                img_path=temp_path,
                db_path=dataset_path,
                enforce_detection=False
            )

            # 🔥 If match found
            if len(result) > 0 and len(result[0]) > 0:

                identity = result[0].iloc[0]["identity"]
                recognized = identity.split("/")[-2]

                # 🔥 Avoid duplicate attendance
                if recognized not in marked:
                    mark_attendance(recognized)
                    marked.add(recognized)
                    print(f"✅ Attendance Marked: {recognized}")

        except Exception as e:
            print("Error:", e)

        # 🔥 UI color
        color = (0, 255, 0) if recognized != "Unknown" else (0, 0, 255)

        # Draw rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

        # Show name
        cv2.putText(frame, recognized, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow("Face Recognition - Press Q to Exit", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

# Cleanup temp file
if os.path.exists("temp.jpg"):
    os.remove("temp.jpg")

print("🛑 System Closed.")