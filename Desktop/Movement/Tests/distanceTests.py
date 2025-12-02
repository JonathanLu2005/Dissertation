import numpy as np
from types import SimpleNamespace
from Desktop.Movement.distance import DistanceMonitor

class BoundingBoxSimulation:
    def __init__(self, Coordinates):
        """ Simulated bounding box

        Arguments:
        - Coordinates (list[float]): Bounding box coordinates

        Attributes:
        - Coordinates (list[float]): Bounding box coordinates

        Returns:
        - None
        """
        self.Coordinates = np.array(Coordinates, dtype=np.float32)

    def cpu(self):
        """ Simulates bounding box tensor interface
            
        Returns:
        - BoundingBoxSimulation: Stored bounding box coordinates
        """   
        return self

    def numpy(self):
        """ Returns simulated bounding box coordinates as NumPy array
        
        Returns:
        - Coordinates (np.ndarray): Bounding box coordinates
        """
        return self.Coordinates

class BoundingBoxValues:
    def __init__(self, Height=None):
        """ Detect and creates bounding box

        Arguments:
        - Height (float): Persons bounding box height

        Returns:
        - None
        """
        if Height is None:
            Boxes = SimpleNamespace(xyxy=[], cls=[])
        else:
            x1, y1 = 100, 100
            x2 = 300
            y2 = 100 + Height
            SimulatedBox = BoundingBoxSimulation([x1, y1, x2, y2])
            Boxes = SimpleNamespace(xyxy=[SimulatedBox], cls=[0])

        self.boxes = Boxes

class SimulatedPose:
    def __init__(self, WidthPixel):
        """ Simulated posture landmarks

        Arguments:
        - WidthPixel (float): Distance between shoulders

        Returns:
        - None
        """
        LeftX = 0.5 - (WidthPixel / 2) / 640
        RightX = 0.5 + (WidthPixel / 2) / 640

        self.landmark = [None] * 33
        self.landmark[11] = SimpleNamespace(x=LeftX, y=0.5)
        self.landmark[12] = SimpleNamespace(x=RightX, y=0.5)

class DistanceMonitorTests:
    def __init__(self, BoxThreshold=478.5, PoseThreshold=0.5):
        """ Instantiates distance monitor
        
        Arguments:
        - BoxThreshold (float): Threshold to determine if bounding box is too close
        - PoseThreshold (float): Threshold to determine if pose is too close

        Attributes:
        - self.Monitor (DistanceMonitor): Instantiated version of distance monitor for testing

        Returns:
        - None
        """
        self.Monitor = DistanceMonitor(YoloModel=None, BoxThreshold=BoxThreshold, PoseThreshold=PoseThreshold, MaxRows=1, CameraIndex=0)

        try:
            self.Monitor.Cap.release()
        except Exception:
            pass

        self.Monitor.Cap = None

    def Simulate(self, BoxHeight=None, ShoulderWidth=None):
        """ Generates frame to be tested
        
        Arguments:
        - BoxHeight (float): Simulated persons bounding box height
        - ShoulderWidth (float): Simulated persons shoulder width distance

        Returns:
        - dict: Output of distance monitor processing the frame
        """
        Frame = np.zeros((480, 640, 3), dtype=np.uint8)
        self.Monitor.Yolo = lambda img, verbose=False: [BoundingBoxValues(BoxHeight)]

        if ShoulderWidth is None:
            SimulatedPoseResult = SimpleNamespace(pose_landmarks=None)  
        else:
            SimulatedPoseResult = SimpleNamespace(pose_landmarks=SimpleNamespace(landmark=SimulatedPose(ShoulderWidth).landmark))

        self.Monitor.Pose.process = lambda frame: SimulatedPoseResult
        return self.Monitor.ProcessFrame(Frame)

    def TestStandingClose(self):
        """ Tests if the person is standing too close

        Returns:
        - bool: True if person is standing too close
        """
        Result = self.Simulate(BoxHeight=520, ShoulderWidth=250)
        return Result["FinalStatus"] == "TOO CLOSE"

    def TestStandingFar(self):
        """ Tests if the person is standing far away
        
        Returns:
        - bool: True if person is standing safely away
        """
        Result = self.Simulate(BoxHeight=300, ShoulderWidth=100)
        return Result["FinalStatus"] == "Safe"

    def TestSittingClose(self):
        """ Tests if the person is sitting too close
        
        Returns: 
        - bool: True if person is sitting close
        """
        Result = self.Simulate(BoxHeight=480, ShoulderWidth=350)
        return Result["FinalStatus"] == "TOO CLOSE"

    def TestSittingFar(self):
        """ Tests if the person is sitting far
        
        Returns:
        - bool: True if person is sitting safely away
        """
        Result = self.Simulate(BoxHeight=240, ShoulderWidth=120)
        return Result["FinalStatus"] == "Safe"

    def TestCrouchingClose(self):
        """ Tests if the person is crouching too close
        
        Returns:
        - bool: True if person is crouching close
        """
        Result = self.Simulate(BoxHeight=480, ShoulderWidth=400)
        return Result["FinalStatus"] == "TOO CLOSE"

    def TestCrouchingFar(self):
        """ Tests if the person is crouching far away
        
        Returns:
        - bool: True if person is crouching safely away
        """
        Result = self.Simulate(BoxHeight=180, ShoulderWidth=140)
        return Result["FinalStatus"] == "Safe"

    def TestNoPerson(self):
        """ Tests if no person is detected

        Returns:
        - bool: True if no ones there
        """
        Result = self.Simulate(BoxHeight=None, ShoulderWidth=None)
        return (Result["FinalStatus"] == "Safe") and (Result["BoxStatus"] == "No Person")

    def RunAllTests(self):
        """ Runs all unit tests and return results

        Returns:
        - None
        """
        Results = {
            "Standing Close": self.TestStandingClose(),
            "Standing Far": self.TestStandingFar(),
            "Sitting Close": self.TestSittingClose(),
            "Sitting Far": self.TestSittingFar(),
            "Crouching Close": self.TestCrouchingClose(),
            "Crouching Far": self.TestCrouchingFar(),
            "No Person": self.TestNoPerson()
        }

        Passed = sum(1 for r in Results.values() if r)
        Total = len(Results)

        print("\nTest Summary:")
        for Name, Result in Results.items():
            print(f" - {Name}: {'PASS' if Result else 'FAIL'}")

        print(f"\nFinal Result: {Passed}/{Total} tests passed.")

if __name__ == "__main__": 
    Tests = DistanceMonitorTests()
    Tests.RunAllTests()
