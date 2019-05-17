from Conection import Conection

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


def main():

    host = "172.28.130.42"
    port = 12345

    con = Conection(port, host)
    con.connect()

    hello(con.getsocket())
    ip = requestIP(con.getsocket(), host)
    print ip
    bye(con.getsocket())

    #filename = raw_input("Filename -> ")
    #print("Filename:" + filename)

    #print "K"


if __name__ == '__main__':
    main()
