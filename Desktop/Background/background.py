from Desktop.Background.Metrics.metrics import LogMetrics
import cv2
import numpy as np
import time
from skimage.metrics import structural_similarity as ssim
from collections import deque   

class BackgroundMonitor:
    def __init__(self):
        """ Hybrid (Optical Flow and KNN) computer vision component to determine background changes

        Attributes:
        - Cap (cv2.VideoCapture): Laptop's camera
        - PrevGrayFrame (np.ndarray): Grayscale frame for Optical Flow
        - ReferenceFrame (np.ndarray): Frame for SSIM comparison 
        - LastSSIMCheck (float): Timestamp for last SSIM check
        - LastSSIMScore (float): Latest SSIM score
        - SSIMInterval (float): Delay between SSIM scores
        - MaxFrames (int): Max frames to capture till stop
        - FrameNumber (int): Current frame count

        Raises:
        - RuntimError: Camera not accessible

        Returns:
        - None
        """
        #self.Cap = cv2.VideoCapture(0)
        #if not self.Cap.isOpened():
        #    raise RuntimeError("Error: Camera not found.")

        self.PrevGrayFrame = None
        self.ReferenceFrame = None
        self.LastSSIMCheck = time.time()
        self.LastSSIMScore = 1.0
        self.SSIMInterval = 5
        self.MaxFrames = 100000
        self.FrameNumber = 0

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
    
    def GetStatus(self, MotionRatio, MeanBrightness):
        """ Determine if background changed, camera blocked, or people are moving

        Arguments:
        - MotionRatio (float): Optical Flow meaurement of motion
        - MeanBrightness (float): Average brightness over time
        
        Returns:
        - str: Status of background
        """
        Status = "NORMAL - SAFE"

        if MeanBrightness < 50:
            return "BLOCKED - NOT SAFE"

        if 0.1 <= MotionRatio <= 0.6 and 0.5 < self.LastSSIMScore:
            Status = "MOVEMENT - SAFE"
        elif MotionRatio > 0.7 or self.LastSSIMScore <= 0.5:
            Status = "CHANGED - NOT SAFE"

        return Status

    def ProcessFrame(self, Frame):
        """ Extracts Brightness, SSIM, and Motion values from current frame
        
        Arguments:
        - Frame (np.ndarray): Current frame

        Returns:
        - Tuple:
            - Status (str): Background status
            - MotionRatio (float): Metric of movement
            - SSIMScore (float): SSIM score from frame
            - MeanBrightness (float): Frame average brightness
        """
        Gray = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)

        if self.PrevGrayFrame is None:
            self.PrevGrayFrame = Gray
            if self.ReferenceFrame is None:
                self.ReferenceFrame = Gray.copy()
                self.LastSSIMScore = 1.0
            return "Initialising", 0.0, self.LastSSIMScore, float(np.mean(Gray))

        Flow = cv2.calcOpticalFlowFarneback(
            self.PrevGrayFrame, Gray, None,
            0.5, 3, 15, 3, 5, 1.2, 0
        )
        self.PrevGrayFrame = Gray

        Mag, Ang = cv2.cartToPolar(Flow[..., 0], Flow[..., 1])
        MotionRatio = float(np.mean(Mag > 1.0))

        MeanBrightness = float(np.mean(Gray))

        CurrentTime = time.time()
        if self.ReferenceFrame is None:
            self.ReferenceFrame = Gray.copy()
            self.LastSSIMScore = 1.0

        if CurrentTime - self.LastSSIMCheck > self.SSIMInterval:
            self.LastSSIMCheck = CurrentTime
            try:
                SSIMScore, _ = ssim(self.ReferenceFrame, Gray, full=True)
            except Exception:
                SSIMScore = self.LastSSIMScore
            self.LastSSIMScore = float(SSIMScore)

            if MotionRatio < 0.03 and self.LastSSIMScore > 0.98:
                self.StableCount = getattr(self, "StableCount", 0) + 1
            else:
                self.StableCount = 0

            if getattr(self, "StableCount", 0) >= 3:
                self.ReferenceFrame = Gray.copy()
                self.StableCount = 0

        Status = self.GetStatus(MotionRatio, MeanBrightness)

        return Status, MotionRatio, self.LastSSIMScore, MeanBrightness

    def GetDisplay(self, Frame, Status, FrameNumber, MotionRatio, SSIMScore, Brightness):
        """ Shows current frame
        
        Arguments:
        - Frame (np.ndarray): Current frame
        - Status (str): What's detected
        - FrameNumber (int): Current frame number

        Returns:
        - bool: True if background has altered
        """
        #MaskColoured = cv2.applyColorMap(FGMask, cv2.COLORMAP_JET)
        #Display = cv2.addWeighted(Frame, 0.7, MaskColoured, 0.3, 0)
        #OverlayText = f"{Status} | Frame {self.FrameCount}/10000"
        #OverlayText = f"Background Change Detection: {Status}\nMotion Ratio: {MotionRatio}\nSSIM Score: {SSIMScore}\nBrightness: {Brightness}"

        #Lines = [
        #    f"Background Change Detection: {Status}",
        #    f"Motion Ratio: {MotionRatio:.3f}",
        #    f"SSIM Score: {SSIMScore:.3f}",
        #    f"Brightness: {Brightness:.1f}",
        #]

        if "NOT SAFE" in Status:
            Colour = (0, 0, 255)
        else:
            Colour = (0, 255, 0)

        #cv2.putText(Frame, OverlayText, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, Colour, 2)

        #y = 25
        #for Line in Lines:
        #    cv2.putText(Frame, Line, (10, y),
        #                cv2.FONT_HERSHEY_SIMPLEX, 0.6, Colour, 2)
        #    y += 22 
        #cv2.imshow("Hybrid Background Monitor", Frame)

        if Colour == (0, 255, 0):
            return False 
        return True

    def Live(self, Frame):
        """ Live implementation for background changes

        Arguments:
        - Frame (np.ndarray): Current frame

        Returns:
        - Result (bool): True if background changed else false
        """
        self.FrameNumber += 1
        Status, MotionRatio, SSIMScore, Brightness = self.ProcessFrame(Frame)
        Result = self.GetDisplay(Frame, Status, self.FrameNumber, MotionRatio, SSIMScore, Brightness)
        return Result

    def Run(self):
        """ Capture, process, display, and log metrics from the current frame

        Returns:
        - Status (str): Result of background analysis
        """
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        FirstFrame = self.GetFrame()
        Height, Width, _ = FirstFrame.shape
        FourCC = cv2.VideoWriter_fourcc(*"avc1")  # H.264 if available

        Writer = cv2.VideoWriter("Output.mp4", FourCC, 1, (Width, Height))


        FrameNumber = 0

        while FrameNumber <= self.MaxFrames:
            Frame = self.GetFrame()

            gray = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.05,      # smaller = more sensitive
                minNeighbors=3,        # lower = more detections
                minSize=(50, 50)       # detect slightly smaller faces
            )


            for (x, y, w, h) in faces:
                roi = Frame[y:y+h, x:x+w]
                Frame[y:y+h, x:x+w] = cv2.GaussianBlur(roi, (31, 31), 0)


            Status, MotionRatio, SSIMScore, Brightness  = self.ProcessFrame(Frame)

            FrameNumber += 1

            #print(
            #    f"[{self.FrameCount:03d}/200]  "
            #    f"Motion: {MotionRatio:.3f} | SSIM: {SSIMScore:.3f} | "
            #    f"Brightness: {Brightness:.1f} | "
            #    f"Status: {Status}"
            #)
            LogMetrics(MotionRatio, SSIMScore, Brightness)

            Result = self.GetDisplay(Frame, Status, FrameNumber, MotionRatio, SSIMScore, Brightness)

            Writer.write(Frame)

            if cv2.waitKey(1) & 0xFF == 27:
                self.Release()
                exit(0)

            time.sleep(0.5)

        Writer.release()
        self.Release()

        return Status

    def Release(self):
        """ Kills camera feed

        Returns:
        - None
        """
        #self.Cap.release()
        cv2.destroyAllWindows()