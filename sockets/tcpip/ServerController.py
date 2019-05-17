import os
import socket
import threading

from ClientsTable import ClientsTable
from Client import Client
from Server import Server

WIDTH = 1024


def servrIP():
    ipv4 = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
    return ipv4


def sendFile(s, table, id, to_id, filename, whos):
    w = ''
    for dest in whos:
        w += dest + '/'
    wh = w[:-1]
    if os.path.isfile('clients/'+table[id].getIP()+'/'+filename):
        s.send("FILE " + str(os.path.getsize(filename) + " " + filename) + " " + whos)
        userResponse = s.recv(WIDTH)
        if userResponse[:2] == 'OK':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(WIDTH)
                s.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(WIDTH)
                    s.send(bytesToSend)
    else:
        s.send("ERROR")


def recieve(s, table, id):

    while True:
        data = s.recv(WIDTH)

        if data[:5] == 'HELLO':
            print('Got HELLO from Client')
            s.send("HELLO ")
        if data[:2] == 'TO':
            tmp_data = data.split(' ')
            to = tmp_data[1]
            know_client = table.knowClient(to)
            if know_client == servrIP():
                print ("Client asking for my ip")
                s.send("ROUTE" + know_client)
            elif know_client != -1:
                s.send("ROUTE" + know_client)
            else:
                # for route and get the route
                route = "Prueba Ruta" # route
                s.send("ROUTE " + route)

        if data[:4] == 'SEND':
            tmp_data = data.split(' ')
            filesize = long(tmp_data[1])
            filename = tmp_data[2]
            to_who = tmp_data[3]
            print"Client [" + str(id) + "]: File" + filename + ", " + str(filesize) + "Bytes"
            s.send('OK')
            name = 'clients/' + table[id].getIP() + '/' + filename
            f = open(name, 'wb')
            data = s.recv(WIDTH)
            totalRecv = len(data)
            f.write(data)
            while totalRecv < filesize:
                data = s.recv(WIDTH)
                totalRecv += len(data)
                f.write(data)
                print("{0:.2f}".format((totalRecv / float(filesize)) * 100) + "% Done")
            print("Download Complete!")

            tmp = to_who.split('/')

            if len(tmp) == 1:
                if tmp[0] == servrIP():
                    print "FILE to the server"
                else:
                    ip = tmp[0]
                    index = table.getIndex(ip)
                    if index != -1:
                        sendFile(table[index].getCon(), table, id, index, name, tmp)
                    else:
                        print("Search")
            elif len(tmp) > 1:
                ip = tmp[0]
                index = table.getIndex(ip)
                if index != -1:
                    sendFile(table[index].getCon(), table, id, index, name, tmp[1:])
                else:
                    print("Search")
            else:
                print("Message Error")

        if data[:3] == 'BYE':
            print("Client [" + str(id) + "]: BYE")


def main():

    print("Initializing Server")

    if not os.path.isdir('clients'):
        os.mkdir('clients')

    clients = ClientsTable()

    port = 12345
    allowed_clients = 25

    server = Server(port)
    server.bind()
    server.listen(allowed_clients)
    count = 0

    while True:
        con, addr = server.accept()
        print "Got connection from => " + addr[0] + ":" + str(addr[1])

        client = Client(str(count), addr[0], addr[1], con)

        if clients.isClient(client):
            index = clients.getID(client)
            clients.update(client, index)
        else:
            print("New CLient")
            count += 1
            client.setID(count)
            clients.add(client)
            os.mkdir('clients/'+client.getIP()+':'+str(client.getPort())+'/')
        index = clients.getID(client)
        t = threading.Thread(target=recieve, args=(client.getCon(), clients, index))
        t.start()

    server.close()


if __name__ == '__main__':
    main()
