class Client:

    def __init__(self, id, ip, port, con):
        self.id = id
        self.ip = ip
        self.port = port
        self.con = con
        self.listen_port = ''

    def getID(self):
        return self.id

    def getIP(self):
        return self.ip

    def getPort(self):
        return self.port

    def getCon(self):
        return self.con

    def setID(self, id):
        self.id = id

    def setIP(self, ip):
        self.ip = ip

    def setPort(self, port):
        self.port = port

    def setCon(self, con):
        self.con = con

    def setListenPort(self, port):
        self.listen_port = port

    def getListenPort(self):
        return self.listen_port

    def __str__(self):
        print "Client [" + self.id + "] { \nIP Addr: " \
              + self.ip \
              + "\nPort: " \
              + str(self.port) \
              + "\n}"
