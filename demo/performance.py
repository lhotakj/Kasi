#!/usr/bin/python3
# -*- coding: utf-8 -*-

from kasi import Client
from datetime import datetime, timedelta
import redis

# https://pypi.org/project/redis/

if __name__ == '__main__':

    host='10.0.0.108'

    r = redis.Redis(host=host, port=6379, db=0)
    start = datetime.now().timestamp()
    for loop in range(0, 50):
        r.set('foo'+str(loop), 'barxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        r.get('foo'+str(loop))
    end = datetime.now().timestamp()
    red = end - start
    print("REDIS 1000 connections in " + str(end - start))

    client = Client.Client(host=host, port=5000)
    start = datetime.now().timestamp()
    for loop in range(0, 50):
        client.SetCache('foo'+str(loop), 'barxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        client.GetCache('foo'+str(loop))
    end = datetime.now().timestamp()
    print("Kasi 1000 connections in " + str(end - start))
    kasi = end - start

    print("Slow:" + str(int(kasi / red * 100)))


