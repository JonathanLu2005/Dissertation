import 'package:app/widgets/navigation.dart';
import 'package:flutter/material.dart';
import '../services/images.dart';
import '../services/TTS.dart';

class GalleryPage extends StatefulWidget {
  const GalleryPage({super.key});

  @override 
  State<GalleryPage> createState() => _GalleryPageState();
}

class _GalleryPageState extends State<GalleryPage> {
  @override
  void initState() {
    super.initState();
    TTSService.pageAnnouncement("Gallery");
  }

  @override 
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Gallery"),
        backgroundColor: const Color(0xFFEFF2F1)
      ),
      bottomNavigationBar: const AppNavigationBar(currentPage: 2),
      body: StreamBuilder(
        stream: GalleryService.retrieveImages(),
        builder: (context, snapshot) {
          if (!snapshot.hasData) {
            return const Center(child: CircularProgressIndicator());
          }

          final images = snapshot.data!;

          return GridView.builder(
            padding: const EdgeInsets.all(8),
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount( 
              crossAxisCount: 3,
              mainAxisSpacing: 6,
              crossAxisSpacing: 6,
            ),
            itemCount: images.length,
            itemBuilder: (context, i) {
              return Image.network(
                images[i]["image_url"],
                fit: BoxFit.cover,
                loadingBuilder: (context, child, progress) {
                  if (progress == null) return child;
                  return const Center(child: CircularProgressIndicator(strokeWidth: 1));
                },
              );
            },
          );
        },
      ),
    );
  }
}