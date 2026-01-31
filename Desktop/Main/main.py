from Desktop.Background import background
from Desktop.Movement import distance, gesture
from Desktop.Lingering import lingering
from Desktop.Mask import mask
from Desktop.Keyboard import keyboardMonitor
from Desktop.USB import USB
from Desktop.Battery import battery
import time
import ctypes
import cv2 

class CameraManager:
    def __init__(self):
        """ Retrieve frames from camera to analyse

        Attributes:
        - Cap (cv2.VideoCapture): Camera
        - Frame (np.ndarray): Current frame

        Raises:
        - RuntimeError: Camera not accessible

        Returns:
        - None
        """
        self.Cap = cv2.VideoCapture(0)
        if not self.Cap.isOpened():
            raise RuntimeError("Can't access camera")
        self.Frame = None 
    
    def GetFrame(self):
        """ Return current frame

        Returns:
        - Frame (np.ndarray): Current frame
        """
        Ret, Frame = self.Cap.read()
        if not Ret:
            return None 
        self.Frame = cv2.resize(Frame, (900, 700))
        return self.Frame
    
    def Release(self):
        """ Turns off camera

        Returns:
        - None
        """
        self.Cap.release()


def Main():
    """ Calls computer vision components
    
    Returns:
    - None
    """

    Camera = CameraManager()
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
    Monitor1 = lingering.LingeringMonitor()
    Monitor2 = distance.DistanceMonitor()
    Monitor3 = mask.MaskMonitor()
    Monitor4 = background.BackgroundMonitor()
    Monitor5 = USB.USBMonitor()
    Monitor6 = battery.BatteryMonitor(10)
    Monitor7 = keyboardMonitor.KeyboardMonitor()

    try:
        # Live
        while True:
            Frame = Camera.GetFrame()
            Result1 = Monitor1.Live(Frame)
            Result2 = Monitor2.Live(Frame)
            Result3 = Monitor3.Live(Frame)
            Result4 = Monitor4.Live(Frame)
            Result5 = Monitor5.Live()
            Result6 = Monitor6.Live()
            Result7 = Monitor7.Live()
            Result = any([Result1, Result2, Result3, Result4, Result5, Result6, Result7])
            print(Result)
            time.sleep(1)
            yield Result

        # Test
        #while True:
        #    Result = Monitor.Run()
        #    time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping monitoring...")
    finally:
        Monitor1.Release()
        Monitor2.Release()
        Monitor3.Release()
        Monitor4.Release()
        Monitor5.Release()
        Monitor6.Release()
        Monitor7.Release()

if __name__ == "__main__":
    for _ in Main():
        pass