# -*- coding: utf-8 -*-

import sys
import socket
from kasi import Client
from kasi import Storage
import datetime
import os
import re

_performance_mode = True
_stats_mode       = True
_stats_started    = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
_stats_get_hit = 0
_stats_set_hit = 0
_stats_get_mis = 0

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

def receive_all(conn):
    BUFF_SIZE = 1024  # 4 KiB
    data = b''
    while True:
        part = conn.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data.decode()

def start_server(host=None, port=5000, connections=5, domain="default"):
    global _performance_mode
    global _stats_get_hit
    global _stats_set_hit
    global _stats_get_mis

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

    try:

        while True:
            conn, address = server_socket.accept()  # accept new connection
            if not _performance_mode:
                log("INFO", "Connection from: " + str(address))

            #data = Client.Client.receive_all(conn)
            data = receive_all(conn)

            if data[0] == "G":
                if _stats_mode: _stats_get_hit += 1
                data = data[1:]
                lines = data.split("\n")
                name = lines[0]
                domain = lines[1]
                r, datatype = storage.get(name, domain)
                if not _performance_mode:
                    log("INFO", "GET [{domain}].[{key}] type={datatype} value={value}".format(key=name, domain=domain, datatype=datatype, value=str(r)), noeof=True)
                if not r:
                    conn.send("1\n\n".encode())  # 1 - not found
                    if _stats_mode: _stats_get_mis += 1
                    if not _performance_mode:
                        logend("ERROR: Key in given domain not found")
                else:
                    conn.send(("0\n" + datatype + "\n" + r).encode())  # send data to the client
                    if not _performance_mode:
                        logend("OK")

            elif data[0] == "S":
                if _stats_mode: _stats_set_hit += 1
                lines = data.split("\n", 3)
                name = lines[0]
                name = name[1:]
                datatype = name[0]
                name = name[1:]
                domain = lines[1]
                exp = lines[2]
                value = lines[3]
                res = storage.set(name, value, datatype, exp, domain)
                if not _performance_mode:
                    log("INFO", "SET [{domain}].[{key}] type={datatype} value={value}".format(key=name, domain=domain, datatype=datatype, value=str(value)), noeof=True)
                if res == "0":
                    if not _performance_mode:
                        logend("OK")
                    rc = res
                else:
                    if not _performance_mode:
                        logend("ERROR: " + res)
                    rc = res
                conn.send((rc + "\n").encode())  # send data to the client

            elif data[0] == "D":
                conn.send(str("0\n" + str(storage.dump())).encode())  # send data to the client

            elif data[0] == "X":
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

            elif data[0] == "Q":
                conn.send(("0\n").encode())  # send data to the client
                if not _performance_mode:
                    log("INFO", "Shutting down server")
                conn.close()  # close the connection
                break

            elif data[0] == "R":
                if not _performance_mode:
                    log("INFO", "Resetting the cache")
                res = storage.reset()
                conn.send(("0\n").encode())  # send data to the client
                conn.close()  # close the connection

            elif data[0:2] == "? ":
                if not _performance_mode:
                    log("INFO", "Sending stats")
                res = storage.stats(started=_stats_started, get_hit=_stats_get_hit, set_hit=_stats_set_hit, get_miss=_stats_get_mis)
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

