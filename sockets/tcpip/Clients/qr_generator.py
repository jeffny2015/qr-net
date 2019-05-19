#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uu
import hashlib
import pyqrcode
import os
from pyqrcode import QRCode

class gen_codQR:

	msj_dir = "/home/braulio/Desktop/messages/"
	msj_tam = 98
	sha1 = ""
	qr_0 = "1token0token0token"
	num_rep = []
	token = "token"

	def __init__(self, ips , ports):
		self.ips = ips
		self.ports = ports

	# Entrada: (nombre de archivo)
	# Salida: contenido del archivo
	def leer_archivo(self, nom_arch):
		arch_texto = 'temps/temp.txt'
		uu.encode(nom_arch, arch_texto)
		arch =  open(arch_texto, 'rb')
		cont = arch.read()
		arch.close()
		self.sha1 = self.codificar(cont)
		self.sha1 += " "
		return cont

	def codificar(self, cont):
		sha1 = hashlib.sha1(cont)
		val_hex = sha1.hexdigest()
		val_bytes = bytearray(sha1.digest())
		val_int = int(val_hex, 16)
		val_int = str(val_hex)
		return val_int

	# Entrada: (texto, tamaño total, tamaño de cada porción)
	# Salida: (array con texto dividido en porciones tam)
	def dividir_archivo(self, cont, bytes_arch):
		return [cont[i:i+self.msj_tam] for i in range(0, bytes_arch, self.msj_tam)]

	# Primero hay que definir el protocolo
	def convertir(self, msj, tam):
		for i in range(0, tam):
			qr = pyqrcode.create(msj[i], mode = 'binary')
			qr.png("qrs/frame" + str(i) + ".png", scale = 8)

	def protocolo(self, msj):
		self.qr_0 += self.sha1
		self.qr_0 += self.ips + " "
		self.qr_0 += self.ports
		largo_msj = len(msj)
		#msj = [("0token" + self.setLast(i, largo_msj) +"token" + str(i + 1) + "token" + self.sha1 + msj[i]) for i in range(0, largo_msj)]
		msj = [("0token" + self.setLast(i, largo_msj) + self.token + str(i + 1) + self.token + msj[i]) for i in range(0, largo_msj)]
		msj = [self.qr_0] + msj
		return msj

	def setLast(self, i, largo_msj):
		if i == (largo_msj - 1):
			return '1'
		return '0'

	# Entrada: (nombre de archivo, tamaño de cada porción de texto)
	def generar(self, nom_arch):
		cont = self.leer_archivo(self.msj_dir + nom_arch)
		bytes_arch = len(cont)
		msj = self.dividir_archivo(cont, bytes_arch)
		msj2 = self.protocolo(msj)
		tam = len(msj2)
		self.convertir(msj2, tam)
		return tam


'''def main():
	file_size_prueba = "0017FC340000"
	file_name_prueba = "0017FC250000"
	ips_prueba = "172.16.254.1"
	ports_prueba = "192.168.1.24"
	generador = gen_codQR(file_size_prueba,file_name_prueba,ips_prueba,ports_prueba)
	generador.generar("texto.txt")

if __name__ == '__main__':
	main()'''