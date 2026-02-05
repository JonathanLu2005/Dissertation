from winrt.windows.devices.geolocation import Geolocator 

async def GetLocation():
    """ Retrieve laptop longitude and latitude coordinates

    Returns:
    - (float): Latitude value
    - (float): Longitude value
    """
    Location = Geolocator()
    Location.desired_accuracy_in_meters = 50
    Position = await Location.get_geoposition_async()
    Coordinates = Position.coordinate.point.position 
    return Coordinates.latitude, Coordinates.longitude