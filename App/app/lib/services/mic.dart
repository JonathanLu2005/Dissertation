import 'dart:typed_data';
import 'dart:async';
import 'package:flutter_sound/flutter_sound.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:permission_handler/permission_handler.dart';

class MicStreamer {
  final FlutterSoundRecorder micRecorder = FlutterSoundRecorder();
  WebSocketChannel? channel;
  StreamController<Uint8List>? audioStream;

  Future<void> startRecording() async {
    await Permission.microphone.request();
    await micRecorder.openRecorder();

    channel = WebSocketChannel.connect(Uri.parse("ws://172.25.11.164:8765"),);

    audioStream = StreamController<Uint8List>();
    audioStream!.stream.listen((buffer) {
      if (channel != null && buffer.isNotEmpty) {
        channel!.sink.add(buffer);
      }
    });

    await micRecorder.startRecorder(
      codec: Codec.pcm16,
      numChannels: 1,
      sampleRate: 16000,
      bufferSize: 2048,
      toStream: audioStream!.sink,
    );
  }

  Future<void> stopRecording() async {
    await micRecorder.stopRecorder();
    await micRecorder.closeRecorder();
    await channel?.sink.close();
    channel = null;
  }
}