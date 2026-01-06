import csv
import os

LogFile = os.path.join(os.path.dirname(__file__), "LingeringLog.csv")
if not os.path.exists(LogFile):
    with open(LogFile, "w", newline="") as File:
        writer = csv.writer(File)
        writer.writerow(["FrameNumber", "PersonDetected", "Confidence", "DwellTime", "Status"])

def SafeCasting(Metric, Cast, Default):
    """ Casting values safely in case values aren't recorded due to issue with the model

    Arguments:
    - Metric (any): Either a number from the model or string which is the status
    - Cast (any): Either int, float, str dependent on the metrics from the model
    - Default (any): Either 0 for numerical scores or a string for status

    Returns:
    - Metric (any) or Default (any): Returns the casted metric or the default result
    """
    try:
        return Cast(Metric)
    except:
        return Default

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
    PersonDetected = SafeCasting(PersonDetected, int, 0)
    Confidence = SafeCasting(Confidence, float, 0.0)
    DwellTime = SafeCasting(DwellTime, float, 0.0)
    Status = SafeCasting(Status, str, "Unknown")

    with open(LogFile, "a", newline="") as File:
        writer = csv.writer(File)
        writer.writerow([int(FrameNumber) if FrameNumber is not None else None, PersonDetected, round(Confidence, 3), round(DwellTime, 2), Status])