from pyHook import HookManager
from win32gui import PumpMessages, PostQuitMessage
from threading import Thread

class KeystrokeWatcher(object):

    def __init__(self, functions):
        self.queue = []
        self.functions = functions
        self.calculateQueueMaxSize()

        self.hookMan = HookManager()
        self.hookMan.KeyDown = self.onKeyDown
        self.hookMan.HookKeyboard()
    
    def calculateQueueMaxSize(self):
        self.queueMaxSize = 0
        
        for function in self.functions:
            size = len(function[0])
            
            if size > self.queueMaxSize:
                self.queueMaxSize = size

    def onKeyDown(self, event):
        if len(self.queue) == self.queueMaxSize:
            del self.queue[-1]

        self.queue.insert(0, event.KeyID)
        self.checkQueue()

        return True

    def checkQueue(self):
        for pair in self.functions:
            keys, func = pair
            
            if len(self.queue) >= len(keys):
                found = True

                for i, key in enumerate(keys):
                    if self.queue[i] != key:
                        found = False
                        break
                
                if found:
                    func()

    def shutdown(self):
        PostQuitMessage(0)
        self.hookMan.UnhookKeyboard()

class KeystrokeThread(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.functions = []
    
    def addFunction(self, keys, func):
        keys.reverse()
        self.functions.append((keys, func))

    def run(self):
        self.watcher = KeystrokeWatcher(self.functions)
        PumpMessages()