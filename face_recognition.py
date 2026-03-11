import cv2
import os
from deepface import DeepFace
from attendance import mark_attendance

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

dataset_path = "images/student_photos"

cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

marked = set()

while True:

    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray,1.3,5)

    for (x,y,w,h) in faces:

        face = frame[y:y+h, x:x+w]

        temp = "temp.jpg"
        cv2.imwrite(temp, face)

        recognized = "Unknown"

        try:

            result = DeepFace.find(
                img_path=temp,
                db_path=dataset_path,
                enforce_detection=False
            )

            if len(result[0]) > 0:

                identity = result[0].iloc[0]["identity"]

                recognized = identity.split("/")[-2]

                if recognized not in marked:

                    mark_attendance(recognized)
                    marked.add(recognized)

                    print("Attendance Marked:",recognized)

                    # SHOW MESSAGE
                    cv2.putText(frame,f"{recognized} Marked",(50,50),
                                cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

                    cv2.imshow("Face Recognition",frame)

                    cv2.waitKey(2000)

                    cap.release()
                    cv2.destroyAllWindows()

                    os.remove(temp)

                    exit()

        except:
            pass

        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        cv2.putText(frame,recognized,(x,y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    cv2.imshow("Face Recognition",frame)

    # PRESS Q TO CLOSE
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()