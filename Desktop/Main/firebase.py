import time 
import firebase_admin 
from firebase_admin import credentials, db 
import os 
from dotenv import load_dotenv 
from pathlib import Path
from Desktop.Main.main import Main
import winsound
import cv2
import ctypes

def Firebase():
    """ Establish connection to the Firebase server

    Returns:
    - None
    """
    BaseDirectory = os.path.dirname(__file__)
    CredentialsPath = os.path.join(BaseDirectory, "ServiceAccountKey.json")
    Credentials = credentials.Certificate(CredentialsPath)
    load_dotenv(Path(__file__).resolve().parents[2]/".env")
    FirebaseID = os.getenv("FIREBASE_PROJECT_ID")
    firebase_admin.initialize_app(Credentials, {"databaseURL": f"https://{FirebaseID}-default-rtdb.europe-west1.firebasedatabase.app"})
    BackendReference = db.reference("BackendMessages")
    AlertReference = db.reference("AlertSettings/Laptop")
    AppReference = db.reference("AppMessages")
    ControlPanel = db.reference("RemoteControl")

    ImagePath = os.path.join(BaseDirectory, "Warning.png")
    Warning = cv2.imread(ImagePath)
    cv2.imshow("Warning", Warning)
    cv2.waitKey(1)

    ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)

    while True:
        ControlPanelResults = ControlPanel.get() or {}
        PowerOn = ControlPanelResults.get("Power", False)

        AlertSettings = AlertReference.get() or {}
        AlertsEnabled = AlertSettings.get("enabled", True)
        AlertsVolume = float(AlertSettings.get("volume", 1.0))

        Result = False
        Message = "Powered off"

        if PowerOn:
            Message = "No suspicious activity detected"

            for Result in Main():
                break 

            if Result and AlertsEnabled:
                winsound.Beep(1500, int(500 * AlertsVolume))
                Message = "Suspicious activity detected"

        BackendReference.set({
            "alert": Result,
            "message": Message
        })

        print("Sent:", Message)
        time.sleep(3)


Firebase()