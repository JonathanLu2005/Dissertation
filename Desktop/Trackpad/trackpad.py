from pynput import mouse
import time 

class TrackpadMonitor:
    def __init__(self):
        """ Instantiate value to listen for any detections and change attribute if the trackpad has been used

        Attributes:
        - Moved (bool): True if trackpad moved else false
        - Clicked (bool): True if trackpad clicked else false
        - Scrolled (bool): True if trackpad scrolled else false
        - Listener (pynput.mouse.Listener): Listens for trackpad movement, click, or scroll

        Returns:
        - None
        """
        self.Moved = False 
        self.Clicked = False 
        self.Scrolled = False
        self.Listener = mouse.Listener(
            on_move=self.TrackMove,
            on_click=self.TrackClick,
            on_scroll=self.TrackScroll
        )
        self.Listener.start()

    def TrackMove(self, x, y):
        """ Detects if the mouse has been moved

        Arguments:
        - x (int): Cursor x position
        - y (int): Cursor y position

        Returns:
        - None
        """
        self.Moved = True 

    def TrackClick(self, x, y, Button, Pressed):
        """ Detects if the mouse has been clicked

        Arguments:
        - x (int): Cursor x position
        - y (int): Cursor y position
        - Button (pynput.mouse.Button): Enumerator of the left right and middle button
        - Pressed (bool): True if any of the buttons been pressed

        Returns:
        - None
        """
        if Pressed:
            self.Clicked = True 

    def TrackScroll(self, x, y, dx, dy):
        """ Detects if the mouse was scrolled with

        Arguments:
        - x (int): Cursor x position
        - y (int): Cursor y position
        - dx (int): Amount thats been horizontally scrolled
        - dy (int): Amount thats been vertically scrolled

        Returns:
        - None
        """
        self.Scrolled = True

    def LiveMove(self):
        """ Report if mouse moved
        
        Returns:
        - (bool): True if moved else false
        """
        if self.Moved:
            self.Moved = False 
            return True 
        return False 
    
    def LiveClick(self):
        """ Report if mouse has been clicked

        Returns:
        - (bool): True if clicked else false
        """
        if self.Clicked:
            self.Clicked = False 
            return True 
        return False
    
    def LiveScroll(self):
        """ Report if scrolling has happened

        Returns:
        - (bool): True if scrolled else false
        """
        if self.Scrolled:
            self.Scrolled = False 
            return True 
        return False
    
    def Release(self):
        """ Kills code

        Returns:
        - None
        """
        self.Listener.stop()