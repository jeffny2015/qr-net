import pyqrcode
import os
from pyqrcode import QRCode



pruebas_dir = "D:\\braul\\Documents\\tec\\2019-I\\Redes\\Proyectos\\Proyecto1\\codigo_fuente\\Pruebas\\"
prueba = pruebas_dir + "imagen.png"

stat = os.path.getsize(prueba)
print stat

f = open(prueba, 'rb')

file_content = f.read()

f.close()
s = "D:\\braul\\Documents\\tec\\2019-I\\Redes\\Proyectos\\Proyecto1\\codigo_fuente\\imagenes"

print file_content

url = pyqrcode.create(file_content)

url.svg("myqr.svg", scale = 8)

# I - 2 byte
# F - 2 byte
# # - 8 bytes
# xxxxxxxxxxxx - 13 bytes
# xxxxxxxxxxxx - 13 bytes
# xxx.xxx.xxx.xxx - 16 bytes
# xxx.xxx.xxx.xxx - 16 bytes

# protocolo - 70 bytes

# mensaje - 58 bytes

# total - 128 bytes

# 1369fa9e0b933431ba9debea60cf9834a3617202
# d3356b5961aacbbc9e6d3e41da1e59935f88b50c

# 40