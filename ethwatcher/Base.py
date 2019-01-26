from .KeystrokeWatcher import KeystrokeThread
from .ProcessHandler import ProcessHandler
from .ToastManager import ToastManager
import webbrowser, json, sys, os, time

class Base(object):

    def __init__(self):
        self.processInfo = self.loadProcessInfo()
        self.watcherThread = KeystrokeThread()
        self.watcherThread.addFunction([162, 91], lambda: self.toggleProcess('ethereum'))
        self.watcherThread.addFunction([162, 160], lambda: self.getStatus('ethereum'))
        self.watcherThread.addFunction([91, 164], lambda: webbrowser.open(self.processInfo['hashLink']))
        self.watcherThread.start()
        
        self.toastManager = ToastManager()
        self.toastManager.start()
        self.processHandler = ProcessHandler()
        self.processHandler.createProcess(self.processInfo['process'], 'ethereum')
        self.processHandler.startProcess('ethereum')
        
        while True:
            try:
                time.sleep(1)
            except:
                return
    
    def getLog(self, name):
        return os.path.join(os.getcwd(), name + '.log')

    def getProcessFile(self):
        return os.path.join(os.getcwd(), 'process.json')
    
    def loadProcessInfo(self):
        filename = self.getProcessFile()
        
        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                json.dump({'process': [], 'hashLink': 'https://nicehash.com'}, file)
            
            print('Saved process file to {0}.'.format(filename))
            sys.exit()
        
        with open(filename, 'r') as file:
            return json.load(file)

    def toggleProcess(self, name):
        if (not self.toastManager) or self.toastManager.isShowing():
            return

        if self.processHandler.toggleProcess(name):
            self.toastManager.show('Watcher', 'Started %s!' % name.capitalize())
        else:
            self.toastManager.show('Watcher', 'Stopped %s!' % name.capitalize())
    
    def getStatus(self, name):
        if (not self.toastManager) or self.toastManager.isShowing():
            return
        
        if self.processHandler.isRunning(name):
            self.toastManager.show('Watcher', '%s is running!' % name.capitalize())
        else:
            self.toastManager.show('Watcher', '%s is not running.' % name.capitalize())

if __name__ == '__main__':
    base = Base()