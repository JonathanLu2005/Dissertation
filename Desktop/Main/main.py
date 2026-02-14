from Desktop.Background import background
from Desktop.Movement import distance, gesture
from Desktop.Lingering import lingering
from Desktop.Mask import mask
from Desktop.Keyboard import keyboardMonitor
from Desktop.USB import USB
from Desktop.Battery import battery
import time
import ctypes

def Main(BackgroundModel, ProximityModel, LoiteringModel, MaskModel, Frame, Monitors):
    """ Calls computer vision components

    Argments:
    - BackgroundModel (bool): True if activated
    - ProximityModel (bool): True if activated
    - LoiteringModel (bool): True if activated
    - MaskModel (bool): True if activated
    - Frame (np.ndarray): Current frame
    - Monitors (tuple): List of all the monitors
    
    Returns:
    - None
    """
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
    Monitor1, Monitor2, Monitor3, Monitor4, Monitor5, Monitor6, Monitor7, Monitor8 = Monitors

    try:
        # Live
        Message = ""

        if LoiteringModel:
            Result1 = Monitor1.Live(Frame)
            if Result1:
                Message += "Someone is loitering\n"
        if ProximityModel:
            Result2 = Monitor2.Live(Frame)
            if Result2:
                Message += "Someone is within proximity\n"
        if MaskModel:
            Result3 = Monitor3.Live(Frame)
            if Result3:
                Message += "Someone is wearing a mask\n"
        if BackgroundModel:
            Result4 = Monitor4.Live(Frame)
            if Result4:
                Message += "Background has changed\n"
        Result5 = Monitor5.Live()
        if Result5:
            Message += "USB has been modified\n"
        Result6 = Monitor6.Live()
        if Result6:
            Message += "Battery is low\n"
        Result7 = Monitor7.Live()
        if Result7:
            Message += "Keyboard was used\n"
        Result8 = Monitor8.LiveMove()
        Result9 = Monitor8.LiveClick()
        Result10 = Monitor8.LiveScroll()
        if Result8:
            Message += "Mouse was moved\n"
        if Result9:
            Message += "Mouse was clicked\n"
        if Result10:
            Message += "Mouse was scrolled\n"
            
        if Message != "":
            #print(True)
            #print(Message)
            return (True,Message)
        else:
            #print(False)
            #print("No suspicious activity is detected")
            return (False,"No suspicious activity is detected")
        time.sleep(1)

        # Test
        #while True:
        #    Result = Monitor.Run()
        #    time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping monitoring...")

if __name__ == "__main__":
    for _ in Main():
        pass