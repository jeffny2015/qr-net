class ClientsTable:
    '''
    EN esta clase se maneja una tabla de clientes(Client.py Client)
    aqui estan las funcionalidades que se pueden hacer con la tabla cliente
    y para acceder a cada posicion de la tabla
    Esta clase se usa en ServerController.py
    '''

    def __init__(self):
        self.table = []
        # ip's:id|index
        self.dictionary = {}
        # ip's:puertos en los que se escuchan
        self.listen = {}

    def add(self, client):
        self.table.append(client)
        self.dictionary[client.getIP()] = client.getID()
        self.listen[client.getIP()] = client.getListenPort()

    def printTable(self):
        print self.table

    def getClient(self, cid):
        return self.table[cid]

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

    def getLPort(self, ip):
        if ip in self.listen:
            return self.listen[ip]
        else:
            return -1

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
