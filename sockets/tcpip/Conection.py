import socket


class Conection:

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
