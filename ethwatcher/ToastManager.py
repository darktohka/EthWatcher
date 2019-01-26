from win10toast import ToastNotifier
from threading import Thread
from Queue import Queue

class ToastManager(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.toaster = ToastNotifier()
        self.queue = Queue()
        self.showing = False
    
    def isShowing(self):
        return self.showing
        
    def show(self, title, message):
        self.queue.put((title, message))
    
    def run(self):
        while True:
            item = self.queue.get()
            self.showing = True
            self.toaster.show_toast(*item)
            self.showing = False
            self.queue.task_done()