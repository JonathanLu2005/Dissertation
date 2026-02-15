from Desktop.Background import background
from Desktop.Movement import distance
from Desktop.Lingering import lingering
from Desktop.Mask import mask
from Desktop.Keyboard import keyboardMonitor
from Desktop.USB import USB
from Desktop.Battery import battery
from Desktop.Trackpad import trackpad
from Desktop.Performance import performance

def GenerateMonitors():
    """ Generate monitor objects to use

    Returns:
    - (tuple):
        - LoiteringMonitor (LingeringMonitor): Monitors loitering
        - ProximityMonitor (DistanceMonitor): Monitors proximity
        - MaskMonitor (MaskMonitor): Monitors mask
        - BackgroundMonitor (BackgroundMonitor): Monitors background
        - USBMonitor (USBMonitor): Monitors USBs
        - BatteryMonitor (BatteryMonitor): Monitors battery
        - KeyboardMonitor (KeyboardMonitor): Monitors keyboard
        - TrackpadMonitor (TrackpadMonitor): Monitors trackpad
    """
    LoiteringMonitor = lingering.LingeringMonitor()
    ProximityMonitor = distance.DistanceMonitor()
    MaskMonitor = mask.MaskMonitor()
    BackgroundMonitor = background.BackgroundMonitor()
    USBMonitor = USB.USBMonitor()
    BatteryMonitor = battery.BatteryMonitor(10)
    KeyboardMonitor = keyboardMonitor.KeyboardMonitor()
    TrackpadMonitor = trackpad.TrackpadMonitor()
    PerformanceMonitor = performance.PerformanceMonitor()
    return (LoiteringMonitor, ProximityMonitor, MaskMonitor, BackgroundMonitor, USBMonitor, BatteryMonitor, KeyboardMonitor, TrackpadMonitor)