def SetIP(IPReference, LocalIP):
    """ Set IP used

    Arguments:
    - IPReference (firebase_admin.db.Reference): Reference to IP storage
    - LocalIP (str): Local IP used

    Returns:
    - None
    """
    IPReference.set({"ip": LocalIP})

def SetLocation(LocationReference, Latitude, Longitude):
    """ Set the current location

    - LocationReference (firebase_admin.db.Reference): Reference to location storage
    - Latitude (float): Current latitude
    - Longitude (float): Current longiutde

    Returns:
    - None
    """
    Location = {
        "latitude": Latitude,
        "longitude": Longitude,
    }
    LocationReference.set(Location)

def SetBackend(BackendReference, SuspiciousDetected, Message, Timestamp):
    """ Send message via firebase

    Arguments:
    - BackendReference (firebase_admin.db.Reference): Reference to storage for messaging
    - SuspiciousDetected (bool): True if something is detected
    - Message (str): Message of what occurred
    - Timestamp (int): Current time

    Returns:
    - None
    """
    BackendReference.set({
        "alert": SuspiciousDetected,
        "message": Message,
        "timestamp": Timestamp
    })