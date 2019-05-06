#!/usr/bin/env python
# -*- coding: utf-8 -*-

from qr_generator import gen_codQR
from qr_showcase import display_qr

def main():
	mac_em_prueba = "0017FC340000"
	mac_re_prueba = "0017FC250000"
	ip_em_prueba = "172.16.254.1"
	ip_re_prueba = "192.168.1.24"
	generador = gen_codQR(mac_em_prueba,mac_re_prueba,ip_em_prueba,ip_re_prueba)
	file_name = raw_input()
	tam = generador.generar(file_name)
	disp = display_qr(tam)
	disp.display()

if __name__ == '__main__':
	main()