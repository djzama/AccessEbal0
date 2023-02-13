from aiogram import *
import cv2
import sqlite3

API_TOKEN = '5876734711:AAEuAXxnxjF31z-_bPZAxNRrOaOzfdOjb6M'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["protect"])
async def echo(message: types.Message):
	recognizer = cv2.face.LBPHFaceRecognizer_create(); #create a recognizer, LBPH is a face recognition algorithm.Local Binary Patterns Histograms
	recognizer.read("D:\Python\AccessEbal0\AccessEbal0V1\Face-detection-and-identification-with-mysql-database-in-real-time-master\\recognizer\\trainingData.yml")
	faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
	path = 'D:\Python\AccessEbal0\AccessEbal0V1\Face-detection-and-identification-with-mysql-database-in-real-time-master\DataSet'

	conn = sqlite3.connect("D:\Python\AccessEbal0\AccessEbal0V1\Face-detection-and-identification-with-mysql-database-in-real-time-master\FaceBase.db")
	c = conn.cursor()

	cam = cv2.VideoCapture(0);
	font = cv2.FONT_HERSHEY_SIMPLEX #5=font size
	fontscale = 1
	fontcolor = (255,255,255)
	stroke = 2
	profiles={}
	while(True):
		ret, frame = cam.read()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces=faceDetect.detectMultiScale(gray,1.3,5);
		for(x,y,w,h) in faces:
			id, conf = recognizer.predict(gray[y:y+h,x:x+w])
			cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
			if(conf<50):
				c.execute(f"SELECT * FROM People WHERE id = '{id}';")
				val = c.fetchall()
				for i in val:
					cv2.putText(frame, "Name:" + str(i[1]), (x, y + h + 30), font, fontscale, fontcolor, stroke)
					cv2.putText(frame, "Age:" + str(i[2]), (x, y + h + 60), font, fontscale, fontcolor, stroke)
					cv2.putText(frame, "Gender:" + str(i[3]), (x, y + h + 90), font, fontscale, fontcolor, stroke)
					cv2.putText(frame, "Criminal Records:" + str(i[4]), (x, y + h + 120), font, fontscale, fontcolor,stroke)
					cv2.putText(frame, "Profession:" + str(i[5]), (x, y + h + 150), font, fontscale, fontcolor,stroke)
					await message.answer("К вам пришел {0}".format(str(i[1])))
				conn.commit()
			else:
				cv2.putText(frame, "Name:" + "Unknown", (x, y + h + 30), font, fontscale, fontcolor, stroke)

		cv2.imshow("frame",frame);
		if cv2.waitKey(20) & 0xFF == ord('q'):
			break;
	cam.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)