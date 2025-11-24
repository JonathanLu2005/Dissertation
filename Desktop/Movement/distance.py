import cv2
import time
import numpy as np
import mediapipe as mp
from ultralytics import YOLO
from Desktop.Movement.Metrics.metrics import LogDistance

class DistanceMonitor:
    def __init__(self, YoloModel=None, BoxThreshold=470, PoseThreshold=0.5, MaxRows=200, CameraIndex=0):
        """ Initialise parameters to determine if persons too close and models to capture this

        Arguments:
        - YoloModel (YOLO): YOLO model to determine a persons bounding box and pose
        - BoxThreshold (int): Measurement of persons bounding box before they're too close
        - PoseThreshold (float): Measurement of persons pose before they're too close
        - MaxRows (int): Number of frames to test implementation
        - CameraIndex (int): Camera index used

        Attributes:
        - Cap (cv2.VideoCapture): Laptop's camera
        - Yolo (YOLO): Model for pose detection and bounding box
        - BoxThreshold (int): Measurement of persons bounding box before they're too close
        - MpPose (mediapipe.solutions.pose): Run pose estimator
        - Pose (mediapipe.solutions.pose.Pose): Pose estimation model
        - MpDrawing (mediapipe.solutions.drawing_utils): Show pose landmarks on camera
        - PoseThreshold (float): Measurement of persons pose before they're too close 
        - MaxRows (int): Number of frames to test implementation 

        Raises:
        - RuntimeError: Camera not accessible

        Returns:
        - None
        """
        self.Cap = cv2.VideoCapture(CameraIndex)
        if not self.Cap.isOpened():
            raise RuntimeError("Error: Camera not accessible.")

        self.Cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.Cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        if YoloModel is None:
            self.Yolo = YOLO("yolo11n.pt")
        else:
            self.Yolo = YoloModel

        self.BoxThreshold = BoxThreshold

        self.MpPose = mp.solutions.pose
        self.Pose = self.MpPose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.MpDrawing = mp.solutions.drawing_utils

        self.PoseThreshold = PoseThreshold
        self.MaxRows = MaxRows

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

    def GetDisplay(self, Frame, BoxStatus, PoseStatus, FrameNumber):
        """ Displays current frame and status to user

        Arguments:
        - Frame (np.ndarray): Current frame
        - BoxStatus (str): Status of persons bounding box
        - PoseStatus (str): Status of persons pose 
        - FrameNumber (int): Current numbered frame
        
        Returns:
        - None
        """
        if "TOO CLOSE" in (BoxStatus, PoseStatus):
            Colour = (0, 0, 255) 
        else: 
            Colour = (0, 255, 0)

        Text = (
            f"{BoxStatus} | {PoseStatus} | "
            f"Frame {FrameNumber}/{self.MaxRows}"
        )

        cv2.putText(Frame, Text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, Colour, 2)
        cv2.imshow("Distance Monitor", Frame)

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
            "FinalStatus": FinalStatus
        }

    def Run(self):
        """ Capture, process, display, and log metrics for current frame
        
        Returns:
        - Tuple:
            - FinalStatus (str): Message if persons too close
            - FinalTorso (float): Measurement between shoulders
        """
        FrameNumber = 0
        FinalStatus = "Unknown"
        FinalTorso = None

        while FrameNumber < self.MaxRows:
            FrameNumber += 1
            Frame = self.GetFrame()

            Results = self.ProcessFrame(Frame)

            FinalStatus = Results["FinalStatus"]
            FinalTorso = Results["Torso"] or 0

            LogDistance(FinalTorso, None, FinalStatus)

            self.GetDisplay(
                Frame,
                Results["BoxStatus"],
                Results["PoseStatus"],
                FinalTorso,
                FrameNumber
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            time.sleep(0.3)

        self.Release()
        return FinalStatus, FinalTorso

    def Release(self):
        """ Kills camera feed

        Returns:
        - None
        """
        self.Cap.release()
        cv2.destroyAllWindows()