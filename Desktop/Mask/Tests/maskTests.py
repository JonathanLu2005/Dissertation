import cv2
import os
from Desktop.Mask.mask import MaskMonitor

class MaskMonitorTests:
    def __init__(self):
        """ Instantiate the monitor, file paths, and cut camera, to test the mask detection component

        Attributes:
        - Monitor (MaskMonitor): Component to detect if masks are present
        - Monitor.Cap (cv2.VideoCapture): Camera cut as not live
        - TestDirectory (str): File path of directory
        - MaskImage (str): File path of mask image
        - NoMaskImage (str): File path of no mask image

        Returns:
        - None
        """
        self.Monitor = MaskMonitor(MaxRows=1, CameraIndex=0)
        self.Monitor.Cap.release() 
        self.Monitor.Cap = None
        self.TestDirectory = os.path.dirname(__file__)
        self.MaskImage = os.path.join(self.TestDirectory, "Mask.jpg")
        self.NoMaskImage = os.path.join(self.TestDirectory, "NoMask.jpg")

    def TestImage(self, ImagePath):
        """ Run the system with the provided testing image to test performance

        Arguments:
        - ImagePath (str): Image provided to test

        Returns:
        - Tuple:
            - Masked (bool): True if mask is present
            - Confidence (float): Confidence in the outcome
        """
        Frame = cv2.imread(ImagePath)
        Detections = self.Monitor.RunInference(Frame)
        Masked, Confidence = self.Monitor.ProcessFrame(Detections)
        return Masked, Confidence

    def TestMask(self):
        """ Test if mask is detected
        
        Returns:
        - bool: True if mask is detected
        """
        Masked, Confidence = self.TestImage(self.MaskImage)
        return Masked is True

    def TestNoMask(self):
        """ Test if no mask is detected

        Returns:
        - bool: True if no mask is detected
        """
        Masked, Confidence = self.TestImage(self.NoMaskImage)
        return Masked is False

    def RunAllTests(self):
        """ Run all tests for mask detection

        Returns:
        - None
        """
        Results = {
            "Mask": self.TestMask(),
            "No Mask": self.TestNoMask()
        }

        Passed = sum(1 for r in Results.values() if r)
        Total = len(Results)

        print("\nTest Summary:")
        for Name, Result in Results.items():
            print(f" - {Name}: {'PASS' if Result else 'FAIL'}")

        print(f"\nFinal Result: {Passed}/{Total} tests passed.")

if __name__ == "__main__":
    Tests = MaskMonitorTests()
    Tests.RunAllTests()
