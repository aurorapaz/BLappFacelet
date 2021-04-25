import 'package:rxdart/rxdart.dart';
import 'dart:convert' as convert;
import 'package:http/http.dart' as http;
import 'package:socket_io_client/socket_io_client.dart' as IO;
import 'dart:typed_data';
import 'dart:async';
import 'globals.dart' as globals;

class Sender {
  IO.Socket socket = IO.io('http://facelet.myddns.me:8080', <String, dynamic>{
    'transports': ['websocket']
  });
  String initialCount =
      ''; //if the data is not passed by paramether it initializes with ''
  BehaviorSubject<String> _subjectCounter;
  DateTime envioAhora = DateTime.now().subtract(Duration(minutes: 5));
  String enviar="true";
  Sender({this.initialCount}) {
    socket.on('notify', (data) {
      httpRequest();
    });
    _subjectCounter = new BehaviorSubject<String>.seeded(
        this.initialCount); //initializes the subject with element already
  }

  Stream<String> get counterObservable => _subjectCounter.stream;

  void httpRequest() async {
    var url = 'http://facelet.myddns.me:8080/';
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
    print(DateTime.now().difference(envioAhora).inMinutes);
      if (DateTime.now().difference(envioAhora).inMinutes>=5) {
        enviar="true";
      }
      if(enviar=="true"){
        envioAhora=DateTime.now();
        var url = 'http://facelet.myddns.me:8080/save';
        print(globals.email);
        print("Voy a mandar la foto al server...");
        print(DateTime.now());
        Map data = {"name": globals.email, "photo": _bytes};
        var body = convert.json.encode(data);
        // just like JS
        // Await the http get response, then decode the json-formatted response.
        var response = await http
            .post(url, body: body, headers: {"Content-Type": "application/json"});
        if (response.statusCode == 200) {
          var jsonResponse = convert.jsonDecode(response.body);

          print('$jsonResponse');
          if('$jsonResponse'=="{status: success}"){
            enviar="false";
          }
        } else {
          print('Request failed with status: ${response.statusCode}.');
        }
      }
  }

  void dispose() {
    _subjectCounter.close();
  }
}
