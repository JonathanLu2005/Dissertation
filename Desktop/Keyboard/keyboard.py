import keyboard 
import time

def KeyboardMonitor():
    """ Detects if a key is pressed and yields True

    Returns:
    - None
    """
    while True:
        Event = keyboard.read_event()
        yield True 
        print("True")
        time.sleep(1)
    return