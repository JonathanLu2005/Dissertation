from Desktop.Lingering.Metrics.metrics import LogLingering
import cv2
import mediapipe as mp
import time

class LingeringMonitor:
    def __init__(self):
        """ Initialise lingering detection

        Attributes:
        - Cap (cv2.VideoCapture): Current camera feed
        - MpPose (module): Mediapipes pose module
        - Pose (mediapipe.python.solutions.pose.Pose): Pose estimation model
        - LoiteringThreshold (int): Time taken till person is determined to be lingering
        - MaxFrames (int): Frames specified to record for evaluation
        - PersonDetected (bool): True if model finds a person
        - StartTime (float): Timestamp when persons detected to determine if they've lingered
        - FrameNumber (int): Keep track on frame number

        Raises:
        - RuntimeError: Camera not accessible

        Returns:
        - None
        """
        #self.Cap = cv2.VideoCapture(0)
        #if not self.Cap.isOpened():
        #    raise RuntimeError("Camera not accessible.")

        self.MpPose = mp.solutions.pose
        self.Pose = self.MpPose.Pose(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.LoiteringThreshold = 10
        self.MaxFrames = 60000
        self.PersonDetected = False
        self.StartTime = None
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
            raise RuntimeError("Camera failed.")
        return cv2.resize(Frame, (900, 700))
    
    def ProcessFrame(self, Landmarks):
        """ Analyse through models landmarks and determine if persons present and is lingering

        Arguments:
        - Landmarks (mediapipe.python.solution_base.SolutionOutputs): Mediapipe Pose landmarks for current frame

        Returns:
        - Tuple:
            - Status (str): String to confirm state of current frame
            - Colour (tuple[int, int, int]): RGB value for UI displaying landmarks
            - DwellTime (float): Time current persons been detected for
        """     
        if Landmarks.pose_landmarks:
            if not self.PersonDetected:
                self.PersonDetected = True
                self.StartTime = time.time()
            DwellTime = time.time() - self.StartTime

            if DwellTime >= self.LoiteringThreshold:
                Status = "LOITERING - NOT SAFE"
                Colour = (0, 0, 255)
            else:
                Status = "PRESENT - SAFE"
                Colour = (0, 255, 0)
        else:
            self.PersonDetected = False
            self.StartTime = None
            DwellTime = 0.0
            Status = "NO PERSON"
            Colour = (0, 255, 0)

        return Status, Colour, DwellTime
    
    def GetDisplay(self, Status, Frame, Colour):
        """ Shows the outcome for the current frame

        Arguments:
        - Status (str): Status of the current frame
        - Frame (np.ndarray): Current frame captured
        - Colour (tuple): Colour for the display

        Returns:
        - bool: True if person is loitering
        """
        #UI = f"{Status} | Conf={Confidence:.1f} | BBox={BoundingBox:.0f} | Time={DwellTime:.1f}s | Frame={FrameNumber}/{self.MaxFrames}"
        #UI = f"Loitering False Positives (Object): {Status}"

        try: 
            Time = time.time() - self.StartTime
        except:
            Time = 0
        #Lines = [
        #    f"Loitering Detection: {Status}",
        #    f"Time: {Time:.3f}",
        #]
        
        #y = 25
        #for Line in Lines:
        #    cv2.putText(Frame, Line, (10, y),
        #                cv2.FONT_HERSHEY_SIMPLEX, 0.6, Colour, 2)
        #    y += 22 
        
        #cv2.putText(Frame, UI, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, Colour, 2)
        #cv2.imshow("Linger Experiment (1 FPS)", Frame)
        if Colour == (0, 255, 0):
            return False 
        return True

    def Live(self, Frame):
        """ Live implementation for constant running of the system

        Arguments:
        - Frame (np.ndarray): Current frame captured

        Returns:
        - FinalResult (bool): True if loitering else false
        """
        self.FrameNumber += 1
        RGB = cv2.cvtColor(Frame, cv2.COLOR_BGR2RGB)
        Result = self.Pose.process(RGB)
        Status, Colour, DwellTime = self.ProcessFrame(Result)
        FinalResult = self.GetDisplay(Status, Frame, Colour)
        return FinalResult

    def Run(self):
        """ Runs functions to retrieve current frames, run it through model, and process frame

        Returns:
        - str: Confirm run is completed
        """
        FrameNumber = 0

        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
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

            RGB = cv2.cvtColor(Frame, cv2.COLOR_BGR2RGB)
            Result = self.Pose.process(RGB)

            Status, Colour, DwellTime = self.ProcessFrame(Result)

            LogLingering(FrameNumber, int(self.PersonDetected), 0, DwellTime, Status)
            FinalResult = self.GetDisplay(Status, Frame, Colour)
            Writer.write(Frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(1)

        self.Release()
        Writer.release()
        return "Lingering monitoring finished."

    def Release(self):
        """ Kills camera feed

        Returns:
        - None
        """
        #self.Cap.release()
        cv2.destroyAllWindows()