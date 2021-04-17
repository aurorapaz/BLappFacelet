import 'package:rxdart/rxdart.dart';
import 'dart:convert' as convert;
import 'package:http/http.dart' as http;
import 'package:socket_io_client/socket_io_client.dart' as IO;
import 'dart:typed_data';
import 'dart:async';
import 'globals.dart' as globals;

class Sender {
  IO.Socket socket = IO.io('http://facelet.ddns.net:8080', <String, dynamic>{
    'transports': ['websocket']
  });
  String initialCount =
      ''; //if the data is not passed by paramether it initializes with ''
  BehaviorSubject<String> _subjectCounter;

  Sender({this.initialCount}) {
    socket.on('notify', (data) {
      print(data);
      httpRequest();
    });
    _subjectCounter = new BehaviorSubject<String>.seeded(
        this.initialCount); //initializes the subject with element already
  }

  Stream<String> get counterObservable => _subjectCounter.stream;

  void httpRequest() async {
    var url = 'http://facelet.ddns.net:8080/';
    // Await the http get response, then decode the json-formatted response.
    var response = await http.get(url);
    if (response.statusCode == 200) {
      var jsonResponse = convert.jsonDecode(response.body);
      _subjectCounter.sink.add(response.body);
      print('Number of books about http: $jsonResponse.');
    } else {
      print('Request failed with status: ${response.statusCode}.');
    }
  }

  void httpPostRequest(Uint8List _bytes) async {
    var url = 'http://facelet.ddns.net:8080/save';
  print(globals.email);
    Map data = {"name": globals.email, "photo": _bytes};
    var body = convert.json.encode(data);
    // just like JS
    // Await the http get response, then decode the json-formatted response.
    var response = await http
        .post(url, body: body, headers: {"Content-Type": "application/json"});
    if (response.statusCode == 200) {
      var jsonResponse = convert.jsonDecode(response.body);

      print('$jsonResponse');
    } else {
      print('Request failed with status: ${response.statusCode}.');
    }
  }

  void dispose() {
    _subjectCounter.close();
  }
}
