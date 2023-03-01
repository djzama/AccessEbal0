import os
import cv2
import numpy as np
from PIL import Image
import glob


recognizer = cv2.face.LBPHFaceRecognizer_create()
path = 'D:\Python\AccessEbal0\Docker\db\DataSet'

def NewEbaloFromUnknown():

    faceDetect = cv2.CascadeClassifier(f'D:\Python\AccessEbal0\Docker\db/haarcascade_frontalface_default.xml')
    path_for_unknwn_images = r'D:\Python\AccessEbal0\Docker\Video\Unknown'
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(f"D:\Python\AccessEbal0\Docker\Training/recognizer/trainingData.yml")

    imagePaths = [os.path.join(path_for_unknwn_images, f) for f in os.listdir(path_for_unknwn_images)]
    print(imagePaths)
    sampleNum = 0
    for imagePath in imagePaths:
        frame = cv2.imread(imagePath)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            if (conf < 40):
                list_of_files = glob.glob(
                    'D:\Python\AccessEbal0\Docker\db\DataSet\*')
                list_of_ids_files = []
                maxnumber = []
                for imagePathh in list_of_files:
                    ID = int(os.path.split(imagePathh)[-1].split('.')[1])
                    if ID == id:
                        test = os.path.split(imagePathh)[-1]
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
                            str(buferiter + 1) + ".jpg", frame[y:y + h, x:x + w])
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

while(True):
    def getImagesWithID(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        print(imagePaths)
    # getImagesWithID(path)
        faces = []  # create an empty list for face
        IDs = []  # create empty list for the id
        count=0
        for imagePath in imagePaths:
            count +=1
            faceImg = Image.open(imagePath).convert("L")
            faceNp = np.array(faceImg, 'uint8')
            ID = int(os.path.split(imagePath)[-1].split('.')[1])
            faces.append(faceNp)
            print(ID)
            print(count)
            IDs.append(ID)
            #cv2.imshow("training", faceNp)
            cv2.waitKey(10)
        return np.array(IDs), faces


    Ids, faces = getImagesWithID(path)
    recognizer.train(faces, Ids)
    recognizer.save('D:\Python\AccessEbal0\Docker\Training/recognizer/trainingData.yml')
    NewEbaloFromUnknown()
    cv2.destroyAllWindows()
