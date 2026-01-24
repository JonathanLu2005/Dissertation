import 'package:flutter/material.dart';
import 'package:firebase_database/firebase_database.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

class TrackLocation extends StatefulWidget {
  const TrackLocation({super.key});

  @override
  State<TrackLocation> createState() => TrackLocationState();
}

class TrackLocationState extends State<TrackLocation> {
  final locationStatus = FirebaseDatabase.instance.ref("LaptopLocation");

  double? latitude; 
  double? longitude; 

  @override
  void initState() {
    super.initState();
    locationStatus.onValue.listen((event) {
      final locationData = event.snapshot.value as Map?;
      if (locationData == null) return;

      setState(() {
        latitude = locationData["latitude"];
        longitude = locationData["longitude"];
      });
    });
  }

  @override 
  Widget build(BuildContext context) {
    if (latitude == null || longitude == null) {
      return const Center(child: CircularProgressIndicator());
    }

    return SizedBox(
      height: MediaQuery.of(context).size.height * 1,
      child: FlutterMap(
        options: MapOptions(
          center: LatLng(latitude!, longitude!),
          zoom: 15,
        ),
        children: [
          TileLayer(
            urlTemplate: "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
          ),
          MarkerLayer(
            markers: [
              Marker( 
                point: LatLng(latitude!, longitude!),
                child: const Icon(
                  Icons.location_pin,
                  color: Colors.red,
                  size: 40,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}