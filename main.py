from queue import Queue
from core.task import *
import threading
#from com import Interface

class Cogitron:
    def __init__(self, emulate_hardware=False, verbose=False):
        self.shutdown = False
        self.verbose = verbose
        self.com = None
        self.tasks = Queue()
        def task_spam(cog):
            for _ in range(8):
                cog.tasks.put(TaskDriveForward(cog, debug_msg='thread 1'))
                time.sleep(0.1)
            time.sleep(30)
            cog.tasks.put(TaskDriveForward(cog, debug_msg='thread 1, final'))
                
        th1 = threading.Thread(target=task_spam, args=(self,))
        th2 = threading.Thread(target=lambda cog : cog.tasks.put(TaskDriveForward(cog, debug_msg='thread 2')), args=(self,)) 
        th3 = threading.Thread(target=lambda cog : cog.tasks.put(TaskDriveForward(cog, debug_msg='thread 3')), args=(self,)) 
        th3.start()
        th1.start()
        th2.start()
        self.tasks.put(TaskDriveForward(self))
        self.tasks.put(TaskDriveForward(self))
        self.tasks.put(TaskDriveForward(self))
        #self.tasks.put(TaskShutdown(self))
        print('Initialization done!')
        
    def run(self):
        print('Starting execution loop')
        while not self.shutdown:
            if self.tasks.empty():
                print('Task queue is empty, sleeping...')
                time.sleep(1.0)
            else:
                t = self.tasks.get()
                t.execute()

                if self.verbose: print('Task execution time: {:.4f}s'.format(t.exec_time) + (', debug_msg="{}"'.format(t.debug_msg) if t.debug_msg else ''))

if __name__ == '__main__':
    print('Initializing Cogitron...')
    cogitron = Cogitron(verbose=True)
    cogitron.run()