from threading import Thread
import subprocess, sys, os, signal, select, time

class Process(object):

    def __init__(self, info):
        self.info = info
        self.thread = None
    
    def isRunning(self):
        return self.thread is not None and self.thread.running

    def start(self):
        if self.isRunning():
            return
        
        self.thread = ProcessThread(self.info)
        self.thread.start()
    
    def stop(self):
        if not self.isRunning():
            return
        
        self.thread.stop()

class ProcessThread(Thread):

    def __init__(self, info):
        Thread.__init__(self)

        if isinstance(info, str):
            info = str.split(' ')

        self.daemon = True
        self.running = False
        self.info = info
        self.process = None
        self.stopped = False
    
    def isRunning(self):
        return self.process is not None

    def run(self):
        self.running = True
        
        while not self.stopped:
            self.process = subprocess.Popen(self.info)
            self.process.wait()
        
        self.running = False
        
    def stop(self):
        if self.process:
            self.process.kill()

        self.process = None
        self.stopped = True

class ProcessHandler(object):
    
    def __init__(self):
        self.processes = {}
    
    def createProcess(self, info, name):
        if name not in self.processes:
            self.processes[name] = Process(info)
    
    def isRunning(self, name):
        return name in self.processes and self.processes[name].isRunning()

    def startProcess(self, name):
        if name in self.processes:
            self.processes[name].start()
    
    def stopProcess(self, name):
        if name in self.processes:
            self.processes[name].stop()
    
    def toggleProcess(self, name):
        if name in self.processes:
            process = self.processes[name]
            
            if process.isRunning():
                process.stop()
                return False
            else:
                process.start()
                return True
         
        return None