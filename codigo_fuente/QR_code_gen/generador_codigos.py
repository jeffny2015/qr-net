#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyqrcode
import os
from pyqrcode import QRCode

class gen_codQR:

	msj_dir = "D:\\braul\\Documents\\tec\\2019-I\\Redes\\Proyectos\\Proyecto1\\codigo_fuente\\Pruebas\\"

	def __init__(self):
		pass

	# Entrada: (nombre de archivo)
	# Salida: contenido del archivo
	def leer_archivo(self, nom_arch):
		arch =  open(nom_arch, 'rb')
		cont = arch.read()
		arch.close()
		return cont

	# Entrada: (texto, tamaño total, tamaño de cada porción)
	# Salida: (array con texto dividido en porciones tam)
	def dividir_archivo(self, cont, bytes_arch, tam):
		return [cont[i:i+tam] for i in range(0, bytes_arch, tam)]

	# Primero hay que definir el protocolo
	def convertir(self):
		url = pyqrcode.create(file_content)
		url.svg("myqr.svg", scale = 8)

	# Entrada: (nombre de archivo, tamaño de cada porción de texto)
	def generar(self, nom_arch, tam):
		cont = self.leer_archivo(self.msj_dir + nom_arch)
		bytes_arch = len(cont)
		arch_div = self.dividir_archivo(cont, bytes_arch, tam)
		print arch_div


def main():
	generador = gen_codQR()
	generador.generar("texto.txt", 15)

if __name__ == '__main__':
	main()