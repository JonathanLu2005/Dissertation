from Desktop.Background.Metrics.metrics import LogMetrics
import cv2
import numpy as np
import time
from skimage.metrics import structural_similarity as ssim
from collections import deque   

class BackgroundMonitor:
    def __init__(self, CameraIndex=0, SSIMInterval=5, HistoryLen=10, MaxRows=200):
        """ Hybrid (Optical Flow and KNN) computer vision component to determine background changes

        Arguments:
        - CameraIndex (int): Camera index to use
        - SSIMInterval (int): Time gaps between SSIM calculations
        - HistoryLen (int): Max Brightness values to hold to calculate average
        - MaxRows (int): Max frames to log

        Attributes:
        - Cap (cv2.VideoCapture): Laptop's camera
        - PrevGray (np.ndarray): Grayscale frame for Optical Flow
        - BGSubtractor (cv2.createBackgroundSubtractorKNN): KNN background subtraction
        - ReferenceFrame (np.ndarray): Frame for SSIM comparison 
        - LastSSIMCheck (float): Timestamp for last SSIM check
        - LastSSIMScore (float): Latest SSIM score
        - SSIMInterval (float): Delay between SSIM scores
        - BrightnessHistory (collections.deque): Queue of recent average brightness values
        - HistoryLen (int): Max BrightnessHistory length
        - FrameCount (int): Number frames processed
        - MaxRows (int): Max frames to capture till stop
        - StartTime (float): Timestamp when monitoring started

        Raises:
        - RuntimError: Camera not accessible

        Returns:
        - None
        """
        self.Cap = cv2.VideoCapture(CameraIndex)
        if not self.Cap.isOpened():
            raise RuntimeError("Error: Camera not found.")

        self.PrevGray = None
        self.BGSubtractor = cv2.createBackgroundSubtractorKNN(history=200, dist2Threshold=1000.0)

        self.ReferenceFrame = None
        self.LastSSIMCheck = time.time()
        self.LastSSIMScore = 1.0
        self.SSIMInterval = SSIMInterval

        self.BrightnessHistory = deque(maxlen=HistoryLen)
        self.HistoryLen = HistoryLen

        self.FrameCount = 0
        self.MaxRows = MaxRows
        self.StartTime = time.time()

    def GetFrame(self):
        """ Captures current camera frame

        Returns:
        - np.ndarray: Video frame

        Raises:
        - RuntimeError: Camera fails to return frame
        """
        Ret, Frame = self.Cap.read()
        if not Ret:
            raise RuntimeError("Error: Failed to read from camera.")
        return cv2.resize(Frame, (640, 480))
    
    def GetStatus(self, BrightnessDrop, AvgBrightness, MotionRatio):
        """ Determine if background changed, camera blocked, or people are moving

        Arguments:
        - BrightnessDrop (float): Difference in average and current brightness
        - AvgBrightness (float): Average brightness recently
        - MotionRatio (float): Optical Flow meaurement of motion
        
        Returns:
        - str: Status of background
        """
        Status = "Normal"

        if len(self.BrightnessHistory) >= self.HistoryLen / 2:
            if BrightnessDrop > AvgBrightness * 0.3:
                Status = "Lighting Drop / Camera Blocked"

        if Status == "Normal":
            if self.LastSSIMScore < 0.5:
                if MotionRatio < 0.05:
                    Status = "Background Changed"
                else:
                    Status = "Person Movement"
            elif MotionRatio > 0.05:
                Status = "Person Movement"

        return Status

    def ProcessFrame(self, Frame):
        """ Extracts Brightness, SSIM, and Motion values from current frame
        
        Arguments:
        - Frame (np.ndarray): Current frame

        Returns:
        - Tuple:
            - Status (str): Background status
            - FGMask (np.ndarray): Foreground mask
            - MotionRatio (float): Metric of movement
            - SSIMScore (float): SSIM score from frame
            - MeanBrightness (float): Frame average brightness
            - BrightnessDrop (float): Difference in current and average brightness
        """
        Gray = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)

        FGMask = self.BGSubtractor.apply(Gray)
        FGMask = cv2.morphologyEx(FGMask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

        if self.PrevGray is None:
            self.PrevGray = Gray
            return "Initialising", FGMask, 0.0, 1.0, np.mean(Gray), 0.0

        Flow = cv2.calcOpticalFlowFarneback(
            self.PrevGray, Gray, None,
            0.5, 3, 15, 3, 5, 1.2, 0
        )
        self.PrevGray = Gray

        Mag, Ang = cv2.cartToPolar(Flow[..., 0], Flow[..., 1])
        MotionRatio = np.mean(Mag > 1.0)
        AvgFlowMag = np.mean(Mag)

        MeanBrightness = np.mean(Gray)
        self.BrightnessHistory.append(MeanBrightness)
        AvgBrightness = np.mean(self.BrightnessHistory)
        BrightnessDrop = AvgBrightness - MeanBrightness

        CurrentTime = time.time()
        if self.ReferenceFrame is None:
            self.ReferenceFrame = Gray

        if CurrentTime - self.LastSSIMCheck > self.SSIMInterval:
            self.LastSSIMCheck = CurrentTime
            self.LastSSIMScore, _ = ssim(self.ReferenceFrame, Gray, full=True)
            self.ReferenceFrame = Gray

        Status = self.GetStatus(BrightnessDrop, AvgBrightness, MotionRatio)

        return Status, FGMask, MotionRatio, self.LastSSIMScore, MeanBrightness, BrightnessDrop

    def GetDisplay(self, Frame, FGMask, Status):
        """ Shows current frame
        
        Arguments:
        - Frame (np.ndarray): Current frame
        - FGMask (np.ndarray): Foreground mask
        - Status (str): What's detected

        Returns:
        - None
        """
        MaskColoured = cv2.applyColorMap(FGMask, cv2.COLORMAP_JET)
        Display = cv2.addWeighted(Frame, 0.7, MaskColoured, 0.3, 0)
        OverlayText = f"{Status} | Frame {self.FrameCount}/200"
        cv2.putText(Display, OverlayText, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.imshow("Hybrid Background Monitor", Display)

    def Run(self):
        """ Capture, process, display, and log metrics from the current frame

        Returns:
        - Tuple:
            - Status (str): Result of background analysis
            - MotionRatio (float): Movement score from Optical Flow
        """
        if self.FrameCount >= self.MaxRows:
            print("\n✅ Reached 200 logged frames — stopping monitoring.")
            self.Release()
            exit(0)

        Frame = self.GetFrame()
        Status, FGMask, MotionRatio, SSIMScore, Brightness, BrightnessDrop = self.ProcessFrame(Frame)

        self.FrameCount += 1

        print(
            f"[{self.FrameCount:03d}/200]  "
            f"Motion: {MotionRatio:.3f} | SSIM: {SSIMScore:.3f} | "
            f"Brightness: {Brightness:.1f} | ΔBright: {BrightnessDrop:.1f} | "
            f"Status: {Status}"
        )
        LogMetrics(MotionRatio, SSIMScore, Brightness)

        self.GetDisplay(Frame, FGMask, Status)

        if cv2.waitKey(1) & 0xFF == 27:
            self.Release()
            exit(0)

        time.sleep(0.3)
        return Status, MotionRatio

    def Release(self):
        """ Kills camera feed

        Returns:
        - None
        """
        self.Cap.Release()
        cv2.destroyAllWindows()