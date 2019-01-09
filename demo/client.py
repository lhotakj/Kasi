#!/usr/bin/python3
# -*- coding: utf-8 -*-

from kasi import Client
from datetime import datetime, timedelta

if __name__ == '__main__':

    # create an instance of client
    client = Client.Client(host='localhost', port=5000)
    client.reset()
    
    # save string into domain X
    client.set("D1", "test1", domain="X")
    print(str(client.get("D1", domain="X")))

    # save non-trivial object
    client.set("list", ['a', 'd'], timedelta(seconds=1))               # set expiration 1 second
    client.set("text", 'hello', timedelta(hours=1), domain="default")  # set expiration 1 hour and save into domain 'default'
    client.set("unicode1", u'2H₂ + O₂ ⇌ 2H₂O, R = 4.7 kΩ, ⌀ 200 mm')   # store unicode
    client.set("unicode2", u'ก ข ฃ ค ฅ ฆ ง จ ฉ ช ซ ฌ ญ ฎ ฏ ')        # store unicode

    # get them
    print(str(client.get("list")))
    print(str(client.get("text")))
    print(str(client.get("unicode1")))
    print(str(client.get("unicode2")))
    print(str(client.get("not-existing")))    # demonstrate reading non-existing key

    client.delete("D1", domain="X")
    print(str(client.stats()))

    # some performance
    #    print("==PERF==")
    #    start = datetime.now().timestamp()
    #    for x in range(0,1000):
    #        client.SetCache("hi"+str(x), "2545646")
    #        client.GetCache("hi"+str(x))
    #    end = datetime.now().timestamp()
    #    print("100 connections in " + str(end - start))

