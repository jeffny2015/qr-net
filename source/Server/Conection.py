import socket


class Conection:
    '''
    Esta clase lo que hace es lo contrario a Server.py en vez de escuchar por 
    nuevas conecciones este recibe un puerto y un host para poder crear un socket
    y intentar conectarse a ese host con la funccion connect
    Esta clase se usar en Server Controller
    '''
    def __init__(self, port, host):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.host = host

    def getsocket(self):
        return self.socket

    def close(self):
        return self.socket.close()

    def connect(self):
        return self.socket.connect((self.host, self.port))
