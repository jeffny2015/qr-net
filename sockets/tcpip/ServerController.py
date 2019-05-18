import os
import socket
import threading

from ClientsTable import ClientsTable
from Client import Client
from Server import Server
from Conection import Conection

WIDTH = 1024
PORT = 12345


def servrIP():
    ipv4 = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
    return ipv4


# tabla_ips, id=index en la tabla ip, filename,whos= 192.168.1.1/192.168.1.2
def sendFile(table, id, to_id, filename, whos, port, dest_port):
    dest = ''
    for d in whos:
        dest += d + '/'
    new_dest = dest[:-1]

    dest_ports = ''
    for d in port:
        dest_ports += d + '/'
    dest_ports = dest_ports[:-1]

    if os.path.isfile('clients/'+table[id].getIP()+'/'+filename):
        con = Conection(dest_port, table[to_id].getIP())
        con.connect()
        s = con.getsocket()
        s.send("SEND " + str(os.path.getsize(filename) + ' ' + filename) + ' ' + new_dest + ' ' + dest_ports)
        userResponse = s.recv(WIDTH)
        if userResponse[:2] == 'OK':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(WIDTH)
                s.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(WIDTH)
                    s.send(bytesToSend)
        con.close()


def recieve(s, table, id):

    while True:
        data = s.recv(WIDTH)

        if data[:5] == 'HELLO':
            print('Got HELLO from Client')
            tmp = data.split(' ')
            listen_port = tmp[1]
            table.getClient(id).setListenPort(listen_port)
            s.send("HELLO ")
        if data[:2] == 'TO':
            tmp_data = data.split(' ')
            to = tmp_data[1]
            know_client = table.knowClient(to)
            if tmp_data[1] == servrIP():
                print ("Client asking for my ip")
                #Probablemente agregar otra cosa al cliente cuando es para el el server principal
                s.send("ROUTE " + tmp_data[1] + ' ' + str(PORT))
            elif know_client != -1:

                s.send("ROUTE " + table.getClient(know_client).getIP() + " " + table.getClient(know_client).getListenPort())
            else:
                # for route and get the route
                route = "Prueba Ruta" # route
                s.send("ROUTE " + route)

        if data[:4] == 'SEND':
            tmp_data = data.split(' ')
            filesize = long(tmp_data[1])
            filename = tmp_data[2]
            to_who = tmp_data[3]
            ports = tmp_data[4]
            print "Client [" + str(id) + "]: File" + filename + ", " + str(filesize) + "Bytes"
            s.send('OK')
            table.printTable()
            name = 'clients/' + table.getClient(id).getIP() + '/' + filename
            f = open(name, 'wb')
	    data = s.recv(WIDTH)
            totalRecv = len(data)
            f.write(data)
            while totalRecv < filesize:
                data = s.recv(WIDTH)
                totalRecv += len(data)
		f.write(data)
                print "{0:.2f}".format((totalRecv / float(filesize)) * 100) + "% Done"
            print "Download Complete!"
	    f.close()
	    tmp = to_who.split('/')

            if tmp[0] == '':
                print "Got file from client to me"
            elif len(tmp) >= 1:
                ip = tmp[0]
                index = table.getIndex(ip)
                #Revisar esta
                if index != -1:
                    dest_ports = ports.split('/')
                    sendFile(table, id, index, name, tmp[1:], dest_ports[1:], dest_ports[0])
                else:
                    print 'No Client with ip= ' + ip
            else:
                print "Sending Message Error"

        if data[:2] == 'BY':
            print "Client [" + str(id) + "]: BY"


def main():

    print "Initializing Server"

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
            client.setID(count)
            count += 1
            clients.add(client)
	    if not os.path.exists('clients/'+client.getIP()+'/'):
            	os.mkdir('clients/'+client.getIP()+'/')
        index = clients.getID(client)
        t = threading.Thread(target=recieve, args=(client.getCon(), clients, index))
        t.start()

    server.close()


if __name__ == '__main__':
    main()
