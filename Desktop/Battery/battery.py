import psutil
import time

class BatteryMonitor:
    def __init__(self, Threshold):
        """ Tracks the battery

        Arguments:
        - Threshold (int): Battery level chosen to determine when too low is low

        Attributes:
        - Threshold (int): Track threshold

        Returns:
        - None
        """
        self.Threshold = Threshold

    def Live(self):
        """ Returns true if battery is below threshold

        Returns:
        - (bool): True if battery is below threshold
        """
        Battery = psutil.sensors_battery()

        if Battery.percent <= self.Threshold:
            return True 
        return False

    def Release(self):
        """ Kills code

        Returns:
        - None
        """
        return