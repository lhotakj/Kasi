#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import datetime
import sys
from kasi import Client

if __name__ == '__main__':

    # instantiate the client
    client = Client.Client(host='localhost', port=5000)

    test_list = ['a', 'd']
    test_str_ascii = 'hi'
    test_str_unicode = '2H₂ + O₂ ⇌ 2H₂O, R = 4.7 kΩ, ⌀ 200 mm'

    print("Testing SET [list] ...")
    client.SetCache("test_list", test_list)

    print("Testing SET [str_ascii] ...")
    client.SetCache("test_str_ascii", test_str_ascii)

    #print("Testing SET [str_unicode] ...")
    #client.SetCache("test_str_unicode", test_str_unicode)

    print("Testing DEBUG ...")
    debug = client.Debug()
    print(debug)


    print("Testing GET [list] ...")
    read_list = client.GetCache("test_list")
    if read_list != test_list:
        print("Failed")
        exit(1)

    print("Testing GET [str_ascii] ...")
    read_str_ascii = client.GetCache("test_str_ascii")
    if read_str_ascii != test_str_ascii:
        print("Failed")
        exit(1)

    #print("Testing GET [str_unicode] ...")
    #read_str_unicode = client.GetCache("test_str_unicode")
    #if read_str_unicode != test_str_unicode:
    #    print("Failed")
    #    exit(1)

    load_test = 1000
    start = datetime.datetime.now().timestamp()
    for x in range(0, load_test):
        client.SetCache("load_test_"+str(x), str(x))
        client.GetCache("load_test_" + str(x))
    end = datetime.datetime.now().timestamp()
    sys.stdout.write(str(load_test) + " connections in " + str(end - start))


