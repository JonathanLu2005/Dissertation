import time
from types import SimpleNamespace
from Desktop.Lingering.lingering import LingeringMonitor

class LingeringMonitorTests:
    def __init__(self, Threshold=60):
        """ Instantiates lingering monitor

        Arguments:
        - Threshold (int): Duration an individual must last to be considered loitering

        Attributes:
        - Monitor (LingeringMonitor): Instantiated version of lingering monitor for testing
        - Monitor.Cap (cv2.VideoCapture): Camera cut as not live

        Returns:
        - None
        """
        self.Monitor = LingeringMonitor(LingeringThreshold=Threshold, MaxRows=1, CameraIndex=0)
        self.Monitor.Cap.release() 
        self.Monitor.Cap = None

    def Simulate(self, Period):
        """ This simulates each test scenario by providing a mock pose if the person is there or not

        Arguments:
        - Period (list[tuple]): Simulates the person in front of the camera by whether or not they're there and how long for

        Returns:
        - Status (str): Final outcome from processing the final frame 
        """
        StartTime = time.time()
        self.Monitor.StartTime = None
        self.Monitor.PersonDetected = False

        for Elapsed, Present in Period:
            time.time = lambda: StartTime + Elapsed

            if Present:
                Result = SimpleNamespace(pose_landmarks=SimpleNamespace(landmark=[SimpleNamespace(x=0.5, y=0.5)] * 33))
            else:
                Result = SimpleNamespace(pose_landmarks=None)

            Status, Colour, DwellTime, Confidence, BoundingBox = self.Monitor.ProcessFrame(Result)

        return Status

    def TestStandingLoitering(self):
        """ Tests if a person is present to camera for 60 seconds, if they're considered loitering
        
        Returns:
        - bool: True if person is loitering
        """
        Period = [(Seconds, True) for Seconds in range(0, 61)]
        return self.Simulate(Period) == "LOITERING - NOT SAFE"

    def TestStandingNotLongEnough(self):
        """ Tests if a person is present to a camera for 30 seconds, if they're considered loitering

        Returns:
        - bool: True if person is not loitering
        """
        Period = [(Seconds, True) for Seconds in range(0, 30)]
        return self.Simulate(Period) == "PRESENT - SAFE"

    def TestMovingInAndOut(self):
        """ Tests if a person who move in and out of the camera under 60 seconds, if they're considered loitering

        Returns:
        - bool: True if person is not loitering
        """
        Period = (
            [(Seconds, True) for Seconds in range(0, 30)] +
            [(31, False)] +
            [(Seconds, True) for Seconds in range(32, 60)]
        )
        return self.Simulate(Period) == "PRESENT - SAFE"

    def TestNoPerson(self):
        """ Tests if no one is present in the camera, if they're considered loitering

        Returns:
        - bool: True if person is not loitering
        """
        Period = [(Seconds, False) for Seconds in range(0, 60)]
        return self.Simulate(Period) == "NO PERSON"

    def TestObjectOnly(self):
        """ Tests if only an object is in the camera, if its considered loitering
        
        Returns:
        - bool: True, its not considered loitering
        """
        Period = [(Seconds, False) for Seconds in range(0, 60)]
        return self.Simulate(Period) == "NO PERSON"

    def RunAllTests(self):
        """ Run all tests for lingering monitor
        
        Returns:
        - None
        """
        Results = {
            "Standing Loitering": self.TestStandingLoitering(),
            "Standing Not Long Enough": self.TestStandingNotLongEnough(),
            "Moving In and Out": self.TestMovingInAndOut(),
            "No Person": self.TestNoPerson(),
            "Object Only": self.TestObjectOnly()
        }

        Passed = sum(1 for r in Results.values() if r)
        Total = len(Results)

        print("\nTest Summary:")
        for Name, Result in Results.items():
            print(f" - {Name}: {'PASS' if Result else 'FAIL'}")

        print(f"\nFinal Result: {Passed}/{Total} tests passed.")

if __name__ == "__main__":
    Tests = LingeringMonitorTests()
    Tests.RunAllTests()
