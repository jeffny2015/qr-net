import numpy as np
import cv2
import sys
import time
import pyzbar.pyzbar as pyzbar


cap = cv2.VideoCapture(0)

while True:
	_, frame = cap.read()
	decodedObjects = pyzbar.decode(frame)
	for obj in decodedObjects:
		print("Data", obj.data)
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1)
	if key == 27:
		break

#imagen = cv2.imread("imagenes/profile.jpg")

#cv2.imshow("Ventana de imagen", imagen)

#cv2.waitKey(0)