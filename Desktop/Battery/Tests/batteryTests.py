from types import SimpleNamespace
import psutil
from Desktop.Battery.battery import BatteryMonitor

class BatteryMonitorTests:
    def __init__(self):
        """ Establish a battery monitor with threshold 20

        Attributes:
        - Monitor (BatteryMonitor): Monitor battery

        Returns:
        - None
        """
        self.Monitor = BatteryMonitor(20)

    def Simulate(self, BatteryPercentage):
        """ Simulates receiving a proxy battery percentage

        Arguments:
        - BatteryPercentage (int): Mock battery percentage

        Returns:
        - (bool): True if battery is below threshold else false
        """
        psutil.sensors_battery = lambda: SimpleNamespace(percent=BatteryPercentage)
        return self.Monitor.Live()
    
    def TestLowBattery(self):
        """ Tests if battery is too low

        Returns:
        - (bool): True if battery is below threshold
        """
        return self.Simulate(10) is True 
    
    def TestHighBattery(self):
        """ Tests if battery is not too low
        
        Returns:
        - (bool): True if battery is above threshold
        """
        return self.Simulate(90) is False 
    
    def RunAllTests(self):
        """ Run all tests for battery monitoring

        Returns:
        - None
        """
        Results = {
            "Low Battery": self.TestLowBattery(),
            "High Battery": self.TestHighBattery()
        }

        Passed = sum(1 for r in Results.values() if r)
        Total = len(Results)

        print("\nTest Summary:")
        for Name, Result in Results.items():
            print(f" - {Name}: {'PASS' if Result else 'FAIL'}")

        print(f"\nFinal Result: {Passed}/{Total} tests passed.")

if __name__ == "__main__":
    Tests = BatteryMonitorTests()
    Tests.RunAllTests()