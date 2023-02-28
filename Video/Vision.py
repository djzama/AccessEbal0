import cv2
import pymysql
import os
import time
import glob
import requests
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from sys import argv
import subprocess
import collections
def Vremya():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time

def send_message(chat_id, text):
    requests.get(f'{URL}{API_TOKEN}/sendMessage?chat_id={chat_id}&text={text}')


# def Updater():
#     if Vremya() == "23:59:00":
#         time.sleep(1)
#         os.startfile('facetrain.exe')

API_TOKEN = '5876734711:AAEuAXxnxjF31z-_bPZAxNRrOaOzfdOjb6M'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
URL = 'https://api.telegram.org/bot'

conn = sqlite3.connect(u"D:\Python\AccessEbal0\AccessEbal0Obuchaemaya\FaceBase.db")
c = conn.cursor()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(f"D:\Python\AccessEbal0\Docker\Training/trainingData.yml")
faceDetect = cv2.CascadeClassifier(f'D:\Python\AccessEbal0\Docker\db/haarcascade_frontalface_default.xml')

# conn = pymysql.connect(
#     host="localhost",  # your host, usually localhost
#     user="root",  # your username
#     passwd=os.getenv['MYSQL_ROOT_PASSWORD'],  # your password
#     db=os.getenv['MYSQL_DATABASE']
# )
# c = conn.cursor()

#script,cam_address = argv
# "rtsp://admin:admin123@172.19.3.15:22225/RVi/1/2"
cam = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX  # 5=font size
fontscale = 1
fontcolor = (255, 255, 255)
stroke = 2
sleep = 0
max_4_items = collections.deque([None] * 4, maxlen=4)
while (True):
    # Updater()
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        id, conf = recognizer.predict(gray[y:y + h, x:x + w])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        if (conf < 80):
            sleep += 1
            c.execute(f"SELECT * FROM People WHERE id = '{id}';")
            val = c.fetchall()
            for i in val:
                cv2.putText(
                    frame, "Name:" + str(i[1]), (x, y + h + 30), font, fontscale, fontcolor, stroke)
                if sleep == 5:
                    send_message(786824447, "К вам пришел {0} в {1}".format(str(i[1]), Vremya()))
                    #await message.answer("К вам пришел {0} в {1}".format(str(i[1]), Vremya()))

                    max_4_items.append(frame)
                    for writer in max_4_items:
                        cv2.imwrite("D:\Python\AccessEbal0\Docker\Video\TopFaceFolder",writer)


                    #cv2.imshow("Ebalo", frame)
                if sleep == 50:
                    sleep = 0
            conn.commit()
        else:
            cv2.putText(frame, "Name:" + "Unknown", (x, y + h + 30),
                        font, fontscale, fontcolor, stroke)
            sleep = 0


        if (conf < 65):
            list_of_files = glob.glob(
                'D:\Python\AccessEbal0\Docker\db\DataSet\*')
            list_of_ids_files = []
            maxnumber = []
            for imagePath in list_of_files:
                ID = int(os.path.split(imagePath)[-1].split('.')[1])
                if ID == id:
                    test = os.path.split(imagePath)[-1]
                    list_of_ids_files.append(test)
                for latest_file in list_of_ids_files:
                    flag = 0
                    bufer = ''
                    for i in latest_file:
                        if i == '.':
                            flag += 1
                            if flag == 3:
                                break
                        if flag >= 2:
                            bufer += i
                    buferiterlow = bufer[1:]
                    maxnumber.append(int(buferiterlow))
            buferiter = max(maxnumber)
            cv2.imwrite("/bd/DataSet/user." + str(id) + '.' +
                        str(buferiter+1) + ".jpg", frame[y:y + h, x:x + w])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imshow("frame", frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
