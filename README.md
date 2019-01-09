# Kasi
Kasi means is Shona language "speed". It's a *cache server* implementation similar to `redis`. I decided to write this code to serve a simple caching server to help me to store persisent data such as sessions for a python web server. The intention is not to compete `redis` or `memcached`, but to provide a lightweight solution for cases where you can't install software. When running complex tests, `Kasi` is about 2-3x slower than `redis`, the difference is noticeable only when executing hundreds of thousands requests; the performance should be sufficient for basic use cases.

The cache server supports storing of any type of object, it's not limited to `str` like `redis`. There's build-in algortithm to perform operation with strings much faster.

The server can host multiple so called domains (like db in `redis`). If not specificed, the default domain `default` is be used. Deamon mode is not available yet, coming soon :)

Basic methods of the client are as follows:
* `.set(name, value, timedelta=None, domain="default")` - stores a key with `name` and `value` with expiration `timedelta` in domain `domain`. Value can be any Python object.
* `.get(name, domain="default")` - gets the value of key `name`. If the `key` doesn't exists or has expired, returns `None`
* `.delete(name, domain="default")` - removes the key `name`.
* `.reset()` - resets server. Note all domains got purged. *TODO* optional parameter `domain`
* `.shutdown()` - shutdowns server. In case you want take control over the process.

# Requirements
* Python 3.6+ (Python 2 support is currently ongoing)
* 3pp dependencies

## Demo
### Server
Start `Kasi` server bound to `0.0.0.0` in one console
```
from kasi import Server
Server.start_server(host='0.0.0.0', port=5000)
```

### Client
and run this code in another console. 
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
See folder [demo](https://github.com/lhotakj/Kasi/tree/master/demo) to run this code. You can also try `performance.py` to see the difference between `Kasi` and `redis`.

[![CircleCI](https://circleci.com/gh/lhotakj/Kasi/tree/master.svg?style=svg&circle-token=3b00590f1211a956d5ab9d210c0ff59ea10b19d7)](https://circleci.com/gh/lhotakj/Kasi/tree/master)
 [![Known Vulnerabilities](https://snyk.io/test/github/lhotakj/Kasi/badge.svg)](https://snyk.io/test/github/lhotakj/Kasi/) 
