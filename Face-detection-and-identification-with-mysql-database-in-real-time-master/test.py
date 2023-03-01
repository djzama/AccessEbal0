import cv2
import sqlite3
import numpy
from PIL import Image, ImageFont, ImageDraw

# Эта функция предназначена для отображения на китайском языке, opencv имеет функцию отображения текста и не может отображать китайский язык.
def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=20):
    if (isinstance(img, numpy.ndarray)):  # Оценить, является ли тип изображения OpenCV
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontText = ImageFont.truetype(
        "./simsun.ttc", textSize, encoding="utf-8")
    draw.text((left, top), text, textColor, font=fontText)
    return cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)
def getDataFromSql():
    names = {}
    # Создать соединение
    con = sqlite3.connect("D:\Python\AccessEbal0\Face-detection-and-identification-with-mysql-database-in-real-time-master\FaceBase.db")
    # Создать объект курсора
    cur = con.cursor()
    # Написать запрос sql
    sql = "SELECT * FROM People"
    # Выполнить sql
    try:
        cur.execute(sql)
        # Обработка набора результатов
        students = cur.fetchall()
        for student in students:
            id = student[0]
            sname = student[1]
            sno = student[2]
            names[int(id)] = sname
    except Exception as e:
        print(e)
        print("Не удалось запросить все данные")
    finally:
        # Закрыть соединение
        con.close()
        return names

if __name__ == '__main__':
    recogizer=cv2.face.LBPHFaceRecognizer_create()
    # Загрузить файл набора данных для обучения
    recogizer.read('D:\Python\AccessEbal0\Face-detection-and-identification-with-mysql-database-in-real-time-master\\recognizer\\trainingData.yml')
    # Загрузить данные об особенностях лица
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    names = getDataFromSql() # Получить соответствующие данные из базы данных
    cam = cv2.VideoCapture(0) # Включите камеру по умолчанию, другие параметры внешней камеры можно изменить на 1, 2 ....
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    font = cv2.FONT_HERSHEY_SIMPLEX # font format
    while True:
        ret, img = cam.read() # Прочитать каждый кадр изображения
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Установить изображение в оттенках серого
        faces = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH))
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            idnum, confidence = recogizer.predict(gray[y:y+h, x:x+w])
            if confidence < 60:
                idname = names[idnum]
                confidence = "{0}%".format(round(100 - confidence))
            else:
                idname = 'unknown'
                confidence = "{0}%".format(round(100 - confidence))
            # Показать имя и сходство на картинке
            img = cv2ImgAddText(img, idname, x, y-30, (0, 255, 0),30) # Показать китайский
            #cv2.putText(img, str(idname), (x+5, y-5), font, 1, (0, 0, 255), 2)
            cv2.putText(img, str(confidence), (x+5, y+h-5), font, 1, (0, 0, 255), 2)
        cv2.imshow('Camera', img)
        k = cv2.waitKey(1)
        if k == 27:# Нажмите ESC, чтобы выключить камеру и выйти из функции распознавания лиц.
            break
    cam.release()
    cv2.destroyAllWindows()