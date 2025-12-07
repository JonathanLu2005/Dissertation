from Desktop.Lingering.Metrics.metrics import LogLingering
import cv2
import mediapipe as mp
import time

class LingeringMonitor:
    def __init__(self, LingeringThreshold=10, MaxRows=60, CameraIndex=0):
        """ Initialise lingering detection

        Arguments:
        - LingeringThreshold (int): Time taken till person is determined to be lingering
        - MaxRows (int): Frames specified to record for evaluation
        - CameraIndex (int): Positioning of the camera

        Attributes:
        - Cap (cv2.VideoCapture): Current camera feed
        - MPPose (module): Mediapipes pose module
        - Pose (mediapipe.python.solutions.pose.Pose): Pose estimation model
        - LingeringThreshold (int): Time taken till person is determined to be lingering
        - MaxRows (int): Frames specified to record for evaluation
        - PersonDetected (bool): True if model finds a person
        - StartTime (float): Timestamp when persons detected to determine if they've lingered

        Raises:
        - RuntimeError: Camera not accessible

        Returns:
        - None
        """
        self.Cap = cv2.VideoCapture(CameraIndex)
        if not self.Cap.isOpened():
            raise RuntimeError("Camera not accessible.")

        self.MPPose = mp.solutions.pose
        self.Pose = self.MPPose.Pose(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.LingeringThreshold = LingeringThreshold
        self.MaxRows = MaxRows
        self.PersonDetected = False
        self.StartTime = None

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
        return cv2.resize(Frame, (900, 700))
    
    def ProcessFrame(self, Result):
        """ Analyse through models result and determine if persons present and is lingering

        Arguments:
        - Result (mediapipe.python.solution_base.SolutionOutputs): Mediapipe Pose results for current frame

        Returns:
        - Tuple:
            - Status (str): String to confirm state of current frame
            - Colour (tuple[int, int, int]): RGB value for UI displaying results
            - DwellTime (float): Time current persons been detected for
            - Confidence (float): Confidence in detecting the person
            - BoundingBox (float): Estimates persons bounding box
        """     
        Confidence = 0.0
        BoundingBox = 0.0

        if Result.pose_landmarks:
            Confidence = 1.0
            Landmarks = Result.pose_landmarks.landmark
            xs = [Point.x * 900 for Point in Landmarks]
            ys = [Point.y * 700 for Point in Landmarks]
            BoundingBox = (max(xs) - min(xs)) * (max(ys) - min(ys))

            if not self.PersonDetected:
                self.PersonDetected = True
                self.StartTime = time.time()
            DwellTime = time.time() - self.StartTime

            if DwellTime >= self.LingeringThreshold:
                Status = "LINGERING"
                Colour = (0, 0, 255)
            else:
                Status = "PRESENT"
                Colour = (0, 255, 0)
        else:
            self.PersonDetected = False
            self.StartTime = None
            DwellTime = 0.0
            Status = "NO_PERSON"
            Colour = (255, 255, 255)

        return Status, Colour, DwellTime, Confidence, BoundingBox

    def Run(self):
        """ Runs functions to retrieve current frames, run it through model, and process frame

        Returns:
        - str: Confirm run is completed
        """
        FrameNumber = 0

        while FrameNumber < self.MaxRows:
            FrameNumber += 1
            Frame = self.GetFrame()
            RGB = cv2.cvtColor(Frame, cv2.COLOR_BGR2RGB)
            Result = self.Pose.process(RGB)

            Status, Colour, DwellTime, Confidence, BoundingBox = self.ProcessFrame(Result)

            LogLingering(FrameNumber, int(self.PersonDetected), Confidence, DwellTime, Status)
            UI = f"{Status} | Conf={Confidence:.1f} | BBox={BoundingBox:.0f} | Time={DwellTime:.1f}s | Frame={FrameNumber}/{self.MaxRows}"
            cv2.putText(Frame, UI, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, Colour, 2)
            cv2.imshow("Linger Experiment (1 FPS)", Frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(1)

        self.Release()
        return "Experiment finished."

    def Release(self):
        """ Kills camera feed

        Returns:
        - None
        """
        self.Cap.release()
        cv2.destroyAllWindows()