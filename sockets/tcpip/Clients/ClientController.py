from Conection import Conection

WIDTH = 1024


def hello(con):
    #print ("Send HELLO")
    con.send('HELLO ')
    data = con.recv(WIDTH)

    if data[:5] == 'HELLO':
        print('Server say HELLO')
    else:
        print("Something is wrong")


def by(con):
    con.send('BY ')
    #data = con.recv(WIDTH)

    #if data[:2] == 'BY':
    print('Server say BY')
    #else:
    #    print("Something is wrong")
    con.close()


def requestIP(con, ip):
    con.send('TO ' + ip)
    
def main():

    host = "127.0.0.1"
    port = 12345

    con = Conection(port, host)
    con.connect()

    hello(con.getsocket())
    by(con.getsocket())

    #filename = raw_input("Filename -> ")
    #print("Filename:" + filename)

    #print "K"


if __name__ == '__main__':
    main()