import cv2
import time
import os
from dotenv import load_dotenv
from pathlib import Path
import tempfile
from inference_sdk import InferenceHTTPClient
from Desktop.Mask.Metrics.metrics import LogMask

# https://universe.roboflow.com/joseph-nelson/mask-wearing
class MaskMonitor:
    def __init__(self):
        """ Instantiate attributes to run the model

        Attributes:
        - APIKey (str): Roboflow API key for the model
        - Cap (cv2.VideoCapture): Camera used
        - Client (InferenceHTTPClient): Call to use account for the model
        - ModelID (str): Name of the model used
        - MaxFrames (int): Max number of frames to test monitor on
        - FrameNumber (int): Current frame

        Raises:
        - RuntimeError: Camera not accessible

        Returns:
        - None
        """
        load_dotenv(Path(__file__).resolve().parents[2]/".env")
        self.__APIKey = os.getenv("ROBOFLOW_API_KEY")
        #self.Cap = cv2.VideoCapture(0)
        #if not self.Cap.isOpened():
        #    raise RuntimeError("Camera not accessible.")

        self.Client = InferenceHTTPClient(api_url="https://serverless.roboflow.com", api_key=self.__APIKey)
        self.ModelID = "mask-wearing/18"
        self.MaxFrames = 120
        self.FrameNumber = 0

    def GetFrame(self):
        """ Retrieve current frame

        Returns:
        - np.ndarray: Frame retrieved

        Raises:
        - RuntimeError: Camera fails to return frame
        """
        Ret, Frame = self.Cap.read()
        if not Ret:
            raise RuntimeError("Error: Failed to read camera frame.")
        return cv2.resize(Frame, (640, 480))

    def RunInference(self, Frame):
        """ Convert the current frame to provide to the API and retrieve predictions

        Arguments:
        - Frame (np.ndarray): Current video frame

        Returns:
        - list[dict]: Results from the model
        """
        TempFile = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        try:
            cv2.imwrite(TempFile.name, Frame)
            TempFile.close()
            Result = self.Client.infer(TempFile.name, model_id=self.ModelID)
        finally:
            os.unlink(TempFile.name)

        return Result.get("predictions", [])
    
    def ProcessFrame(self, Detections):
        """ Retrieve the model results and extract its most confident outcome and return values reflecting that

        Arguments:
        - Detections (list[dict]): Results of the model for the current frame

        Returns:
        - Tuple:
            - bool: True if person is wearing mask
            - Confidence (float): Confidence in the result
        """
        if not Detections:
            return False, 0.0

        MostConfident = max(Detections, key=lambda d: d["confidence"])

        Label = MostConfident["class"]
        Confidence = float(MostConfident["confidence"])

        if Label == "mask":
            return True, Confidence
        return False, Confidence

    def GetDisplay(self, Frame, Detections, Masked):
        """ Retrieve the current frame and its results to display onto the screen

        Arguments:
        - Frame (np.ndarray): Current frame
        - Detections (list[dict]): Result of current frame from model
        - Masked (bool): True if the person is wearing a mask

        Returns:
        - None
        """
        if Masked:
            Colour = (0, 0, 255)
            Status = "MASK DETECTED - SUSPICIOUS"
        else:
            Colour = (0, 255, 0)
            Status = "NO MASK - SAFE"

        #for Detection in Detections:
        #    x1 = int(Detection["x"] - Detection["width"] / 2)
        #    y1 = int(Detection["y"] - Detection["height"] / 2)
        #    x2 = int(Detection["x"] + Detection["width"] / 2)
        #    y2 = int(Detection["y"] + Detection["height"] / 2)
        #    Label = f'{Detection["class"]} {Detection["confidence"]:.2f}'
        #    cv2.rectangle(Frame, (x1, y1), (x2, y2), Colour, 2)
        #    cv2.putText(Frame, Label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, Colour, 2)

        UI = f"Mask False Positives (Object): {Status}"

        #Lines = [
        #    f"Mask Detection: {Status}",
        #]

        #y = 25
        #for Line in Lines:
        #    cv2.putText(Frame, Line, (10, y),
        #                cv2.FONT_HERSHEY_SIMPLEX, 0.6, Colour, 2)
        #    y += 22  

        #cv2.putText(Frame, UI, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, Colour, 2)
        #cv2.imshow("Mask Experiment (1 FPS)", Frame)
        return Status
    
    def Live(self, Frame):
        """ For live implementation to constantly return the results

        Arguments:
        - Frame (np.ndarray): Current frame captured

        Returns:
        - Masked (bool): True if mask is worn else false
        """
        self.FrameNumber += 1
        Detections = self.RunInference(Frame)
        Masked, Confidence = self.ProcessFrame(Detections)
        #Status = self.GetDisplay(Frame, Detections, Masked)
        return Masked

    def Run(self):
        """ Capture, call API, retrieve and display results for each frame

        Returns:
        - Tuple:
            - Status (str): Outcome of the last frame
            - Confidence (float): Confidence in outcome
        """
        FrameNumber = 0
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        FirstFrame = self.GetFrame()
        Height, Width, _ = FirstFrame.shape
        FourCC = cv2.VideoWriter_fourcc(*"mp4v")
        Writer = cv2.VideoWriter("MaskOutput.mp4", FourCC, 1, (Width, Height))

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

            Detections = self.RunInference(Frame)
            Masked, Confidence = self.ProcessFrame(Detections)

            Status = self.GetDisplay(Frame, Detections, Masked)

            LogMask(FrameNumber, Status, Confidence)
            Writer.write(Frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(1)

        self.Release()
        Writer.release()
        return "Mask monitoring finished."

    def Release(self):
        """ Kills camera feed

        Returns:
        - None
        """
        #self.Cap.release()
        cv2.destroyAllWindows()