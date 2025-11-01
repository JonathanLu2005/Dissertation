import cv2
import numpy as np
import time
from Desktop.Background.background import BackgroundMonitor

class BackgroundMonitorTests:
    def __init__(self):
        """ Sets up camera to send frames to test component

        Attributes:
        - Monitor (BackgroundMonitor): Component ran for tests
        
        Returns:
        - None
        """
        self.Monitor = BackgroundMonitor(CameraIndex=0)
        self.Monitor.Cap.release()  
        self.Monitor.Cap = None

    def ResetMonitor(self, SSIMInterval=0.1, StartingFrames=5):
        """ Resets BackgroundMonitor to test next situation
        
        Arguments:
        - SSIMInterval (float): Interval between SSIM calculations
        - StartingFrames (int): Num frames to stabilise BackgroundMonitor

        Returns:
        - None
        """
        self.Monitor = BackgroundMonitor(CameraIndex=0, SSIMInterval=SSIMInterval)
        try:
            self.Monitor.Cap.release()
        except Exception:
            pass
        self.Monitor.Cap = None

        Frame = self.GenerateSolidFrame(100)
        for i in range(StartingFrames):
            self.Monitor.ProcessFrame(Frame)
            time.sleep(0.05)

    def GenerateSolidFrame(self, ColourValue):
        """ Generate Frame to test component if can detect situation
        
        Arguments:
        - ColourValue (int): Grayscale intensity level for Frame

        Returns:
        - Frame (np.ndarray): BGR image to test component
        """
        Frame = np.full((480, 640, 3), ColourValue, dtype=np.uint8)
        return Frame

    def SimulateFrames(self, Frames):
        """ Send Frame to background component for results
        
        Arguments:
        - Frames (list[np.ndarray]): Images to be analysed

        Returns:
        - Tuple:
            - Status (str): Situation result
            - Motion (float): Measure of motion from situation
            - SSIMScore (float): Final SSIM value
            - Brightness (float): Frame's average brightness
        """
        Status = None
        for Frame in Frames:
            Status, FG, Motion, SSIMScore, Brightness = self.Monitor.ProcessFrame(Frame)
            time.sleep(0.1)
        return Status, Motion, SSIMScore, Brightness

    def TestNormal(self):
        """ Provide frames that hasn't changed and expect status to be Normal
        
        Returns:
        - bool: True if situation is classed as Normal
        """
        self.ResetMonitor()
        Frame = self.GenerateSolidFrame(150)
        Frames = [Frame for i in range(10)]
        Status, Motion, SSIM, Brightness = self.SimulateFrames(Frames)
        return Status == "Normal"

    def TestLightingChange(self):
        """ Provide frames with a change of brightness and expect status related to Lighting / Camera Blocked
        
        Returns:
        - bool: True if situation is classed as Lighting Drop / Camera Blocked
        """
        self.ResetMonitor()
        Frames = [self.GenerateSolidFrame(150)] * 5 + [self.GenerateSolidFrame(30)] * 5
        Status, Motion, SSIM, Brightness = self.SimulateFrames(Frames)
        return Status == "Lighting Drop / Camera Blocked"

    def TestPersonMovement(self):
        """ Generate circles onto frames to simulate motion
        
        Returns:
        - bool: True if situation is classed as Person Movement
        """
        self.ResetMonitor()

        Frames = []
        BackgroundColour = (40, 40, 40)  

        for FrameNumber in range(10):
            Frame = np.full((480, 640, 3), BackgroundColour, dtype=np.uint8)
            np.random.seed(FrameNumber)

            for i in range(8):
                x = int((FrameNumber * 40 + i * 80) % 640)
                y = int((FrameNumber * 25 + i * 50) % 480)
                cv2.circle(Frame, (x, y), 25, (255, 255, 255), -1)

            Frame = cv2.convertScaleAbs(Frame, alpha=1.0, beta=np.random.randint(-5, 5))
            Frames.append(Frame)

        Status, Motion, SSIM, Brightness = self.SimulateFrames(Frames)
        return Status == "Person Movement"

    def TestBackgroundChange(self):
        """ Creates current frame and new ones by adding rectnagle to test background change
        
        Returns:
        - bool: True if situation is classed as Background Change
        """
        self.ResetMonitor()
        Frames = []

        for i in range(5):
            Frame = np.full((480, 640, 3), (60, 60, 60), dtype=np.uint8)
            cv2.putText(Frame, "Old Background", (200, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)
            Frames.append(Frame)

        for i in range(5):
            Frame = np.full((480, 640, 3), (230, 230, 230), dtype=np.uint8)

            for i in range(0, 480, 60):
                Colour = (
                    np.random.randint(0, 255),
                    np.random.randint(0, 255),
                    np.random.randint(0, 255),
                )
                cv2.rectangle(Frame, (0, i), (640, i + 30), Colour, -1)

            cv2.putText(Frame, "New Background", (100, 240), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 6)
            Noise = np.random.randint(0, 60, (480, 640, 3), dtype=np.uint8)
            Frame = cv2.add(Frame, Noise)

            Frames.append(Frame)

        Status, Motion, SSIM, Brightness = self.SimulateFrames(Frames)
        return Status == "Background Changed"

    def RunAllTests(self):
        """ Run tests and provide summary
        
        Returns:
        - None
        """
        Results = {
            "Normal": self.TestNormal(),
            "Lighting Change": self.TestLightingChange(),
            "Person Movement": self.TestPersonMovement(),
            "Background Change": self.TestBackgroundChange()
        }

        Passed = sum(1 for r in Results.values() if r)
        Total = len(Results)
        print("\nTest Summary:")
        for Name, Result in Results.items():
            print(f" - {Name}: {'PASS' if Result else 'FAIL'}")

        print(f"\nFinal Result: {Passed}/{Total} tests Passed.")

if __name__ == "__main__":
    Tests = BackgroundMonitorTests()
    Tests.RunAllTests()
