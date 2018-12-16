# -*- coding: utf-8 -*-

import sys
import socket
from kasi import Client
from kasi import Storage
import datetime
import os


def log(log_type, text, noeof=False):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
    pid = str(os.getpid())
    if noeof:
        e = ""
    else:
        e = "\n"
    sys.stdout.write("[{now}] [{pid}] [{log_type}] {text}{e}".format(now=now, pid=pid, log_type=log_type.upper(), text=text, e=e))
    sys.stdout.flush()

def logend(text):
    sys.stdout.write("{text}\n".format(text=text))
    sys.stdout.flush()


def start_server(host=None, port=5000, connections=5, domain="default"):
    # get the hostname
    if not host:
        host = 'localhost'

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get the instance
    server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((host, port))  # bind host address and port together
        server_socket.listen(connections)
    except Exception as e:
        logme("ERROR", str(e))
        exit(1)

    log("INFO", 'Server "{server_name}" up and running and waiting on {host}:{port} ...'.format(host=host, port=str(port), server_name="Kasi"))
    log("INFO", 'Press <Ctrl+C> to stop the server.')

    storage = Storage.Storage()

    conn = None
    while True:

        try:

            conn, address = server_socket.accept()  # accept new connection

            log("INFO", "Connection from: " + str(address))

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
                name = lines[0]
                domain = lines[1]
                exp = lines[2]
                value = lines[3]
                res = storage.set(name, exp, value, domain)
                log("INFO", "SET [{domain}].[{key}] ".format(key=name, domain=domain), noeof=True)
                if res == "0":
                    logend("OK")
                    rc = res
                else:
                    logend("ERROR: " + res)
                    rc = res
                conn.send((rc + "\n").encode())  # send data to the client

            elif data.startswith("G"):
                data = data[1:]
                lines = data.split("\n")
                name = lines[0]
                domain = lines[1]
                log("INFO", "GET [{domain}].[{key}] ".format(key=name, domain=domain), noeof=True)
                r = storage.get(name, domain)
                if not r:
                    conn.send("1\n\n".encode())  # 1 - not found
                    logend("ERROR: Key in given domain not found")
                else:
                    conn.send(("0\n" + r).encode())  # send data to the client
                    logend("OK")

            elif data.startswith("X"):
                data = data[1:]
                lines = data.split("\n")
                name = lines[0]
                domain = lines[1]
                res = storage.delete(name, domain)
                log("INFO", "DEL [{domain}].[{key}] ".format(key=name, domain=domain), noeof=True)
                if res == "0":
                    logend("OK")
                    rc = res
                else:
                    logend("ERROR: " + res)
                    rc = res
                conn.send((rc + "\n").encode())  # send data to the client

            elif data.startswith("Q"):
                conn.send(("0\n").encode())  # send data to the client
                log("INFO", "Shutting down server")
                conn.close()  # close the connection
                break

            elif data.startswith("R"):
                log("INFO", "Resetting the cache")
                res = storage.reset()
                conn.send(("0\n").encode())  # send data to the client
                conn.close()  # close the connection

            elif data.startswith("? "):
                log("INFO", "Sending stats")
                res = storage.stats()
                conn.send(("0\n" + res).encode())  # send data to the client
                conn.close()  # close the connection

        except KeyboardInterrupt:
            log("WARN", "<CRTL+C> Detected.")
            if conn:
                conn.shutdown(1)
                conn.close()
                log("INFO", "Shutting down server")
            exit(0)

        finally:
            pass


if __name__ == '__main__':
    start_server()

