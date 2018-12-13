import sys
import socket
from datetime import datetime

def recvall(sock):
    BUFF_SIZE = 4096  # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data.decode()

class Storage(object):

    def __init__(self):
        self.__data = {}

    def Set(self, name, value):
        self.__data[name] = [value, datetime.utcnow().timestamp()]

    def Get(self, name):
        if name in self.__data:
            return self.__data[name][0]
        return "None"

    def Dump(self):
        return self.__data


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get the instance
    server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(5)

    sys.stderr.write('Server up and running and waiting on {port} ... \n'.format(port=str(port)))
    sys.stdout.flush()

    storage = Storage()

    while True:

        try:

            conn, address = server_socket.accept()  # accept new connection

            sys.stdout.write("Connection from: " + str(address) + "\n")
            sys.stdout.flush()

            # receive data stream.
            data = recvall(conn)
            #sys.stdout.write("Received: " + str(data).replace("\n","|") + "\n")

            #print(storage.Dump())
            #if not data:
            #    break

            if data.startswith("D"):
                conn.send(str("0\n" + str(storage.Dump())).encode())  # send data to the client
            elif data.startswith("S"):
                data = data[1:]
                lines = data.split("\n")
                storage.Set(lines[0], lines[1])
                sys.stdout.write("SET {key} \n".format(key=lines[0]))
                sys.stdout.flush()
                conn.send(("0\n" + data).encode())  # send data to the client
            elif data.startswith("G"):
                data = data[1:-1]
                sys.stdout.write("GET {key} \n".format(key=data))
                sys.stdout.flush()
                r = storage.Get(data)
                conn.send(("0\n" + r).encode())  # send data to the client
            elif data.startswith("Q"):
                conn.send(("0\n" + data).encode())  # send data to the client
                sys.stdout.write("QUIT\n")
                sys.stdout.flush()
                conn.close()  # close the connection
                sys.stdout.write("Shutting down server ...\n")
                sys.stdout.flush()
                break

        except KeyboardInterrupt:
            sys.stdout.write("[CTRL+C detected]\n")
            sys.stdout.flush()
            conn.close()
            sys.stdout.write("Shutting down server ...\n")
            sys.stdout.flush()
            exit()

        finally:
            conn.close()


if __name__ == '__main__':
    server_program()

