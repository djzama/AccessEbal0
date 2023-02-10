import cv2


#some params
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

#capturing video
cap = cv2.VideoCapture("rtsp://admin:admin123@172.19.3.15:22223/RVi/1/1")
def face_detect_loop():
    while True:
        # Read a frame from the video stream
        ret, frame = cap.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the processed frame
        cv2.imshow("Face Detection", frame)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()