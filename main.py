from queue import Queue
from core.task import *
#from com import Interface

class Cogitron:
    def __init__(self, emulate_hardware=False, verbose=False):
        self.shutdown = False
        self.verbose = verbose
        self.com = None
        self.tasks = Queue()
        self.tasks.put(TaskDriveForward(self))
        self.tasks.put(TaskDriveForward(self))
        self.tasks.put(TaskDriveForward(self))
        self.tasks.put(TaskShutdown(self))
        
    def run(self):
        while not self.shutdown:
            if self.tasks.empty():
                print('Task queue is empty, sleeping...')
                time.sleep(1.0)
            else:
                t = self.tasks.get()
                t.execute()

                if self.verbose: print('Task execution time: {:.4f}s'.format(t.exec_time))

if __name__ == '__main__':
    print('Initializing Cogitron...')
    cogitron = Cogitron(verbose=True)
    cogitron.run()