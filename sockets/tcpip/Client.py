class Client:

    def __init__(self, id, ip, port, con):
        self.id = id
        self.ip = ip
        self.port = port
        self.con = con

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

    def __str__(self):
        print "Client [" + self.id + "] { \nIP Addr: " \
              + self.ip \
              + "\nPort: " \
              + str(self.port) \
              + "\n}"
