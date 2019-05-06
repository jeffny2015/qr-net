import numpy as np
import cv2
import sys
import time
import pyzbar.pyzbar as pyzbar
import uu


cap = cv2.VideoCapture(0)
dat = ""
inicio = 0
final = 0
num = 0
ident = ""
msj = ""

def escribir_archivo():
	arch_texto = 'temp2.txt'
	arch =  open(arch_texto, 'w+')
	cont = arch.write(msj)
	arch.close()
	uu.decode(arch_texto, 'original.txt')

while True:
	_, frame = cap.read()
	decodedObjects = pyzbar.decode(frame)
	for obj in decodedObjects:
		print("Data", obj.data)
		datos = obj.data.split('token')
		n = int(datos[2])
		if num != n:
			num = n
			msj += datos[4]
		final = int(datos[1])
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1)
	if key == 27:
		escribir_archivo()
		break


#imagen = cv2.imread("imagenes/profile.jpg")

#cv2.imshow("Ventana de imagen", imagen)

#cv2.waitKey(0)