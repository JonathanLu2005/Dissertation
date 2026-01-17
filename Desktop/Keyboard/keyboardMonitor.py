import keyboard 
import time
from collections import deque

class KeyboardMonitor:
    def __init__(self):
        """ Instantiate queue to hold if key has been pressed

        Attributes:
        - KeyQueue (queue[bool]): Queue of if any keys has been pressed

        Returns:
        - None
        """
        self.KeyQueue = deque()

    def OnKey(self, Event):
        """ Method to detect if a key has been pressed and update queue as so
        
        Arguments:
        - Event (keyboard.KeyboardEvent): 

        Returns:
        - None
        """
        if Event.event_type == "down":
            self.KeyQueue.append(True)

    def Live(self):
        """ Generator which returns if a key has been pressed or not

        Returns:
        - None
        """
        keyboard.hook(self.OnKey)
        while True:
            if self.KeyQueue:
                yield self.KeyQueue.popleft()
                self.KeyQueue.clear()
            else:
                yield False 
            time.sleep(1)
        self.Release()

    def Release(self):
        """ Kills code

        Returns:
        - None
        """
        keyboard.unhook_all()