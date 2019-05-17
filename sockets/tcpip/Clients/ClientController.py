from Conection import Conection
import os
import socket

WIDTH = 1024


def hello(con):
    con.send('HELLO ')
    data = con.recv(WIDTH)

    if data[:5] == 'HELLO':
        print('Server say HELLO')
    else:
        print("Something is wrong")


def bye(con):
    con.send('BYE ')
    print('Server say BYE')
    con.close()


def requestIP(con, ip):
    con.send('TO ' + ip)
    data = con.recv(WIDTH)
    if data[:5] == 'ROUTE':
        tmp = data.split(' ')
        return tmp[1]
    return '-1'


def sendFile(ip, port, filename):
    dest_ip = ip.split('/')
    new_dest = ''
    host = ''
    if len(dest_ip) == 1:
        # 192.168.1.1
        host = dest_ip[0]
    else:
        # 192.168.1.1/192.168.1.104/192.168.1.130
        host = dest_ip[0]
        for des in dest_ip[1:]:
            new_dest += des + '/'
        new_dest = new_dest[:-1]
        size_ip_path = 2

    if os.path.isfile(filename):

        file_transfer = Conection(port, host)
        file_transfer.connect()
        s = file_transfer.getsocket()

        s.send('SEND ' + str(os.path.getsize(filename)) + ' ' + filename + ' ' + new_dest)

        data = s.recv(WIDTH)
        if data[:2] == 'OK':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(WIDTH)
                s.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(WIDTH)
                    s.send(bytesToSend)
        else:
            print "Error while sending file:" + filename
            s.send("ERROR")
        s.close()


'''
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


'''
'''
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
'''
def main():

    host = "172.28.130.42"
    port = 12345

    con = Conection(port, host)
    con.connect()

    hello(con.getsocket())
    bye(con.getsocket())

    #filename = raw_input("Filename -> ")
    #print("Filename:" + filename)

    #print "K"


if __name__ == '__main__':
    main()