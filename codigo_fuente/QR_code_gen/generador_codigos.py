#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import pyqrcode
import os
from pyqrcode import QRCode

class gen_codQR:

	msj_dir = "D:\\braul\\Documents\\tec\\2019-I\\Redes\\Proyectos\\Proyecto1\\codigo_fuente\\Pruebas\\"
	msj_tam = 87
	sha1 = ""
	qr_0 = "1 0 0 "

	def __init__(self, mac_em, mac_re, ip_em, ip_re):
		self.mac_em = mac_em
		self.mac_re = mac_re
		self.ip_em = ip_em
		self.ip_re = ip_re


	# Entrada: (nombre de archivo)
	# Salida: contenido del archivo
	def leer_archivo(self, nom_arch):
		arch =  open(nom_arch, 'rb')
		cont = arch.read()
		arch.close()
		self.sha1 = self.codificar(cont)
		self.sha1 += "#"
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
			qr = pyqrcode.create(msj[i])
			qr.png(str(i) + "myqr.png", scale = 8)

	def protocolo(self, msj):
		self.qr_0 += self.sha1
		self.qr_0 += self.mac_em + " "
		self.qr_0 += self.mac_re + " "
		self.qr_0 += self.ip_em + " "
		self.qr_0 += self.ip_re
		largo_msj = len(msj)
		msj = [("0 " + "0 " + str(i) + " " + self.sha1 + msj[i]) for i in range(0, largo_msj)]
		msj = [self.qr_0] + msj
		return msj


	# Entrada: (nombre de archivo, tamaño de cada porción de texto)
	def generar(self, nom_arch):
		cont = self.leer_archivo(self.msj_dir + nom_arch)
		bytes_arch = len(cont)
		msj = self.dividir_archivo(cont, bytes_arch)
		msj2 = self.protocolo(msj)
		self.convertir(msj2, len(msj2))


def main():
	mac_em_prueba = "0017FC340000"
	mac_re_prueba = "0017FC250000"
	ip_em_prueba = "172.16.254.1"
	ip_re_prueba = "192.168.1.24"
	generador = gen_codQR(mac_em_prueba,mac_re_prueba,ip_em_prueba,ip_re_prueba)
	generador.generar("texto3.txt")

if __name__ == '__main__':
	main()