import datetime
from datetime import datetime

class Storage(object):

    def __init__(self):
        self.__data = {}  # { 'default': {"key1":[ exp1, value1]}, 'domain2': {"key1":[ exp1, value1] }

    def set(self, name, value, expiration=None, domain="default"):

        self.__data[domain] = {name: [value, expiration]}
        #self.__data[name] = [value, expiration]

    def get(self, name, domain="default"):
        if domain in self.__data:
            rec = self.__data[domain]
            if name in rec:
                # exp in self.__data[name][0]
                if rec[name][0]: # exp is set
                    now = datetime.now().timestamp()
                    if now > float(rec[name][0]):
                        try:
                            del rec.remove[name]  # remove from cache
                        except Exception as e:
                            pass
                        return None
                return rec[name][1]
        return None

#        if name in self.__data:
#            # exp in self.__data[name][0]
#            if self.__data[name][0]: # exp is set
#                now = datetime.now().timestamp()
#                if now > float(self.__data[name][0]):
#                    try:
#                        del self.__data.remove[name]  # remove from cache
#                    except Exception as e:
#                        pass
#                    return None
#            return self.__data[name][1]
#        return None

    def dump(self):
        return self.__data

