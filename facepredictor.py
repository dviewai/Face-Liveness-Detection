from keras.preprocessing.image import img_to_array
from keras.models import load_model
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import imutils
import cv2
import os
import sys
import dlib

def predictperson():
	video_capture = cv2.VideoCapture(0)
	startinit = 0
	while(True):
		if cv2.waitKey(1) & 0xFF == ord('q'):
					break 
		ret,frame = video_capture.read()
		if startinit==0:
			frame_shape = frame.shape
			ymax = frame_shape[0]
			xmax = frame_shape[1]
			x1 = np.int(np.floor((xmax - (xmax/2))/2))
			y1 = np.int(np.floor((ymax - (ymax / 2)) / 2))
			x2 = np.int(np.floor(x1 + xmax/2))
			y2 = np.int(np.floor(y1 + ymax/2))
			startinit = 1
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30),)
		#cv2.rectangle(frame, (400, 100), (900, 550), (255,0,0), 2)
		# cv2.putText(frame,"Please keep your head inside the blue box and have only one face in the frame", (10, 700),
		#		cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

		cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
		cv2.putText(frame, "Please keep your head inside the blue box and have only one face in the frame", (10, ymax-50),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		
		faces_inside_box = 0
		for (x, y, w, h) in faces:
			if x<x2 and x>x1 and y<y2 and y>y1 and (x+w)<x2 and (x+w)>x1 and (y+h)<y2 and (y+h)>y1:
				faces_inside_box+=1
				cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

		if faces_inside_box > 1 :
			cv2.putText(frame,"Multiple Faces detected!", (xmax-100, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

		if faces_inside_box == 1 :
			(x, y, w, h)
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

			image = cv2.resize(frame, (128, 128))
			image = image.astype("float") / 255.0
			image = img_to_array(image)
			image = np.expand_dims(image, axis=0)
			(real, fake) = model.predict(image)[0]
			if fake > real:
				label = "fake"
			else:
				label = "real"
			label = "{}".format(label)
			cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

			#if(w*h > (500*450)/4 ) and x<800 and x>400 and y<300 and y>100 and (x+w)<900 and (x+w)>400 and (y+h)<560 and (y+h)>100:
			# if (w * h > (ymax * xmax) / 4) and x < x2 and x > x1 and y < y2 and y > y1 and (x + w) < x2 and (
			# 			x + w) > x1 and (y + h) < y2 and (y + h) > y1:
			# 	image = cv2.resize(frame, (128, 128))
			# 	image = image.astype("float") / 255.0
			# 	image = img_to_array(image)
			# 	image = np.expand_dims(image, axis=0)
			# 	(real, fake) = model.predict(image)[0]
			# 	if fake > real:
			# 		label = "fake"
			# 	else:
			# 		label= "real"
			# 	label = "{}".format(label)
			# 	cv2.putText(frame,label, (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
			#
			# else:
			# 	cv2.putText(frame,"Please come closer to the camera", (10, 390),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		cv2.imshow("Frame",frame)
			
	

if __name__ == '__main__':

	model = load_model("models/anandfinal.hdf5")
	cascPath = "haarcascade_frontalface_default.xml"
	faceCascade = cv2.CascadeClassifier(cascPath)
	predictperson()
	