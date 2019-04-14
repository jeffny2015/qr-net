import pyqrcode
import os
from pyqrcode import QRCode



pruebas_dir = "D:\\braul\\Documents\\tec\\2019-I\\Redes\\Proyectos\\Proyecto1\\codigo_fuente\\Pruebas\\"
prueba = pruebas_dir + "texto.txt"

stat = os.path.getsize(prueba)
print stat

f = open(prueba, 'rb')

file_content = f.read()

f.close()
s = "D:\\braul\\Documents\\tec\\2019-I\\Redes\\Proyectos\\Proyecto1\\codigo_fuente\\imagenes"

print file_content

url = pyqrcode.create(file_content)

url.svg("myqr.svg", scale = 8)