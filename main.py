from queue import Queue
from core.task import *
#from com import Interface

class Cogitron:
    pass

if __name__ == '__main__':
    print('Initializing Cogitron...')
    com = None
    tasks = Queue()
    tasks.put(TaskDriveForward('Take over the world'))
    t = tasks.get()
    t.execute()