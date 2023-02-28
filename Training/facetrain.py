import os
import cv2
import numpy as np
from PIL import Image
recognizer = cv2.face.LBPHFaceRecognizer_create()
path = 'DataSet'

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
    recognizer.save('/bd/trainingData.yml')
    cv2.destroyAllWindows()
