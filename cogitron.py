from queue import Queue
from core.task import *
import threading
from com.communicator import Communicator

class Cogitron:
    def __init__(self, emulate_hardware=False, verbose=False):
        self.shutdown = False
        self.verbose = verbose
        self.com = Communicator('real')

        time.sleep(2)
        while True:
            msg = 'setMotor;0;80'
            print('sending', msg)
            self.com.sendMessage(msg)
            time.sleep(0.2)
        
            msg = 'setMotor;0;0'
            print('sending', msg)
            self.com.sendMessage(msg)
            time.sleep(0.2)
        
        #msg = 'setMotors;80;80;0'
        #print('sending', msg)
        #self.com.sendMessage(msg)
        #time.sleep(0.1)

        while True:
            time.sleep(0.1)
            rec = self.com.receiveMessage()
            #print('received {} (len={})'.format(bytes(rec, 'utf-8'), len(rec)))
            print('received {} (len={})'.format(rec, len(rec)))

        self.tasks = Queue()
        """
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
        """
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