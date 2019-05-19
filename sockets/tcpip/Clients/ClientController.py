#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Conection import Conection
import os
import threading
from qr_generator import gen_codQR
from qr_showcase import display_qr
import socket

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
ports = ""
ips = ""



WIDTH = 1024
PORT = 12346

def hello(con):
	print "-------------------------hello"
	con.send('HELLO ' + str(PORT))
	data = con.recv(WIDTH)

	if data[:5] == 'HELLO':
		print('Server say HELLO')
	else:
		print("Something is wrong")


def bye(con):
	print "-------------------------bye"
	con.send('BYE ')
	print('Server say BYE')
	con.close()


def requestIP(con, ip):
	print "-------------------------requestIP"
	con.send('TO ' + ip)
	data = con.recv(WIDTH)
	if data[:5] == 'ROUTE':
		tmp = data.split(' ')
		return tmp[1], tmp[2]
	return '-1'


def sendFile(socket, ip, port, filename, host):
	print "-------------------------sendFile"
	dest_ip = ip.split('/')
	new_dest = ''
	if len(dest_ip) == 1:
		# 192.168.1.1
		dest_host = dest_ip[0]
	else:
		# 192.168.1.1/192.168.1.104/192.168.1.130
		dest_host = dest_ip[0]
		for des in dest_ip[1:]:
			new_dest += des + '/'
		new_dest = new_dest[:-1]

	if os.path.isfile(filename):
		if dest_ip[0] == host:

			dest_ports = port.split('/')
			new_dest_ports = ''
			for d in dest_ports[1:]:
				new_dest_ports += d + '/'
			new_dest_ports = new_dest_ports[:-1]

			s = socket
			s.send('SEND ' + str(os.path.getsize(filename)) + ' ' + filename + ' ' + new_dest + ' ' + new_dest_ports )

			data = s.recv(WIDTH)
			if data[:2] == 'OK':
				with open(filename, 'rb') as f:
					bytesToSend = f.read(WIDTH)
					s.send(bytesToSend)
					while bytesToSend != "":
						bytesToSend = f.read(WIDTH)
						s.send(bytesToSend)
			else:
				print "Error while sending file:" + filename
				s.send("ERROR")
		else:
			dest_ports = port.split('/')
			new_dest_ports = ''
			for d in dest_ports[1:]:
				new_dest_ports += d + '/'
			new_dest_ports = new_dest_ports[:-1]

			file_transfer = Conection(dest_ports[0], dest_host)
			file_transfer.connect()
			s = file_transfer.getsocket()
			s.send('SEND ' + str(os.path.getsize(filename)) + ' ' + filename + ' ' + new_dest + ' ' + new_dest_ports)

			data = s.recv(WIDTH)
			if data[:2] == 'OK':
				with open(filename, 'rb') as f:
					bytesToSend = f.read(WIDTH)
					s.send(bytesToSend)
					while bytesToSend != "":
						bytesToSend = f.read(WIDTH)
						s.send(bytesToSend)
			else:
				print "Error while sending file:" + filename
				s.send("ERROR")
		s.close()




def escribir_archivo():
	arch_texto = 'temp2.txt'
	arch =  open(arch_texto, 'w+')
	cont = arch.write(msj)
	arch.close()
	uu.decode(arch_texto, file_name)

def watch():
	final = 0
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
	t.start()
	print "-------------------------main"
	host = "172.28.130.42"
	port = 12345

	con = Conection(port, host)
	con.connect()

	hello(con.getsocket())
	# bye(con.getsocket())
	ip, set_port = requestIP(con.getsocket(), "172.28.130.110") #lo que le entra aqui es la ip por la que quiere enviar un archivo, la ip por que que tiene que enviar basicamente
	s = ip.split('/') #sendFile(con.getsocket(), ip, set_port, "aaaaaaaaaaaaa.txt", host)
	print s[0]
	if s[0] == "172.28.130.110":
		generador = gen_codQR(ip, set_port)
		file_name = raw_input()
		tam = generador.generar(file_name)
		disp = display_qr(tam)

# filename = raw_input("Filename -> ")
# print("Filename:" + filename)

# print "K"


if __name__ == '__main__':
	main()
