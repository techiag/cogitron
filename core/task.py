from abc import ABC, abstractmethod

class Task(ABC):
    def __init__(self, com):
        self.com = com

    @abstractmethod
    def execute(self):
        pass

class TaskDriveForward(Task):
    def execute(self):
        print('Driving forward!')