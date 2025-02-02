from abc import ABC, abstractmethod
from timeit import default_timer as timer
import time

class Task(ABC):
    def __init__(self, cogref, debug_msg=None):
        self.cogref = cogref
        self.exec_time = -1
        self.debug_msg = debug_msg

    def execute(self):
        start = timer()
        self.exec_body()
        end = timer()
        self.exec_time = end - start

    @abstractmethod
    def exec_body(self):
        pass

class TaskDriveForward(Task):
    def exec_body(self):
        print('Driving forward!')
        time.sleep(1)

class TaskShutdown(Task):
    def exec_body(self):
        print('Shutting down.')
        self.cogref.shutdown = True
    
class TaskFaceDetect(Task):
    def exec_body(self):
        print('saw a face!')
        time.sleep(10)