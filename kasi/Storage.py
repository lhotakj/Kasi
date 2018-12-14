import datetime
from datetime import datetime

class Storage(object):

    def __init__(self):
        self.__data = {}

    def set(self, name, value):
        self.__data[name] = [value, datetime.now().timestamp()]

    def get(self, name):
        if name in self.__data:
            return self.__data[name][0]
        return "None"

    def dump(self):
        return self.__data

