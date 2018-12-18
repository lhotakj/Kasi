#!/usr/bin/python3
# -*- coding: utf-8 -*-

from kasi import Client
from datetime import datetime, timedelta



if __name__ == '__main__':


    client = Client.Client(host='localhost', port=5000)

    client.reset()

    client.set("D1", "Nonssssssssse", domain="X")
    print(str(client.get("D1", domain="X")))

    client.set("list", ['a', 'd'], timedelta(seconds=1))
    client.set("text", 'AHOJ', timedelta(hours=1), domain="default")
    client.set("unicode1", u'2H₂ + O₂ ⇌ 2H₂O, R = 4.7 kΩ, ⌀ 200 mm')
    client.set("unicode2", u'ก ข ฃ ค ฅ ฆ ง จ ฉ ช ซ ฌ ญ ฎ ฏ ฐ ฑ ฒ ณ ด ต ถ ท ธ น บ ป ผ ฝ พ ฟ ภ ม ย ร ฤ ล ฦ ว ศ ษ ส ห ฬ อ ฮ ฯ ะ ั า ำ ิ ี ึ ื ุ ู ฺ ฿ เ แ โ ใ ไ ๅ ๆ ็ ่ ้ ๊ ๋ ์ ํ ๎ ๏ ๐ ๑ ๒ ๓ ๔ ๕ ๖ ๗ ๘ ๙ ๚ ๛')

    print(str(client.get("list")))
    print(str(client.get("unicode1")))
    print(str(client.get("unicode2")))
    print(str(client.get("hovni")))

    client.delete("D1", domain="X")
    print(str(client.stats()))

    #    print("==PERF==")
    #    start = datetime.now().timestamp()
    #    for x in range(0,1000):
    #        client.SetCache("hi"+str(x), "2545646")
    #        client.GetCache("hi"+str(x))
    #    end = datetime.now().timestamp()
    #    print("100 connections in " + str(end - start))

