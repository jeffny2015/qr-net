from Conection import Conection
import os

import socket

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


def main():
	print "-------------------------main"
	host = "10.20.104.169"
	port = 12345

	con = Conection(port, host)
	con.connect()

	hello(con.getsocket())
	# bye(con.getsocket())
	ip, set_port = requestIP(con.getsocket(), host) #lo que le entra aqui es la ip por la que quiere enviar un archivo, la ip por que que tiene que enviar basicamente
	sendFile(con.getsocket(), ip, set_port, "aaaaaaaaaaaaa.txt", host)


# filename = raw_input("Filename -> ")
# print("Filename:" + filename)

# print "K"


if __name__ == '__main__':
	main()