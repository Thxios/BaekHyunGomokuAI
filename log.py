from common import *


class _Logger:
    def __init__(self):
        self.log = []

    def log(self, *args, **kwargs):
        print(*args, **kwargs)

    def silent_log(self, string):
        self.log.append(string)

    def clear(self):
        self.log = []

    def flush(self):
        for log in self.log:
            print('  ' + log)
        self.clear()


Log = _Logger()

