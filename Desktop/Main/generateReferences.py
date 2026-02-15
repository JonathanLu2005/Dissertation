import os
from pathlib import Path
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, db

def GenerateFirebase():
    """ Generate references to each database to use

    Returns:
    - (tuple):
        - BackendReference (firebase_admin.db.Reference): Allow app to send messages
        - PerformanceReference (firebase_admin.db.Reference): Allow app to send performance
        - IPReference (firebase_admin.db.Reference): Allow app to send IP used
        - AlertReference (firebase_admin.db.Reference): Allow app to get alert preferences
        - LocationReference (firebase_admin.db.Reference): Allow app to send location
        - LockingReference (firebase_admin.db.Reference): Allow app to receive locking preferences
        - ModelReference (firebase_admin.db.Reference): Allow app to receive model preferences
        - ControlPanel (firebase_admin.db.Reference): Allow app to receive panel controls
    """
    BaseDirectory = os.path.dirname(__file__)
    CredentialsPath = os.path.join(BaseDirectory, "ServiceAccountKey.json")
    Credentials = credentials.Certificate(CredentialsPath)
    load_dotenv(Path(__file__).resolve().parents[2]/".env")
    FirebaseID = os.getenv("FIREBASE_PROJECT_ID")
    firebase_admin.initialize_app(Credentials, {"databaseURL": f"https://{FirebaseID}-default-rtdb.europe-west1.firebasedatabase.app"})
    BackendReference = db.reference("BackendMessages")
    PerformanceReference = db.reference("Performance")
    IPReference = db.reference("IP")
    AlertReference = db.reference("AlertSettings/Laptop")
    LocationReference = db.reference("LaptopLocation")
    LockingReference = db.reference("LockSettings")
    ModelReference = db.reference("ModelSettings")
    ControlPanel = db.reference("RemoteControl")
    return (BackendReference, PerformanceReference, IPReference, AlertReference, LocationReference, LockingReference, ModelReference, ControlPanel)

def RetrieveControlPanel(ControlPanel):
    """ Retrieves latest controls

    Arguments:
    - ControlPanel (firebase_admin.db.Reference): Reference to user controls

    Returns:
    - (tuple):
        - PowerOn (bool): If system on
        - LockOn (bool): If lock on
        - CameraOn (bool): If camera on
    """
    ControlPanelResults = ControlPanel.get() or {}
    PowerOn = ControlPanelResults.get("power", False)
    LockOn = ControlPanelResults.get("lock", False)
    CameraOn = ControlPanelResults.get("camera", False)
    return (PowerOn, LockOn, CameraOn)

def RetrieveAlerts(AlertReference):
    """ Retrieve alert preferences

    Arguments:
    - AlertReference (firebase_admin.db.Reference): Reference to user alerts preferences

    Returns:
    - (tuple):
        - AlertsEnabled (bool): If alarms are on
        - AlertsVolume (float): Volume of alarms
    """
    AlertSettings = AlertReference.get() or {}
    AlertsEnabled = AlertSettings.get("enabled", True)
    AlertsVolume = float(AlertSettings.get("volume", 1.0))
    return (AlertsEnabled, AlertsVolume)

def RetrieveLocks(LockingReference):
    """ Retrieve locking preferences

    Arguments:
    - LockingReference (firebase_admin.db.Reference): Reference to user locking preferences
    
    Returns:
    - (tuple):
        - DetectionLock (bool): If want to lock if anythings detected
        - PowerLock (bool): If want to lock if system on
    """
    LockingSettings = LockingReference.get() or {}
    DetectionLock = LockingSettings.get("detectionlock", False)
    PowerLock = LockingSettings.get("powerlock", False)
    return (DetectionLock, PowerLock)

def RetrieveModels(ModelReference):
    """ Retrieve model settings

    Arguments:
    - ModelReference (firebase_admin.db.Reference): Reference to user model preferences

    Returns:
    - (tuple):
        - BackgroundModel (bool): If background model on
        - ProximityModel (bool): If proximity model on
        - LoiteringModel (bool): If loitering model on
        - MaskModel (bool): If mask model on
    """
    ModelSettings = ModelReference.get() or {}
    BackgroundModel = ModelSettings.get("background", True)
    ProximityModel = ModelSettings.get("proximity", True)
    LoiteringModel = ModelSettings.get("loitering", True)
    MaskModel = ModelSettings.get("mask", True)
    return (BackgroundModel, ProximityModel, LoiteringModel, MaskModel)