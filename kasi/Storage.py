import datetime
from datetime import datetime

class Storage(object):

    def __init__(self):
        self.__data = {}

    def set(self, name, value, expiration=None):
        self.__data[name] = [value, expiration]

    def get(self, name):
        if name in self.__data:
            # exp in self.__data[name][0]
            if self.__data[name][0]: # exp is set
                now = datetime.now().timestamp()
                if now > float(self.__data[name][0]):
                    try:
                        del self.__data.remove[name]  # remove from cache
                    except Exception as e:
                        pass
                    return None
            return self.__data[name][1]
        return None

    def dump(self):
        return self.__data

