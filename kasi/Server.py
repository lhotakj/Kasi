import sys
import socket
from Kasi import Client
from Kasi import Storage

def start_server(host=None, port=5000, connections=5):
    # get the hostname
    if not host:
        host = socket.gethostname()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get the instance
    server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    server_socket.bind((host, port))  # bind host address and port together
    server_socket.listen(connections)

    sys.stderr.write('Server up and running and waiting on {port} ... \n'.format(port=str(port)))
    sys.stdout.flush()

    storage = Storage.Storage()

    while True:

        try:

            conn, address = server_socket.accept()  # accept new connection

            sys.stdout.write("Connection from: " + str(address) + "\n")
            sys.stdout.flush()

            # receive data stream.
            data = Client.Client.receive_all(conn)
            #sys.stdout.write("Received: " + str(data).replace("\n","|") + "\n")

            #print(storage.Dump())
            #if not data:
            #    break

            if data.startswith("D"):
                conn.send(str("0\n" + str(storage.dump())).encode())  # send data to the client
            elif data.startswith("S"):
                data = data[1:]
                lines = data.split("\n")
                storage.set(lines[0], lines[1])
                sys.stdout.write("SET {key} \n".format(key=lines[0]))
                sys.stdout.flush()
                conn.send(("0\n" + data).encode())  # send data to the client
            elif data.startswith("G"):
                data = data[1:-1]
                sys.stdout.write("GET {key} \n".format(key=data))
                sys.stdout.flush()
                r = storage.get(data)
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
    start_server()

