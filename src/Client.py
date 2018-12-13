import socket
import sys
import datetime
import codecs
import pickle

class Client(object):

    def __init__(self):
        pass


    def recvall(self):
        BUFF_SIZE = 4096  # 4 KiB
        data = b''
        while True:
            part = self.__client_socket.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                # either 0 or end of data
                break
        return data.decode()


    def send(self, message):
        #sys.stdout.write('Sending message : ' + message)
        #sys.stdout.write('\n---')
        #sys.stdout.flush()
        self.__client_socket.send(message.encode())  # send message
        data = self.recvall()
        #sys.stdout.write('Received from server: ' + data)
        #sys.stdout.write('\n---')
        s = data.split("\n")
        sys.stdout.flush()
        return s[0], s[1]


    def MessageSet(self, name, value):
        return "S" + name + "\n" + value


    def MessageGet(self, name):
        return "G" + name + "\n"


    def MessageDebug(self):
        return "D"


    def MessageQuit(self):
        return "Q"

    def Open(self):
        host = socket.gethostname()                 # as both code is running on same pc
        port = 5000                                 # socket server port number
        self.__client_socket = socket.socket()      # instantiate
        self.__client_socket.connect((host, port))  # connect to the server

    def Close(self):
        self.__client_socket.close()  # close the connection


    def GetCache(self, name):
        self.Open()
        code, value = self.send(client.MessageGet(name))
        self.Close()
        return pickle.loads(codecs.decode(value.encode(), "base64"))

    def SetCache(self, name, value):
        self.Open()
        dump = codecs.encode(pickle.dumps(value), "base64").decode()
        code, value = client.send(self.MessageSet(name, dump))
        self.Close()
        return code


if __name__ == '__main__':

    client = Client()
    client.SetCache("pozdrav", ['a', 'd'])
    client.SetCache("pozdrav5", 'AHOJ')

    print("\n-------------------")
    print(str(client.GetCache("pozdrav")))
    print(str(client.GetCache("pozdrav5")))
    print("\n-------------------")

    start = datetime.datetime.now().timestamp()
    for x in range(0, 1):
        client.SetCache("ahoj"+str(x), "1")
        client.GetCache("ahoj" + str(x))
    end = datetime.datetime.now().timestamp()
    sys.stdout.write("100 connections in " + str(end - start))

    #client.Close()

    # - NORMAL ----------------------------------
#    start = datetime.datetime.now().timestamp()
#    for x in range(0,100):
#        client.send(client.MessageSet("ahoj"+str(x), "1"))
#        client.send(client.MessageSet("hi", "2545646"))
#        client.send(client.MessageGet("hi"))
#    end = datetime.datetime.now().timestamp()




 #   sys.stdout.write("\n\n")
 #   sys.stdout.write("100 connections in " + str(end - start))
 #   sys.stdout.flush()


    #@client.send(client.MessageDebug())
    #client.send(client.MessageQuit())
    #client.Close()


