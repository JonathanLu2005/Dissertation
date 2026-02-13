import 'dart:math';

class LocationService {
  bool trackLocation = false;
  double trackedLatitude = 0;
  double trackedLongitude = 0;

  void processLocation({
    required Map locationData,
    required bool powerOn,
    required bool alertsEnabled,
    required bool vibrationEnabled,
    required Function() alarm,
    required Function() vibrate,
    required Function(String) onMessage,
    required Function(Map<String, dynamic>) backendUpdate,
  }) {
    final double? latitude = locationData["latitude"] as double?;
    final double? longitude = locationData["longitude"] as double?;

    if (latitude == null || longitude == null) return;

    if (!trackLocation) {
      trackedLatitude = latitude;
      trackedLongitude = longitude;
      trackLocation = true;
      return;
    }

    const Radius = 6371000;
    final Phi1 = trackedLatitude * pi / 180;
    final Phi2 = latitude * pi / 180;
    final DistancePhi = (latitude - trackedLatitude) * pi / 180;
    final DistanceLambda = (longitude - trackedLongitude) * pi / 180;

    final Calculation = sin(DistancePhi / 2) * sin(DistancePhi / 2) + cos(Phi1) * cos(Phi2) * sin(DistanceLambda / 2) * sin(DistanceLambda / 2);
    final Result = 2 * atan2(sqrt(Calculation), sqrt(1-Calculation)) * Radius;
    if (Result > 4.2) {
      const receivedMessage = "Suspicious activity detected";

      onMessage(receivedMessage);
      backendUpdate({"message": receivedMessage});

      if (powerOn) {
        if (alertsEnabled) {
          alarm();
        }

        if (vibrationEnabled) {
          vibrate();
        }
      }
    }
  }

  void reset() {
    trackLocation = false;
  }
}