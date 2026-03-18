import cv2
import os
import sys

def capture_images(name):

    path = f"images/student_photos/{name}"
    os.makedirs(path, exist_ok=True)

    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Camera not opening")
        return

    count = 0
    print("📸 Camera Started...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = frame[y:y+h, x:x+w]
            face = cv2.resize(face, (224, 224))

            count += 1
            cv2.imwrite(f"{path}/{count}.jpg", face)

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(frame, f"Captured: {count}/30", (10,30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        cv2.imshow("Capturing Dataset", frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or count >= 30:
            break

    cap.release()
    cv2.destroyAllWindows()
    print("✅ Capture Completed")


# 🔥 DIRECT RUN
if __name__ == "__main__":
    if len(sys.argv) > 1:
        name = sys.argv[1]
        capture_images(name)
    else:
        print("Usage: python dataset_capture.py <name>")