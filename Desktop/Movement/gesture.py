import cv2
import mediapipe as mp
import numpy as np
import time
from Desktop.Movement.Metrics.metrics import LogGesture

class GestureMonitor:
    def __init__(self, CameraIndex=0, MaxRows=200):
        """ Initalise Hand proximity model
        
        Arguments:
        - CameraIndex (int): Location for webcam
        - MaxRows (int): Number frames recorded for metrics

        Attributes:
        - Cap (cv2.VideoCapture): Laptops camera
        - Threshold (int): Distance till someones determined to be too close
        - MPHands (module): MediaPipe hands solution module
        - Hands (mp.solutions.hands.Hands): MediaPipe hands detector 
        - MaxRows (int): Number frames recorded
        - ProximitySmooth (int): Stabilise noisy frames

        Raises:
        - RuntimeError: Camera not accessible

        Returns:
        - None
        """
        self.Cap = cv2.VideoCapture(CameraIndex)
        if not self.Cap.isOpened():
            raise RuntimeError("Camera not accessible.")

        self.Threshold = 120
        self.MPHands = mp.solutions.hands
        self.Hands = self.MPHands.Hands(model_complexity=0, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

        self.MaxRows = MaxRows
        self.ProximitySmooth = 0

    def Smooth(self, Value, Alpha=0.2):
        """ Smoothes to remove noisiness 
        
        Arguments:
        - Value (float): Distance value
        - Alpha (float): Smoothing factor

        Returns:
        - ProximitySmooth (float): Updated smoothed value
        """
        self.ProximitySmooth = (Alpha * Value) + (1 - Alpha) * self.ProximitySmooth
        return self.ProximitySmooth

    def GetFrame(self):
        """ Captures current camera frame

        Returns:
        - np.ndarray: Video frame

        Raises:
        - RuntimeError: Camera fails to return frame
        """
        Ret, Frame = self.Cap.read()
        if not Ret:
            raise RuntimeError("Camera failed.")
        return cv2.resize(Frame, (640, 480))
    
    def ProcessFrame(self, Frame):
        """ Given frame, determine if persons too close via their hand landmarks
        
        Arguments:
        - Frame (np.ndarray): Current frame

        Returns:
        - Tuple:
            - HandDetectedFlag (int): 1 if hands detected
            - HandPresenceScore (float): Confidence hands are detected
            - SmoothedPixel (float): Smoothed estimate of hands pixel width
            - Status (str): String confirming if persons too close or not
            - Colour (tuple): RGB colour for message on screen
        """
        RGB = cv2.cvtColor(Frame, cv2.COLOR_BGR2RGB)
        Result = self.Hands.process(RGB)

        HandDetectedFlag = 0
        HandPresenceScore = 0.0
        HandWidthPixel = 0.0

        if Result.multi_handedness:
            HandPresenceScore = float(Result.multi_handedness[0].classification[0].score)
            HandDetectedFlag = 1

        if Result.multi_hand_landmarks:
            Hand = Result.multi_hand_landmarks[0]
            HandCoordinates = [LandMark.x for LandMark in Hand.landmark]
            MinX = min(HandCoordinates) * 640
            MaxX = max(HandCoordinates) * 640
            HandWidthPixel = MaxX - MinX

        SmoothedPixel = float(self.Smooth(HandWidthPixel))

        if SmoothedPixel >= self.Threshold and HandDetectedFlag == 1:
            Status = "TOO CLOSE - NOT SAFE"
            Colour = (0, 0, 255)
        else:
            Status = "SAFE"
            Colour = (0, 255, 0)

        return HandDetectedFlag, HandPresenceScore, SmoothedPixel, Status, Colour
    
    def GetDisplay(self, Status, Frame, Colour):
        """ Shows the outcome for the current frame

        Arguments:
        - Status (str): Status of the current frame
        - Frame (np.ndarray): Current frame captured
        - Colour (tuple): Colour for the display

        Returns:
        - None
        """
        FinalStatus = f"Hand Gestures Test (Reach): {Status}"
        cv2.putText(Frame, FinalStatus, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.65, Colour, 2)
        cv2.imshow("Hand Gestures Test (Out of Frame)", Frame)

    def Live(self):
        """ For live implementation to constantly return the results

        Returns:
        - None
        """
        FrameNumber = 0
        while True: 
            FrameNumber += 1
            Frame = self.GetFrame() 
            HandDetectedFlag, HandPresenceScore, SmoothedPixel, Status, Colour = self.ProcessFrame(Frame)
            self.GetDisplay(Status, Frame, Colour)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break   

            time.sleep(1)
            yield HandDetectedFlag==1
        self.Release()

    def Run(self):
        """ Starts webcam, analyse frames, and store results in metrics

        Returns:
        - str: Sentence to confirm run finished
        """
        FrameNumber = 0

        #FirstFrame = self.GetFrame()
        #Height, Width, _ = FirstFrame.shape
        #FourCC = cv2.VideoWriter_fourcc(*"mp4v")
        #Writer = cv2.VideoWriter("Output.mp4", FourCC, 1, (Width, Height))

        while FrameNumber < self.MaxRows:
            FrameNumber += 1
            Frame = self.GetFrame()

            HandDetectedFlag, HandPresenceScore, SmoothedPixel, Status, Colour = self.ProcessFrame(Frame)

            #FinalStatus = (f"{Status} | Frame={FrameNumber} | " f"Detected={HandDetectedFlag} | " f"Conf={HandPresenceScore:.2f} | WidthPx={SmoothedPixel:.1f}")
            LogGesture(FrameNumber, HandDetectedFlag, HandPresenceScore, SmoothedPixel, Status)
            self.GetDisplay(Status, Frame, Colour)

            #Writer.write(Frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(1)

        #Writer.release()
        self.Release()
        return "Finished gesture monitoring."

    def Release(self):
        """ Kills camera feed

        Returns:
        - None
        """
        self.Cap.release()
        cv2.destroyAllWindows()