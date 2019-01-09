# Kasi
Easy cache server similar to `redis`. I wrote this code to have a simple caching server which would help me to store persisent data such as session etc. for a web server. It's intention is not to compete `redis` or `memcached` but provide a simple and easy solution when you can't install software.

The server supports storing any object, it's not limited to `str` as `redis`. There's build-in algortithm to perform operation with strings much faster.

Basic methods of the client are as follows:
* `.get()`
* `.set()`
* `.shutdown()`

## How to use

### Server
Start Kasi server bound to `0.0.0.0` in one consoled
```
from kasi import Server
Server.start_server(host='0.0.0.0', port=5000)
```
*TODO* - daemonize is under progress, coming soon

### Client
Run this code in another console. 
```
from kasi import Client
from datetime import datetime, timedelta

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
```

You may shutdown the server by calling. Some more security checks may be implemented in the future
```
client.shutdown() 
```


[![CircleCI](https://circleci.com/gh/lhotakj/Kasi/tree/master.svg?style=svg&circle-token=3b00590f1211a956d5ab9d210c0ff59ea10b19d7)](https://circleci.com/gh/lhotakj/Kasi/tree/master)
