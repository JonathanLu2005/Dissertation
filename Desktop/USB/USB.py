import wmi 
import time 

class USBMonitor():
    def __init__(self):
        """ Check if USBs have been manipulated

        Attributes:
        - Laptop (wmi.WMI): Access to device windows system
        - TotalDevices (set[str]): Set of devices that are currently connected

        Returns:
        - None
        """
        self.Laptop = wmi.WMI()
        self.TotalDevices = set(Device.Dependent for Device in self.Laptop.Win32_USBControllerDevice())

    def Live(self):
        """ Keeps checking if devices are tampered by comparing against how many are stored

        Returns:
        - None
        """
        while True:
            try:
                CurrentDevices = set(Device.Dependent for Device in self.Laptop.Win32_USBControllerDevice())
                AddedDevices = CurrentDevices - self.TotalDevices 
                RemovedDevices = self.TotalDevices - CurrentDevices 

                if AddedDevices or RemovedDevices:
                    yield True 
                    self.TotalDevices = CurrentDevices
                else: 
                    yield False 
                time.sleep(1)
            except: 
                continue

    def Release(self):
        """ Kills code

        Returns:
        - None
        """
        self.TotalDevices = {}