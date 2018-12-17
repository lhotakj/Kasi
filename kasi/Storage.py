import datetime
from datetime import datetime

class Storage(object):

    def __init__(self):
        self.__data = {}  # { 'default': {"key1":[ exp1, value1]}, 'domain2': {"key1":[ exp1, value1] }

    def set(self, name, value, expiration=None, domain="default"):
        try:
            if domain not in self.__data:
                self.__data.update({domain: {}})
            self.__data[domain][name] = [value, expiration]
            return "0"
        except Exception as e:
            return str(e)

    def get(self, name, domain):
        if domain in self.__data:
            rec = self.__data[domain]
            if name in rec:
                # exp in self.__data[name][0]
                if rec[name][0]:  # exp is set
                    now = datetime.now().timestamp()
                    if now > float(rec[name][0]):
                        try:
                            del rec.remove[name]  # remove from cache
                        except Exception as e:
                            pass
                        return None
                return rec[name][1]
        return None

    def delete(self, name, domain):
        try:
            if domain not in self.__data:
                return "Domain does not exists"
            else:
                if name not in self.__data[domain]:
                    return "Key does not exists"
                del self.__data[domain][name]
                return "0"
        except Exception as e:
            return str(e)


    def reset(self):
        self.__data = {}
        return "0"

    def stats(self):
        r = {'domains': None, 'started': 'x', 'hits': 0}
        for domain in self.__data:
            r.update({"domains": {}})
            r["domains"][domain] = {'count': 1}
        return str(r)



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

