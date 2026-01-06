import csv
import os

DistanceLogFile = os.path.join(os.path.dirname(__file__), "DistanceLog.csv")
GestureLogFile = os.path.join(os.path.dirname(__file__), "GestureLog.csv")

if not os.path.exists(DistanceLogFile):
    with open(DistanceLogFile, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Distance", "Approach", "Status"])

if not os.path.exists(GestureLogFile):
    with open(GestureLogFile, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["FrameNumber", "HandDetected", "HandConfidence", "ProximityPixel", "Status"])

def LogDistance(Distance, Approach, Status):
    """ Stores the distance, approach, and status to be analysed later
    
    Arguments:
    - Distance (float): How far the person is from the webcam
    - Approach (float): How fast the person is closing into the laptop
    - Status (str): Result if persons too close or far away

    Returns:
    - None
    """
    with open(DistanceLogFile, "a", newline="") as f:
        writer = csv.writer(f) 
        writer.writerow([round(Distance, 2) if Distance is not None else None, round(Approach, 2) if Approach is not None else None, Status])

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

def LogGesture(FrameNumber, HandDetected, HandConfidence, ProximityPixel, Status):
    """ Receive the results from the frame and stores them

    Arguments:
    - FrameNumber (int): Current frame number
    - HandDetected (int): 1 if hands detected else 0
    - HandConfidence (float): How confident model is that hand is a hand
    - ProximityPixel (float): Distance of the hand from the laptop webcam
    - Status (str): If users too close or not

    Returns:
    - None
    """
    HandDetected = SafeCasting(HandDetected, int, 0)
    HandConfidence = SafeCasting(HandConfidence, float, 0.0)
    ProximityPixel = SafeCasting(ProximityPixel, float, 0.0)
    Status = SafeCasting(Status, str, "Unknown")

    with open(GestureLogFile, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([int(FrameNumber) if FrameNumber is not None else None, HandDetected, round(HandConfidence, 3), round(ProximityPixel, 2), Status])