import cv2
import sqlite3

cam = cv2.VideoCapture(0)
faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml');

id = input('Enter user id : ')
name = input('Enter your name : ')
age = input('Enter your age : ')
gender = input('Enter your gender : ')
profession = input('Enter your profession : ')

conn = sqlite3.connect(
    "D:\Python\AccessEbal0\AccessEbal0V1\Face-detection-and-identification-with-mysql-database-in-real-time-master\FaceBase.db")
c = conn.cursor()
c.execute(f"INSERT INTO 'People' VALUES ('{id}','{name}', '{age}', '{gender}',' ', '{profession}')")
conn.commit()
conn.close()
sampleNum = 0
while (True):
    ret, frame = cam.read();
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5);
    for (x, y, w, h) in faces:
        sampleNum = sampleNum + 1;
        cv2.imwrite("DataSet/user." + id + '.' + str(sampleNum) + ".jpg", frame[y:y + h, x:x + w])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imshow('frame', frame)  # imgshow,it is declare as frame that's why it doesn't shows gray color
    if cv2.waitKey(20) & 0xFF == ord('q'):  # to close the frame just press q
        break

# When everything done, release the capture
cam.release()
cv2.destroyAllWindows()
