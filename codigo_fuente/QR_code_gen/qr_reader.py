import numpy as np
import cv2
import sys
import time
import pyzbar.pyzbar as pyzbar
import uu
import re


cap = cv2.VideoCapture(0)
num = 0
sha1 = ""
msj = ""
file_name = ""
ip_dest = ""
ip_send = ""
mac_dest = ""
mac_send = ""
final = 0

def escribir_archivo():
	arch_texto = 'temp2.txt'
	arch =  open(arch_texto, 'w+')
	cont = arch.write(msj)
	arch.close()
	uu.decode(arch_texto, file_name)

while True:
	_, frame = cap.read()
	decodedObjects = pyzbar.decode(frame)
	for obj in decodedObjects:
		print("Data", obj.data)
		datos = obj.data.split('token')
		n = int(datos[2])
		final = int(datos[1])
		if int(datos[0]) == 1:
			direcciones = datos[3].split(' ')
			sha1 = direcciones[0]
			mac_send = direcciones[1]
			mac_dest = direcciones[2]
			ip_send = direcciones[3]
			ip_dest = direcciones[4]
		else:
			if n == 1:
				file_name = re.search("\dtoken\dtoken\dtoken.{40}tokenbegin 666 (.+\..+)\n", datos[3])
			if num != n:
				num = n
				msj += datos[3]
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1)
	if final == 1:
		escribir_archivo()
		print sha1
		print mac_send
		print mac_dest
		print ip_send
		print ip_dest
		break