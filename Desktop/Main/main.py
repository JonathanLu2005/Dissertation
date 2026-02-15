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
    LoiteringMonitor, ProximityMonitor, MaskMonitor, BackgroundMonitor, USBMonitor, BatteryMonitor, KeyboardMonitor, TrackpadMonitor = Monitors

    try:
        Message = ""
        if LoiteringModel and LoiteringMonitor.Live(Frame):
            Message += "Someone is loitering\n"
        if ProximityModel and ProximityMonitor.Live(Frame):
            Message += "Someone is within proximity\n"
        if MaskModel and MaskMonitor.Live(Frame):
            Message += "Someone is wearing a mask\n"
        if BackgroundModel and BackgroundMonitor.Live(Frame):
            Message += "Background has changed\n"
        if USBMonitor.Live():
            Message += "USB has been modified\n"
        if BatteryMonitor.Live():
            Message += "Battery is low\n"
        if KeyboardMonitor.Live():
            Message += "Keyboard was used\n"
        if TrackpadMonitor.LiveMove():
            Message += "Mouse was moved\n"
        if TrackpadMonitor.LiveClick():
            Message += "Mouse was clicked\n"
        if TrackpadMonitor.LiveScroll():
            Message += "Mouse was scrolled\n"
            
        if Message != "":
            return (True,Message)
        else:
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