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
    #optener IP del de este dispositivo
    ipv4 = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
    return ipv4


def sendFile(table, id, to_id, filename, whos, port, dest_port):
    '''
    Se envia el el archivo  revisando que exista en el directorio por el cual el cliente habia enviado
    a este server
    '''
    dest = ''
    for d in whos:
        dest += d + '/'
    new_dest = dest[:-1]

    dest_ports = ''
    for d in port:
        dest_ports += d + '/'
    dest_ports = dest_ports[:-1]

    if os.path.isfile('clients/'+table[id].getIP()+'/'+filename):
        print 'New Conection'
        con = Conection(dest_port, table[to_id].getIP())
        con.connect()
        s = con.getsocket()
        print "Sending .."
        s.send("SEND " + str(os.path.getsize(filename) + ' ' + filename) + ' ' + new_dest + ' ' + dest_ports)
        userResponse = s.recv(WIDTH)
        if userResponse[:2] == 'OK':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(WIDTH)
                s.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(WIDTH)
                    s.send(bytesToSend)
        print 'File sent'
        con.close()
        print 'Conection closed'


def recieve(s, table, id):
    '''
    EL server escucha, el cliente puede hacer 4 solicitudes al servidor
    HELLO, TO, SEND, BYE
    HELLO: registra al Cliente y recibe el puerto donde el cliente se va a poner a escuchar
    TO: es una solicitud para averiguar la direccion de un cliente especifico al que el cliente le quiera enviar un archivo
    SEND: avisa al servidor que va a recibir un archivo, puede que el  mensaje sea para el servidor o para otro nodo (cliente)
    BYE: Le dice adios al servidor y el cliente cierra la conexion
    '''
    while True:
        # escucha hasta que le venga algo
        data = s.recv(WIDTH)
        if data[:5] == 'HELLO':
            # solicitud HELLO
            print('Got HELLO from Client')
            tmp = data.split(' ')
            listen_port = tmp[1]
            table.getClient(id).setListenPort(listen_port)
            s.send("HELLO ")
        if data[:2] == 'TO':
            # solicitud TO
	        print('Got TO from Client')
            tmp_data = data.split(' ')
            to = tmp_data[1]
            know_client = table.knowClient(to) 
            if tmp_data[1] == servrIP():
                print ("Client asking for me")
                s.send("ROUTE " + tmp_data[1] + ' ' + str(PORT))
            elif know_client != -1:
                print("Client asking for someone else")
                s.send("ROUTE " + table.getClient(know_client).getIP() + " " + table.getClient(know_client).getListenPort())
            else:
                print("Server doesn't recognize this host " + tmp_data[1])

        if data[:4] == 'SEND':
            # solicitud SEND
            # descempaqueta el mensaje
            tmp_data = data.split(' ')
            filesize = long(tmp_data[1])
            filename = tmp_data[2]
            if len(tmp_data) == 3:
                to_who = ''
                ports = ''
            else:
                to_who = tmp_data[3]
                ports = tmp_data[4]

            print "Got File" + filename + ", " + str(filesize) + "Bytes from client"
            # Confirmar que lo recibio
            s.send('OK')
            #table.printTable()
            # Escribir el archivo en el directorio del cliente
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
            print "File recieved!"
	    f.close()
	    tmp = to_who.split('/')

            if tmp[0] == '':
                print "Server recieved a file from client"
            elif len(tmp) >= 1:
                ip = tmp[0]
                index = table.getIndex(ip)
                #Revisar esta
                if index != -1:
                    dest_ports = ports.split('/')
                    sendFile(table, id, index, name, tmp[1:], dest_ports[1:], dest_ports[0])
                else:
                    print print("Server doesn't recognize this host " + ip)
            else:
                print "Message Error"

        if data[:3] == 'BYE':
            #Solicitud BYE
            print "Got BYE from Client"


def main():

    print "ServerController"

    if not os.path.isdir('clients'):
        os.mkdir('clients')

    # Tabla de clientes
    clients = ClientsTable()

    # Puerto en el que va a escuchar
    port = 12345
    allowed_clients = 25

    # Iniciamos Servidor
    server = Server(port)
    server.bind()
    server.listen(allowed_clients)
    count = 0

    while True:
        # Escuchando por nuevas conexiones
        con, addr = server.accept()
        print "Got connection from " + addr[0] + ":" + str(addr[1])

        # Nuevo cliente
        client = Client(str(count), addr[0], addr[1], con)

        # Si ya es un cliente solo se actualiza la informacion
        if clients.isClient(client):
            index = clients.getID(client)
            clients.update(client, index)
        else:
            print("Got new Client")
            client.setID(count)
            count += 1
            clients.add(client)
        # crea nueva carpeta si no existe
	    if not os.path.exists('clients/'+client.getIP()+'/'):
            	os.mkdir('clients/'+client.getIP()+'/')
        index = clients.getID(client)
        # crea un nuevo hilo para el cliente
        t = threading.Thread(target=recieve, args=(client.getCon(), clients, index))
        t.start()

    server.close()


if __name__ == '__main__':
    main()
