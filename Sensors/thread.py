import threading
from random import randint
from threading import Thread
import time

threadLock = threading.Lock()


class IlMioThread(Thread):
    data = {}
    value = 0
    data2 = {}
    def __init__(self, data, value):
        Thread.__init__(self)
        self.data = data
        self.value = value

    def run(self):
        if self.value is None:
            for count in range(0, len(self.data['Sensors'])):
                thread = IlMioThread(self.data, count)
                print("Thread ")
                thread.start()
        else:
            t = time.time()
            internally = self.data['Sensors'].__getitem__(self.value)['Interval']
            while True:
                s = time.time()
                tempo = int(s - t)
                if internally == tempo:
                    IlMioThread.setSensor(self.data['Sensors'].__getitem__(self.value))
                    threadLock.acquire()
                    #sendData(self.data)
                    threadLock.release()
                    t = s
                    s = time.time()

    def setSensor(self):
        self['Value'] = randint(1, 10)
        return self
