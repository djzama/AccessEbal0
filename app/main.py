import os
import mysql.connector

from cam import face_detect_loop
# Create a Haar cascade classifier for face detection
db_connect = mysql.connector.connect(
    host='127.0.0.1',
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    database="IdenFaces1"
)

if __name__ == '__main__':
    import telebot
    telebot()
    face_detect_loop()