import csv
import os

LogFile = os.path.join(os.path.dirname(__file__), "LingeringLog.csv")
if not os.path.exists(LogFile):
    with open(LogFile, "w", newline="") as File:
        Writer = csv.Writer(File)
        Writer.writerow(["FrameNumber", "PersonDetected", "Confidence", "DwellTime", "Status"])

def LogLingering(FrameNumber, PersonDetected, Confidence, DwellTime, Status):
    """ Stores metrics from evaluating lingering implementations

    Arguments:
    - FrameNumber (int): Current frame number
    - PersonDetected (int): 1 if persons detected else 0
    - Confidence (float): Confidence of person detection
    - DwellTime (float): Time in seconds person has been lingering
    - Status (str): Status of current frame

    Returns:
    - None
    """
    try:
        PersonDetected = int(PersonDetected)
    except:
        PersonDetected = 0

    try:
        Confidence = float(Confidence)
    except:
        Confidence = 0.0

    try:
        DwellTime = float(DwellTime)
    except:
        DwellTime = 0.0

    try:
        Status = str(Status)
    except:
        Status = "Unknown"

    with open(LogFile, "a", newline="") as File:
        Writer = csv.Writer(File)
        Writer.writerow([int(FrameNumber) if FrameNumber is not None else None, PersonDetected, round(Confidence, 3), round(DwellTime, 2), Status])