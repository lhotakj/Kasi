#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import socket
import sys
import codecs
import pickle
import base64
import datetime
import time
import sys


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

    # Python < 3.3 compatibile
    @staticmethod
    def timestamp(date):
        return time.mktime(date.timetuple())

    @staticmethod
    def receive_all(sock):
        BUFF_SIZE = 512  # 4 KiB
        data = b''
        while True:
            part = sock.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                # either 0 or end of data
                break
        return data.decode()

    def recvall(self):
        BUFF_SIZE = 512  # 4 KiB
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
        return s[0], s[1]


    def MessageSet(self, name, value, domain, timedelta=None):
        if not timedelta:
            expiration = ""
        else:
            expiration = self.timestamp(datetime.datetime.now().__add__(timedelta))
        return "S" + name + "\n" + domain + "\n" + str(expiration) + "\n" + value

    def MessageGet(self, name, domain):
        return "G" + name + "\n" + domain + "\n"

    def MessageDelete(self, name, domain):
        return "X" + name + "\n" + domain + "\n"

    def MessageDebug(self):
        return "D"

    def MessageReset(self):
        return "R "

    def MessageQuit(self):
        return "Q"

    def MessageStats(self):
        return "? "

    def Open(self):
        self.__client_socket = socket.socket()      # instantiate
        self.__client_socket.connect((self._host, self._port))  # connect to the server

    def Close(self):
        self.__client_socket.close()  # close the connection

    def GetCache(self, name, domain="default"):
        name = name.replace("\n", "").replace("\t", "")
        self.Open()
        code, value = self.send(self.MessageGet(name, domain))
        self.Close()
        datatype = value[:1]
        value = value[2:]
        if code != "0":
            return None
        if datatype == "s":
            return value
        else:
            return pickle.loads(base64.b64decode(value))

    def SetCache(self, name, value, timedelta=None, domain="default"):
        name = name.replace("\n", "").replace("\t", "")

        if type(value) is str:
            name = "s" + name
            dump = value
        else:
            name = "x" + name
            dump = base64.b64encode(pickle.dumps(value)).decode()

        self.Open()
        # dump = base64.b64encode(pickle.dumps(value)).decode()
        code, value = self.send(self.MessageSet(name, dump, domain, timedelta))
        self.Close()
        return code

    def DeleteCache(self, name, domain="default"):
        name = name.replace("\n", "").replace("\t", "")
        self.Open()
        code, value = self.send(self.MessageDelete(name, domain))
        self.Close()
        return code

    def ResetCache(self):
        self.Open()
        code, value = self.send(self.MessageReset())
        self.Close()
        return code

    def Debug(self):
        self.Open()
        code, value = self.send(self.MessageDebug())
        self.Close()
        return value.encode()

    def Stats(self):
        self.Open()
        code, value = self.send(self.MessageStats())
        self.Close()
        return value.encode()




