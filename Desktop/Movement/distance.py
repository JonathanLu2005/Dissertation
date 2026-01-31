import cv2
import time
import numpy as np
import mediapipe as mp
from ultralytics import YOLO
from Desktop.Movement.Metrics.metrics import LogDistance

class DistanceMonitor:
    def __init__(self):
        """ Initialise parameters to determine if persons too close and models to capture this

        Attributes:
        - Cap (cv2.VideoCapture): Laptop's camera
        - Yolo (YOLO): Model for pose detection and bounding box
        - BoxThreshold (float): Measurement of persons bounding box before they're too close
        - MpPose (mediapipe.solutions.pose): Run pose estimator
        - Pose (mediapipe.solutions.pose.Pose): Pose estimation model
        - PoseThreshold (float): Measurement of persons pose before they're too close 
        - MaxFrames (int): Number of frames to test implementation 
        - FrameNumber (int): Current frame

        Raises:
        - RuntimeError: Camera not accessible

        Returns:
        - None
        """
        #self.Cap = cv2.VideoCapture(0)
        #if not self.Cap.isOpened():
        #    raise RuntimeError("Error: Camera not accessible.")

        #self.Cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        #self.Cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.Yolo = YOLO("yolo11n.pt")

        self.BoxThreshold = 478.5
        self.MpPose = mp.solutions.pose
        self.Pose = self.MpPose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.PoseThreshold = 0.5
        self.MaxFrames = 200000
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
            raise RuntimeError("Error: Failed to read camera frame.")
        return cv2.resize(Frame, (640, 480))

    def DetectPersonHeight(self, Boxes):
        """ Extract persons bounding box

        Arguments:
        - Boxes (ultralytics.engine.results.Boxes): List of bounding box coordinates

        Returns:
        - Height (float): Persons bounding box height
        """ 
        for Box, PersonClass in zip(Boxes.xyxy, Boxes.cls):
            if int(PersonClass) == 0:
                X1, Y1, X2, Y2 = Box.cpu().numpy()
                Height = Y2 - Y1
                return Height
        return None

    def ComputeBoxStatus(self, PersonHeight):
        """ Determines if persons bounding box height is within the bounding box threshold
        
        Arguments:
        - PersonHeight (float): Persons bounding box height

        Returns:
        - Tuple:
            - Status (str): Message if persons too close or not
            - Alert (bool): True if persons too close
        """
        Alert = False
        Status = "No Person"

        if PersonHeight is not None:
            if PersonHeight > self.BoxThreshold:
                Status = "TOO CLOSE (Box)"
                Alert = True
            else:
                Status = "Safe (Box)"

        return Status, Alert

    def ComputePoseDistance(self, Landmarks, FrameShape):
        """ Measures how close a person is via their pose

        Arguments:
        - Landmarks (list): Normalised coordinates for each pose joint
        - FrameShape (tuple): Current frame dimensions
        
        Returns:
        - Tuple:
            - TorsoPixels (float): Distance between shoulders
            - Status (str): Message if persons too close or not
            - Alert (bool): True if someones too close
        """
        Alert = False 

        if Landmarks is None:
            return None, "No Person", Alert

        Left = Landmarks[self.MpPose.PoseLandmark.LEFT_SHOULDER]
        Right = Landmarks[self.MpPose.PoseLandmark.RIGHT_SHOULDER]

        Height, Weight, Channels = FrameShape
        TorsoPixels = np.linalg.norm(
            np.array([Left.x * Weight, Left.y * Height]) -
            np.array([Right.x * Weight, Right.y * Height])
        )

        if TorsoPixels > self.PoseThreshold * Weight:
            Status = "TOO CLOSE (Pose)"
            Alert = True
        else:
            Status = "Safe (Pose)"

        return TorsoPixels, Status, Alert

    def GetDisplay(self, Frame, BoxStatus, PoseStatus, FrameNumber, Torso, Height):
        """ Displays current frame and status to user

        Arguments:  
        - Frame (np.ndarray): Current frame
        - BoxStatus (str): Status of persons bounding box
        - PoseStatus (str): Status of persons pose 
        - FrameNumber (int): Current numbered frame
        
        Returns:
        - None
        """
        if "TOO CLOSE" in BoxStatus or "TOO CLOSE" in PoseStatus:
            Colour = (0, 0, 255) 
            BoxStatus = "DISTANCE - NOT SAFE"
        else: 
            Colour = (0, 255, 0)
            BoxStatus = "DISTANCE - SAFE"

        #Text = (
        #    f"{BoxStatus} | {PoseStatus} | "
        #    f"Frame {FrameNumber}/{self.MaxFrames}"
        #)

        Text = (
            f"Proximity Detection: {BoxStatus}"
        )

        if not Torso: Torso = 0 
        if not Height: Height = 0

        #Lines = [
        #    f"Proximity Detection: {BoxStatus}",
        #    f"Pose Estimation Distance: {Torso:.3f}",
        #    f"Bounding Box Height: {Height:.3f}",
        #]

        #y = 25
        #for Line in Lines:
        #    cv2.putText(Frame, Line, (10, y),
        #                cv2.FONT_HERSHEY_SIMPLEX, 0.6, Colour, 2)
        #    y += 22  

        #cv2.putText(Frame, Text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, Colour, 2)
        #cv2.imshow("Distance Monitor", Frame)

    def ProcessFrame(self, Frame):
        """ Determines if persons too close via pose and bounding box distance via current frame

        Arguments:
        - Frame (np.ndarray): Current frame

        Returns:
        - Dictionary:
            - TorsoMeasure (float): Distance between shoulders
            - PoseStatus (str): If persons pose determines they're too close
            - PoseAlert (bool): True if persons pose determines they're too close
            - BoxStatus (str): If persons bounding box determins they're too close
            - FinalStatus (str): If persons determined too close
        """
        RGBFrame = cv2.cvtColor(Frame, cv2.COLOR_BGR2RGB)

        ResultsPose = self.Pose.process(RGBFrame)
        if ResultsPose.pose_landmarks:
            Landmarks = ResultsPose.pose_landmarks.landmark 
        else: 
            Landmarks = None
        TorsoMeasure, PoseStatus, PoseAlert = self.ComputePoseDistance(Landmarks, Frame.shape)

        ResultsBox = self.Yolo(Frame, verbose=False)[0]
        PersonHeight = self.DetectPersonHeight(ResultsBox.boxes)
        BoxStatus, BoxAlert = self.ComputeBoxStatus(PersonHeight)

        FinalAlert = PoseAlert or BoxAlert

        FinalStatus = "Safe"
        if FinalAlert: 
            FinalStatus = "TOO CLOSE"

        return {
            "Torso": TorsoMeasure,
            "PoseStatus": PoseStatus,
            "PoseAlert": PoseAlert,
            "BoxStatus": BoxStatus,
            "BoxAlert": BoxAlert,
            "FinalStatus": FinalStatus,
            "Height": PersonHeight
        }
    
    def Live(self, Frame):
        """ For live implementation to constantly return the results

        Arguments:
        - Frame (np.ndarray): Current frame

        Returns:
        - (bool): True if close else false
        """
        self.FrameNumber += 1
        Results = self.ProcessFrame(Frame)
        #self.GetDisplay(Frame, Results["BoxStatus"], Results["PoseStatus"], self.FrameNumber, Results["Torso"], Results["Height"])
        return Results["PoseAlert"] or Results["BoxAlert"]

    def Run(self):
        """ Capture, process, display, and log metrics for current frame
        
        Returns:
        - str: Confirm monitoring has finished
        """

        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        FrameNumber = 0
        FinalStatus = "Unknown"
        FinalTorso = None

        FirstFrame = self.GetFrame()
        Height, Width, _ = FirstFrame.shape
        FourCC = cv2.VideoWriter_fourcc(*"avc1")
        Writer = cv2.VideoWriter("Output.mp4", FourCC, 1, (Width, Height))

        while FrameNumber < self.MaxFrames:
            FrameNumber += 1
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

            Results = self.ProcessFrame(Frame)

            FinalStatus = Results["FinalStatus"]
            FinalTorso = Results["Torso"] or 0

            LogDistance(FinalTorso, None, FinalStatus)

            self.GetDisplay(Frame, Results["BoxStatus"], Results["PoseStatus"], FrameNumber, Results["Torso"], Results["Height"])
            Writer.write(Frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            time.sleep(1)

        Writer.release()
        self.Release()
        return "Finished distance monitoring."

    def Release(self):
        """ Kills camera feed

        Returns:
        - None
        """
        #self.Cap.release()
        cv2.destroyAllWindows()
