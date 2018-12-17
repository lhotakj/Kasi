# -*- coding: utf-8 -*-

import sys
import socket
from kasi import Client
from kasi import Storage
import datetime
import os
import re

_performance_mode = True


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
    global _performance_mode
    # get the hostname
    if not host:
        host = 'localhost'

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get the instance
    server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024)

    try:
        server_socket.bind((host, port))  # bind host address and port together
        server_socket.listen(connections)
    except Exception as e:
        log("ERROR", str(e))
        exit(1)

    log("INFO", 'Server "{server_name}" up and running and waiting on {host}:{port} ...'.format(host=host, port=str(port), server_name="Kasi"))
    log("INFO", 'Press <Ctrl+C> to stop the server.')
    log("INFO", 'Running in mode: ' + str(_performance_mode) )

    storage = Storage.Storage()

    conn = None
    while True:

        try:

            conn, address = server_socket.accept()  # accept new connection

            if not _performance_mode:
                log("INFO", "Connection from: " + str(address))

            data = Client.Client.receive_all(conn)


            if data.startswith("S"):
                lines = data.split("\n")
                #lines = re.split(r'[\n]+', data)

                name = lines[0]
                name = name[1:]
                datatype = name[0]
                name = name[1:]
                domain = lines[1]
                exp = lines[2]
                value = lines[3]
                res = storage.set(name, value, datatype, exp, domain)
                if not _performance_mode:
                    log("INFO", "SET [{domain}].[{key}] type {datatype} ".format(key=name, domain=domain, datatype=datatype), noeof=True)
                if res == "0":
                    if not _performance_mode:
                        logend("OK")
                    rc = res
                else:
                    if not _performance_mode:
                        logend("ERROR: " + res)
                    rc = res
                conn.send((rc + "\n").encode())  # send data to the client

            elif data.startswith("G"):
                data = data[1:]
                lines = data.split("\n")
                #lines = re.split(r'[\n]+', data)

                name = lines[0]
                domain = lines[1]
                if not _performance_mode:
                    log("INFO", "GET [{domain}].[{key}] ".format(key=name, domain=domain), noeof=True)
                r, datatype = storage.get(name, domain)
                if not r:
                    conn.send("1\n\n".encode())  # 1 - not found
                    if not _performance_mode:
                        logend("ERROR: Key in given domain not found")
                else:
                    conn.send(("0\n" + datatype + "\n" + r).encode())  # send data to the client
                    if not _performance_mode:
                        logend("OK")

            elif data.startswith("D"):
                conn.send(str("0\n" + str(storage.dump())).encode())  # send data to the client

            elif data.startswith("X"):
                data = data[1:]
                lines = data.split("\n")
                name = lines[0]
                domain = lines[1]
                res = storage.delete(name, domain)
                if not _performance_mode:
                    log("INFO", "DEL [{domain}].[{key}] ".format(key=name, domain=domain), noeof=True)
                if res == "0":
                    if not _performance_mode:
                        logend("OK")
                    rc = res
                else:
                    if not _performance_mode:
                        logend("ERROR: " + res)
                    rc = res
                conn.send((rc + "\n").encode())  # send data to the client

            elif data.startswith("Q"):
                conn.send(("0\n").encode())  # send data to the client
                if not _performance_mode:
                    log("INFO", "Shutting down server")
                conn.close()  # close the connection
                break

            elif data.startswith("R"):
                if not _performance_mode:
                    log("INFO", "Resetting the cache")
                res = storage.reset()
                conn.send(("0\n").encode())  # send data to the client
                conn.close()  # close the connection

            elif data.startswith("? "):
                if not _performance_mode:
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

