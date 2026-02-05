import cv2

class CameraManager:
    def __init__(self):
        """ Retrieve frames from camera to analyse

        Attributes:
        - Cap (cv2.VideoCapture): Camera
        - Frame (np.ndarray): Current frame

        Raises:
        - RuntimeError: Camera not accessible

        Returns:
        - None
        """
        self.Cap = cv2.VideoCapture(0)
        if not self.Cap.isOpened():
            raise RuntimeError("Can't access camera")
        self.Frame = None 
    
    def GetFrame(self):
        """ Return current frame

        Returns:
        - Frame (np.ndarray): Current frame
        """
        Ret, Frame = self.Cap.read()
        if not Ret:
            return None 
        self.Frame = cv2.resize(Frame, (900, 700))
        return self.Frame
    
    def Release(self):
        """ Turns off camera

        Returns:
        - None
        """
        self.Cap.release()