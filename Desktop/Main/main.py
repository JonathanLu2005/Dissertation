from Desktop.Background import background
from Desktop.Movement import distance, gesture
from Desktop.Lingering import lingering
from Desktop.Mask import mask
from Desktop.Keyboard import keyboardMonitor
from Desktop.USB import USB
import time

def Main():
    """ Calls computer vision components
    
    Returns:
    - None
    """
    #Monitor = lingering.LingeringMonitor()
    #Monitor = distance.DistanceMonitor()
    #Monitor = gesture.GestureMonitor()
    #Monitor = background.BackgroundMonitor()
    #Monitor = mask.MaskMonitor()
    #Monitor = keyboardMonitor.KeyboardMonitor()
    Monitor = USB.USBMonitor()
    

    try:
        # Live
        for Result in Monitor.Live():
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
        Monitor.Release()

if __name__ == "__main__":
    for _ in Main():
        pass