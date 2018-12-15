#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import socket
import sys
import codecs
import pickle
import base64
import datetime


class Client(object):

    def __init__(self, host=None, port=5000):
        # get the hostname
        if not host:
            self._host = socket.gethostname()
        else:
            self._host = host
        if not isinstance(port, int):
            raise ValueError('Argument port has to be an integer!')
        self._port = port
        print(self._host)

    @staticmethod
    def receive_all(sock):
        BUFF_SIZE = 4096  # 4 KiB
        data = b''
        while True:
            part = sock.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                # either 0 or end of data
                break
        return data.decode()

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


    def MessageSet(self, name, value, timedelta=None):
        if not timedelta:
            expiration = ""
        else:
            expiration = datetime.datetime.now().__add__(timedelta).timestamp()
        print("S" + name + "\n" + str(expiration) + "\n" + value)
        return "S" + name + "\n" + str(expiration) + "\n" + value


    def MessageGet(self, name):
        return "G" + name + "\n"


    def MessageDebug(self):
        return "D"


    def MessageQuit(self):
        return "Q"

    def Open(self):
        self.__client_socket = socket.socket()      # instantiate
        self.__client_socket.connect((self._host, self._port))  # connect to the server

    def Close(self):
        self.__client_socket.close()  # close the connection


    def GetCache(self, name):
        name = name.replace("\n", "").replace("\t", "")
        self.Open()
        code, value = self.send(self.MessageGet(name))
        self.Close()
        if code != "0":
            return None
        print("NAME:" + name)
        print("CODE:" + code)
        print("value:" + value)
        return pickle.loads(base64.b64decode(value))
        #return pickle.loads(codecs.decode(value.encode(), "base64"))

    def SetCache(self, name, value, timedelta=None):
        name = name.replace("\n","").replace("\t","")
        self.Open()
        dump = base64.b64encode(pickle.dumps(value)).decode()
        #dump = codecs.encode(pickle.dumps(value), "base64").decode()
        code, value = self.send(self.MessageSet(name, dump, timedelta))
        self.Close()
        return code

    def Debug(self):
        self.Open()
        code, value = self.send(self.MessageDebug())
        self.Close()
        return value.encode()





