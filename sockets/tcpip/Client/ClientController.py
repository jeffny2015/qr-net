#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Conection import Conection
from Server import Server
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


def recieve(con, ip, port, host):
	data = con.recv(WIDTH)
	if data[:4] == 'SEND':
		tmp_data = data.split(' ')
		filesize = long(tmp_data[1])
		filename = tmp_data[2]
		to_who = tmp_data[3]
		ports = tmp_data[4]
		print "File" + filename + ", " + str(filesize) + "Bytes"
		con.send('OK')
		f = open(filename, 'wb')
		data = con.recv(WIDTH)
		totalRecv = len(data)
		f.write(data)
		while totalRecv < filesize:
			data = con.recv(WIDTH)
			totalRecv += len(data)
			f.write(data)
			print "{0:.2f}".format((totalRecv / float(filesize)) * 100) + "% Done"
		print "Download Complete!"
		f.close()

		tmp = to_who.split('/')
		if tmp[0] == '':
			print "Got file to me"
		elif len(tmp) >= 1:
			ip = tmp[0]
			dest_ports = ports.split('/')
			new_con = Conection(ip, int(ports[0]))

			dest_ips = ''
			for i in tmp[1:]:
				dest_ips += i + '/'
			dest_ips = dest_ips[:-1]
			new_dest_ports = ''
			for i in dest_ports[1:]:
				new_dest_ports += i + '/'
			new_dest_ports = new_dest_ports[:-1]

			sendFile(new_con.getsocket(), dest_ips, new_dest_ports, filename, host)


def listen_Con(listen_port,host):
	allowed_clients = 25

	server = Server(listen_port)
	server.bind()
	server.listen(allowed_clients)

	while True:
		con, addr = server.accept()
		print "Got connection from => " + addr[0] + ":" + str(addr[1])
		t = threading.Thread(target=recieve, args=(con, addr[0], addr[1], host))
        t.start()


def escribir_archivo(fn):
	arch_texto = 'temps/temp2'
	arch =  open(arch_texto, 'w+')
	cont = arch.write(msj)
	arch.close()
	uu.decode(arch_texto, 'to_send/' + fn)

def watch():
	final = 0
	fn = ""
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
					fn = re.search("\dtoken\dtoken\dtoken.{40}tokenbegin 666 (.+\..+)\n", datos[3])
				if num != n:
					num = n
					msj += datos[3]
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1)
		if final == 1:
			escribir_archivo(fn)
			print sha1
			print ips
			print ports
			final = 0
			if ips != '':
				ip, set_port = requestIP(con.getsocket(), ips) #lo que le entra aqui es la ip por la que quiere enviar un archivo, la ip por que que tiene que enviar basicamente
				s = ip.split('/')
				print s[0]
				if s[0] == ips:
					generador = gen_codQR(ip, set_port)
					tam = generador.generar(fn)
					disp = display_qr(tam)
				else:
					sendFile(con.getsocket(), ip, set_port, 'to_send/' + fn, ips)

def main():
	host = "172.28.130.42"
	port = 12345
	t = threading.Thread(target=watch)
	t.start()
	t2 = threading.Thread(target=listen_Con, args=(HOST, host))
	con = Conection(port, host)
	con.connect()

	hello(con.getsocket())
	# bye(con.getsocket())
	while True:
		ip_to_request = raw_input()
		file_name = raw_input()
		ip, set_port = requestIP(con.getsocket(), ip_to_request) #lo que le entra aqui es la ip por la que quiere enviar un archivo, la ip por que que tiene que enviar basicamente
		s = ip.split('/')
		print s[0]
		if s[0] == ip_to_request:
			generador = gen_codQR(ip, set_port)
			tam = generador.generar(file_name)
			disp = display_qr(tam)
		else:
			sendFile(con.getsocket(), ip, set_port, 'to_send/' + file_name, ip_to_request)

# filename = raw_input("Filename -> ")
# print("Filename:" + filename)

# print "K"


if __name__ == '__main__':
	main()
