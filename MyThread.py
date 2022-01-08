# Python program raising 
# exceptions in a python 
# thread 

import threading 
import ctypes 
import time 

from pymouse import PyMouse
from win32api import GetSystemMetrics
from random import randint
from time import sleep,ctime,time

# 定时器执行程序
def MouseMoveTimer(width,height,cycle,m):
    while True:
        x = randint(0, width)
        y = randint(0, height)
        m.move(x, y)
        sleep(cycle)
        print("mouse walk %s" %  ctime(time()))

class thread_with_exception(threading.Thread): 
    def __init__(self, cycle = 5): 
        threading.Thread.__init__(self)
        self.cycle = cycle 
        self.m = PyMouse()
        self.width = GetSystemMetrics(0)
        self.height = GetSystemMetrics(1)

    def run(self):
    # target function of the thread class 
        try: 
            MouseMoveTimer(self.width,self.height,self.cycle,self.m)
        finally: 
            pass

    def get_id(self): 
    # returns id of the respective thread 
        if hasattr(self, '_thread_id'): 
            return self._thread_id 
        for id, thread in threading._active.items(): 
            if thread is self: 
                return id

    def raise_exception(self): 
        thread_id = self.get_id() 
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
        ctypes.py_object(SystemExit)) 
        if res > 1: 
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
            print('Exception raise failure') 
        else:
            return

    def stop_thread(self):
        print("thread ready to stop %s" %  ctime(time()))
        self.raise_exception() 
        self.join() 
        print("thread stopped %s" %  ctime(time()))
	
if __name__ == '__main__':
    t1 = thread_with_exception(1) 
    t1.start() 
    sleep(10) 
    t1.stop_thread() 