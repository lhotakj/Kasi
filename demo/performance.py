#!/usr/bin/python3
# -*- coding: utf-8 -*-

from kasi import Client as kasi
from datetime import datetime, timedelta
import redis
import re

# https://pypi.org/project/redis/

if __name__ == '__main__':


    host='10.0.0.108'

    client = kasi.Client(host=host, port=5000)

    client.set('food','x')
    client.set('food', 'x', domain='x')
    start = datetime.now().timestamp()
    for loop in range(0, 100):
        client.set('foo' + str(loop), 'č_barxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' + str(loop))
        client.get('foo' + str(loop))
    end = datetime.now().timestamp()
    print("Kasi 1000 connections in " + str(end - start))
    kasi = end - start

    r = redis.Redis(host=host, port=6379, db=0)
    start = datetime.now().timestamp()
    for loop in range(0, 100):
        r.set('foo'+str(loop), 'č_barxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'+str(loop))
        r.get('foo'+str(loop))
    end = datetime.now().timestamp()
    print("REDIS 1000 connections in " + str(end - start))
    red = end - start

    print("Slow:" + str(float(kasi / red )))
    print(client.stats())


