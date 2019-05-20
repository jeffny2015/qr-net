import socket


class Server:
    '''
    Recive como parametro el puerto donde el socket va a inicializarse 
    y tiene como atributo un sockete en el que los metodos bind, listen close y accpet
    son funciones para manejar el socket
    Esta clase se usa en ServerController.py
    '''
    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port

    def bind(self):
        # (TCP_IP, TCP_PORT)
        return self.socket.bind(('', self.port))

    def listen(self, quantity):
        return self.socket.listen(quantity)

    def socket(self):
        return self.socket

    def close(self):
        return self.socket.close()

    def accept(self):
        return self.socket.accept()
