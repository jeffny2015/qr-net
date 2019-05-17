class ClientsTable:

    def __init__(self):
        self.table = []
        self.dictionary = {}

    def add(self, client):
        self.table.append(client)
        self.dictionary[client.getIP()] = client.getID()

    def isClient(self, c):
        if c.getIP() in self.dictionary:
            return True
        else:
            return False

    def getIndex(self, ip):
        if ip in self.dictionary:
            return int(self.dictionary[ip])
        else:
            return -1

    def knowClient(self, ip):
        if ip in self.dictionary:
            return int(self.dictionary[ip])
        else:
            return -1

    def getID(self, c):
        return int(self.dictionary[c.getIP()])

    def update(self, c, i):
        self.table[i].setIP(c.getIP())
        self.table[i].setPort(c.getPort())
        self.table[i].getCon().close()
        self.table[i].setCon(c.getCon())

    def showTable(self):
        for client in self.table:
            print "[ID]" + client.getID() +\
                  " [IP]" + client.getIP() +\
                  " [PORT]" + str(client.getPort())
