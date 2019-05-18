#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
from qr_generator import gen_codQR
from qr_showcase import display_qr

def escribir_archivo():
	arch_texto = 'temp2.txt'
	arch =  open(arch_texto, 'w+')
	cont = arch.write(msj)
	arch.close()
	uu.decode(arch_texto, file_name)

def watch():
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
				ips = direcciones[1]
				ports = direcciones[2]
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
			print ips
			print ports
			final = 0

def main():
	t = threading.Thread(target=watch)
	ips = "172.16.254.1/172.16.254.1/172.16.254.1/172.16.254.1"
	ports = "3001/3002/3003/3004"
	generador = gen_codQR(ips , ports)
	file_name = raw_input()
	tam = generador.generar(file_name)
	disp = display_qr(tam)
	disp.display()

if __name__ == '__main__':
	main()



1token0token0token1d7344415cd16bf4b162668194c21fddca88c607 172.16.254.1/172.16.254.1/172.16.254.1/172.16.254.1 3001/3002/3003/3004