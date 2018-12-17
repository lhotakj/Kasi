#!/usr/bin/python3
# -*- coding: utf-8 -*-

from kasi import Client
from datetime import datetime, timedelta
import redis

# https://pypi.org/project/redis/

if __name__ == '__main__':

    r = redis.Redis(host='localhost', port=6379, db=0)
    start = datetime.now().timestamp()
    for loop in range(0, 5000):
        r.set('foo'+str(loop), 'barxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        r.get('foo'+str(loop))
    end = datetime.now().timestamp()
    print("REDIS 1000 connections in " + str(end - start))

    client = Client.Client(host='localhost', port=5000)
    start = datetime.now().timestamp()
    for loop in range(0, 5000):
        client.SetCache('foo'+str(loop), 'barxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        client.GetCache('foo'+str(loop))
    end = datetime.now().timestamp()
    print("Kasi 1000 connections in " + str(end - start))


