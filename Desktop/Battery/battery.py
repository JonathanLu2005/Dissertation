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
        """ Yields true if battery is below threshold

        Returns:
        - None
        """
        while True:
            Battery = psutil.sensors_battery()

            print(Battery.percent)

            if Battery.percent <= self.Threshold:
                yield True 
            else: 
                yield False 
            time.sleep(1)
        self.Release()

    def Release(self):
        """ Kills code

        Returns:
        - None
        """
        return