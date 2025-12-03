import numpy as np
from types import SimpleNamespace
from Desktop.Movement.gesture import GestureMonitor

class SimulatedHand:
    def CreateHand(WidthPixels):
        """ Create landmarks to Simulate hand is shown

        Arguments:
        - WidthPixels (float): Width between hands

        Returns:
        - SimpleNamespace: Simulates MediaPipe's hand structure
        """
        LeftHand = 0.5 - (WidthPixels / 2) / 640
        RightHand = 0.5 + (WidthPixels / 2) / 640

        Landmarks = []
        for i in range(21):
            if i % 2 == 0:
                x = LeftHand 
            else:
                x = RightHand
            Landmarks.append(SimpleNamespace(x=x, y=0.5))

        return SimpleNamespace(landmark=Landmarks)

    def Outcome(WidthPixels):
        """ Returns MediaPipe classification from detecting the hand
        
        Arguments:
        - WidthPixels (float): Width between hands

        Returns:
        - SimpleNamespace: MediaPipe classification after detecting hand
        """
        if WidthPixels is None:
            return SimpleNamespace(multi_handedness=None, multi_hand_landmarks=None)
        return SimpleNamespace(multi_handedness=[SimpleNamespace(classification=[SimpleNamespace(score=1.0)])], multi_hand_landmarks=[SimulatedHand.CreateHand(WidthPixels)])

class GestureMonitorTests:
    def __init__(self, Threshold=120):
        """ Initiates gesture monitor to run
        
        Arguments:
        - Threshold (int): Threshold until someones deemed too close to device

        Attributes:
        - self.Monitor (GestureMonitor): Code to determine if users too close via kinematics
        - self.Monitor.Cap (cv2.VideoCapture): Laptop's camera closed

        Returns:
        - None
        """
        self.Monitor = GestureMonitor(Threshold=Threshold, CameraIndex=0, MaxRows=1)

        try:
            self.Monitor.Cap.release()
        except Exception:
            pass
        self.Monitor.Cap = None

    def Simulate(self, WidthPixels, Frames=6):
        """ Generate frame and provide to Gesture Monitor

        Arguments:
        - WidthPixels (float): Width between hands
        - Frames (int): Number of frames created

        Returns:
        - Tuple:
            - HandDetectedFlag (int): Determine if hand was detected
            - HandPresenceScore (float): Confidence that it was a hand
            - SmoothedPixel (float): Smoothed estimate of hands pixel width
            - Status (str): Result of scenario
            - Colour (tuple): RGB for text
        """
        Frame = np.zeros((480, 640, 3), dtype=np.uint8)
        MPResults = SimulatedHand.Outcome(WidthPixels)

        self.Monitor.Hands.process = lambda Frame: MPResults

        Outcome = None
        for x in range(Frames):      
            Outcome = self.Monitor.ProcessFrame(Frame)

        return Outcome

    def TestHandsClose(self):
        """ Test Gesture Monitor if we have our hands close to the camera
        
        Returns:
        - bool: True if users too close
        """
        HandDetectedFlag, HandPresenceScore, SmoothedPixel, Status, Colour = self.Simulate(WidthPixels=200, Frames=6)
        return Status == "TOO_CLOSE"

    def TestHandsFar(self):
        """ Tests Gesture Monitor if hands are far away from camera

        Returns:
        - bool: True if users far away safely
        """
        HandDetectedFlag, HandPresenceScore, SmoothedPixel, Status, Colour = self.Simulate(WidthPixels=40, Frames=6)
        return Status == "SAFE"

    def TestNoHands(self):
        """ Tests Gesture Monitor if no hands are present

        Returns:
        - bool: True if no hands are present
        """
        HandDetectedFlag, HandPresenceScore, SmoothedPixel, Status, Colour = self.Simulate(WidthPixels=None, Frames=1)
        return Status == "SAFE"

    def RunAll(self):
        """ Run all tests and presents them

        Returns:
        - None
        """
        print("\nGesture Results:")

        Results = {
            "Hands Close": self.TestHandsClose(),
            "Hands Far": self.TestHandsFar(),
            "No Hands": self.TestNoHands(),
        }

        Passed = sum(1 for r in Results.values() if r)
        for Name, Result in Results.items():
            print(f" - {Name}: {'PASS' if Result else 'FAIL'}")
        print(f"\nFinal Result: {Passed}/{len(Results)} Results Passed.")

if __name__ == "__main__":
    Tests = GestureMonitorTests()
    Tests.RunAll()