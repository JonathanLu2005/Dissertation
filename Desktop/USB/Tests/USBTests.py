from types import SimpleNamespace
from Desktop.USB.USB import USBMonitor

class USBMonitorTests:
    def __init__(self):
        """ Tests if detects USB changes

        Attributes:
        - Monitor (USBMonitor): Monitor to check USBs
        - Laptop (SimpleNamespace): Mock laptop devices
        - FullDevices (set[str]): Full set of devices
        - MissingDevices (set[str]): Missing set of devices

        Returns:
        - None
        """
        self.Monitor = USBMonitor()
        self.Monitor.Laptop = SimpleNamespace()
        self.FullDevices = {"USB1", "USB2"}
        self.MissingDevices = {"USB1"}

    def Simulate(self, DevicesBefore, DevicesAfter):
        """ Tests if devices have changed

        Arguments:
        - DevicesBefore (set[str]): Devices currently set on laptop
        - DevicesAfter (set[str]): New devices set on laptop

        Returns:
        - (bool): True if USBs have changed else false
        """
        self.Monitor.TotalDevices = DevicesBefore 
        self.Monitor.Laptop.Win32_USBControllerDevice = lambda: [SimpleNamespace(Dependent=Device) for Device in DevicesAfter]
        return self.Monitor.Live()
    
    def TestNothingHappened(self):
        """ Tests if no USBs are changed
        
        Returns:
        - (bool): True if no USBs are changed
        """
        return self.Simulate(self.FullDevices, self.FullDevices) is False
    
    def TestUSBAdded(self):
        """ Tests when USB is added

        Returns:
        - (bool): True if USBs have changed
        """
        return self.Simulate(self.MissingDevices, self.FullDevices) is True
    
    def TestUSBRemoved(self):
        """ Tests when USB is removed

        Returns:
        - (bool): True if USBs have changed
        """
        return self.Simulate(self.FullDevices, self.MissingDevices) is True
    
    def RunAllTests(self):
        """ Run tests for USB monitor

        Returns:
        - None
        """
        Results = {
            "No USB changes": self.TestNothingHappened(),
            "USB Added": self.TestUSBAdded(),
            "USB Removed": self.TestUSBRemoved()
        }

        Passed = sum(1 for r in Results.values() if r)
        Total = len(Results)

        print("\nTest Summary:")
        for Name, Result in Results.items():
            print(f" - {Name}: {'PASS' if Result else 'FAIL'}")

        print(f"\nFinal Result: {Passed}/{Total} tests passed.")

if __name__ == "__main__":
    Tests = USBMonitorTests()
    Tests.RunAllTests()