// Copyright 2018 The Flutter team. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
import 'dart:convert';
import 'dart:typed_data';
import 'package:async/async.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bluetooth_serial/flutter_bluetooth_serial.dart';
import 'package:provider/provider.dart';
import 'sender.dart';
import 'sing_in_page.dart';
import 'package:flutter/foundation.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'authentication_service.dart';
import 'globals.dart' as globals;

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  Widget build(BuildContext context) {
    return MaterialApp(
      home: MultiProvider(providers: [
        Provider<AuthenticationService>(
          create: (_) => AuthenticationService(FirebaseAuth.instance),
        ),
        StreamProvider(
          create: (context) =>
              context.read<AuthenticationService>().authStateChanges,
        )
      ], child: AuthenticationWrapper()),
      debugShowCheckedModeBanner: false,
    );
  }
}

class HomePage extends StatefulWidget {
  @override
  HomePage({Key key}) : super(key: key);
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> with WidgetsBindingObserver {
  BluetoothConnection connection;
  bool isConnecting = true;

  bool get isConnected => connection != null && connection.isConnected;
  bool isDisconnecting = false;
  bool connected = false;
  bool attached = false;
  String _selectedFrameSize = "2";

  List<List<int>> chunks = <List<int>>[];
  int contentLength = 0;
  Uint8List _bytes = new Uint8List(0);

  RestartableTimer _timertakephoto;
  RestartableTimer _timersavephoto;
  RestartableTimer _timerConnection;

  BluetoothState _bluetoothState = BluetoothState.UNKNOWN;

  List<BluetoothDevice> devices;
  Sender _sender = new Sender();
  @override
  void initState() {
    super.initState();
    chunks = <List<int>>[];
    contentLength = 0;
    _bytes = new Uint8List(0);
    WidgetsBinding.instance.addObserver(this);
    _timerConnection = new RestartableTimer(Duration(seconds: 30), () {
      print('Trying to conect...');
      _getBTState();
      _stateChangeListener();
    });
    _getBTState();
    _stateChangeListener();
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    if (isConnected) {
      isDisconnecting = true;
      connection.dispose();
      connection = null;
      this.connected = false;
      this.attached = false;
      if(_timertakephoto!=null)_timertakephoto.cancel();
      if(_timersavephoto!=null)_timersavephoto.cancel();
    }
    chunks = <List<int>>[];
    contentLength = 0;
    _bytes = new Uint8List(0);
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state.index == 0) {
      //resume
      if (_bluetoothState.isEnabled) {
        _listBondedDevices();
        _getBTConnection();
      }
    }
  }

  _getBTConnection() {
    if (devices != null) {
      BluetoothDevice _device;
      for (final BluetoothDevice dev in devices.toList()) {
        if (dev.name == "ESP32CAM-CLASSIC-BT") {
          _device = dev;

          BluetoothConnection.toAddress(_device.address).then((_connection) {
            connection = _connection;
            isConnecting = false;
            isDisconnecting = false;
            this.connected = true;
            this.attached = true;
            setState(() {});

            _timertakephoto = new RestartableTimer(Duration(seconds: 10), () {
              _sendMessage(_selectedFrameSize);
            });
            _timersavephoto = new RestartableTimer(Duration(seconds: 5), () {
              _saveImage();
            });
            if(_timerConnection!=null)_timerConnection.cancel();

            connection.input.listen(_onDataReceived).onDone(() {
              if (isDisconnecting) {
                print('Disconnecting locally');
                this.connected = false;
                this.attached = false;
                if(_timertakephoto!=null)_timertakephoto.cancel();
                if(_timersavephoto!=null)_timersavephoto.cancel();
                _timerConnection =
                    new RestartableTimer(Duration(seconds: 30), () {
                  print('Trying to conect...');
                  _getBTState();
                  _stateChangeListener();
                });
                chunks = <List<int>>[];
                contentLength = 0;
                _bytes = new Uint8List(0);
              } else {
                print('Disconnecting remotely');
                this.connected = false;
                this.attached = false;
                if(_timertakephoto!=null)_timertakephoto.cancel();
                if(_timersavephoto!=null)_timersavephoto.cancel();
                _timerConnection =
                    new RestartableTimer(Duration(seconds: 30), () {
                  print('Trying to conect...');
                  _getBTState();
                  _stateChangeListener();
                });
                chunks = <List<int>>[];
                contentLength = 0;
                _bytes = new Uint8List(0);
              }
              if (this.mounted) {
                setState(() {});
              }
            });
          }).catchError((error) {
            this.attached = false;
            if(_timerConnection!=null)_timerConnection.cancel();
            _timerConnection = new RestartableTimer(Duration(seconds: 30), () {
              print('Trying to conect...');
              _getBTState();
              _stateChangeListener();
            });
            chunks = <List<int>>[];
            contentLength = 0;
            _bytes = new Uint8List(0);
          });
        } else {
         if(_timerConnection!=null) _timerConnection.cancel();
          this.attached = false;
          _timerConnection = new RestartableTimer(Duration(seconds: 30), () {
            print('Trying to conect...');
            _getBTState();
            _stateChangeListener();
          });
          chunks = <List<int>>[];
          contentLength = 0;
          _bytes = new Uint8List(0);
        }
      }
    }
  }

  void _onDataReceived(Uint8List data) {
    if (data != null && data.length > 0) {
      chunks.add(data);
      contentLength += data.length;
      print(contentLength);
    }
    //print("Data Length: ${data.length}, chunks: ${chunks.length}");
    if(_timertakephoto!=null)_timertakephoto.cancel();
    _timertakephoto = new RestartableTimer(Duration(seconds: 10), () {
      _sendMessage(_selectedFrameSize);
    });
    _timersavephoto.reset();
  }

  void _sendMessage(String text) async {
    text = text.trim();
    print("I'm going to send a message");
    if (text.length > 0) {
      try {
        connection.output.add(utf8.encode(text));
        await connection.output.allSent;
        _timersavephoto.reset();
      } catch (e) {
        setState(() {});
      }
    }
  }

  _saveImage() {
    print(contentLength);
    if (chunks.length == 0 || contentLength < 50000) {
      if(_timertakephoto!=null)_timertakephoto.cancel();
      _timertakephoto = new RestartableTimer(Duration(seconds: 2), () {
        _sendMessage(_selectedFrameSize);
      });
      contentLength = 0;
      chunks.clear();
      return;
    } else {
      if(_timertakephoto!=null)_timertakephoto.cancel();
      _timertakephoto = new RestartableTimer(Duration(seconds: 10), () {
        _sendMessage(_selectedFrameSize);
      });
    }

    _bytes = Uint8List(contentLength);
    int offset = 0;
    for (final List<int> chunk in chunks) {
      _bytes.setRange(offset, offset + chunk.length, chunk);
      offset += chunk.length;
    }
    setState(() {});

    contentLength = 0;
    chunks.clear();
    print('saving photo');
    _sender.httpPostRequest(_bytes);
    _timertakephoto.reset();
    _timersavephoto.reset();
  }

  _getBTState() {
    FlutterBluetoothSerial.instance.state.then((state) {
      _bluetoothState = state;
      if (_bluetoothState.isEnabled) {
        this.connected = true;
        _listBondedDevices();
        _getBTConnection();
      } else {
        this.connected = false;
        this.attached = false;
        if(_timertakephoto!=null)_timertakephoto.cancel();
        if(_timersavephoto!=null)_timersavephoto.cancel();
      }
      setState(() {});
    });
  }

  _stateChangeListener() {
    FlutterBluetoothSerial.instance
        .onStateChanged()
        .listen((BluetoothState state) {
      _bluetoothState = state;
      if (_bluetoothState.isEnabled) {
        _listBondedDevices();
        _getBTConnection();
      } else {
        devices.clear();
        this.attached = false;
        this.connected = false;
        if(_timertakephoto!=null)_timertakephoto.cancel();
        if(_timersavephoto!=null)_timersavephoto.cancel();
      }
      print("State isEnabled: ${state.isEnabled}");
      setState(() {});
    });
  }

  _listBondedDevices() {
    FlutterBluetoothSerial.instance
        .getBondedDevices()
        .then((List<BluetoothDevice> bondedDevices) {
      devices = bondedDevices;
      setState(() {});
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: PreferredSize(
        preferredSize: Size.fromHeight(70.0), // here the desired height
        child: AppBar(
          backgroundColor: Colors.indigoAccent[700],
          title: Center(
            child: Padding(
              padding: EdgeInsets.only(top: 10),
              child: Image.asset(
                'assets/images/top.png',
                height: 80,
                width: 120,
                fit: BoxFit.fitWidth,
              ),
            ),
          ),
        ),
      ),
      body: Center(
        child: Column(
          children: <Widget>[
            Padding(
              padding: EdgeInsets.all(20.0),
              child: Text(
                'Aplicación bluetooth para envío de fotos do dispositivo PIN',
                textAlign: TextAlign.center,
                style: TextStyle(
                    fontSize: 15.0,
                    fontWeight: FontWeight.bold,
                    color: Colors.black45),
              ),
            ),
            SwitchListTile(
              title: Text('Activa Bluetooth'),
              value: _bluetoothState.isEnabled,
              onChanged: (bool value) {
                if (value) {
                  FlutterBluetoothSerial.instance.requestEnable();
                  this.connected = true;
                } else {
                  FlutterBluetoothSerial.instance.requestDisable();
                  this.connected = false;
                  this.attached = false;
                }
                setState(() {});
              },
            ),
            this.connected && !this.attached
                ? ListTile(
                    title: Text("Conectate !"),
                    trailing: ElevatedButton(
                      child: Text("Axustes"),
                      onPressed: () {
                        FlutterBluetoothSerial.instance.openSettings();
                      },
                    ),
                  )
                : Padding(padding: EdgeInsets.all(0), child: Text('')),
            this.connected && this.attached
                ? Padding(
                    padding: EdgeInsets.all(20.0),
                    child: Text(
                      'CONECTADO A ESP32-CAM',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                          fontSize: 15.0,
                          fontWeight: FontWeight.bold,
                          color: Colors.black45),
                    ),
                  )
                : Padding(padding: EdgeInsets.all(0), child: Text('')),
            ElevatedButton(
                child: Text("Pechar sesión"),
                onPressed: () {
                  FlutterBluetoothSerial.instance.requestDisable();
                  this.connected = false;
                  this.attached = false;
                  setState(() {});
                  dispose();
                  context.read<AuthenticationService>().signOut();
                }),
            // this.attached
            //     ? Container(
            //         width: 160,
            //         height: 120,
            //         decoration: BoxDecoration(
            //           image: new DecorationImage(
            //               fit: BoxFit.cover,
            //               image: MemoryImage(_bytes, scale: 1.0)),
            //         ),
            //       )
            //     : Container(),
          ],
        ),
      ),
      bottomNavigationBar: Stack(
        children: [
          new Container(
            height: 40.0,
            color: Colors.indigoAccent[700],
          ),
          Padding(
            padding: EdgeInsets.all(10.0),
            child: Row(
                mainAxisAlignment: MainAxisAlignment
                    .center, //Center Row contents horizontally,
                crossAxisAlignment:
                    CrossAxisAlignment.end, //Center Row contents vertically,
                children: [
                  Text(
                    '© Facelet',
                    style: TextStyle(
                        fontSize: 15.0,
                        fontWeight: FontWeight.normal,
                        color: Colors.white),
                  ),
                ]),
          ),
        ],
      ),
    );
  }
}

class AuthenticationWrapper extends StatelessWidget {
  const AuthenticationWrapper({
    Key key,
  }) : super(key: key);
  @override
  Widget build(BuildContext context) {
    final firebaseUser = context.watch<User>();
    if (firebaseUser != null) {
      return HomePage();
    } else {
      return Scaffold(
        appBar: PreferredSize(
          preferredSize: Size.fromHeight(70.0), // here the desired height
          child: AppBar(
            backgroundColor: Colors.indigoAccent[700],
            title: Center(
              child: Padding(
                padding: EdgeInsets.only(top: 10),
                child: Image.asset(
                  'assets/images/top.png',
                  height: 80,
                  width: 120,
                  fit: BoxFit.fitWidth,
                ),
              ),
            ),
          ),
        ),
        body: SignInPage(),
        bottomNavigationBar: Stack(
          children: [
            new Container(
              height: 40.0,
              color: Colors.indigoAccent[700],
            ),
            Padding(
              padding: EdgeInsets.all(10.0),
              child: Row(
                  mainAxisAlignment: MainAxisAlignment
                      .center, //Center Row contents horizontally,
                  crossAxisAlignment:
                      CrossAxisAlignment.end, //Center Row contents vertically,
                  children: [
                    Text(
                      '© Facelet',
                      style: TextStyle(
                          fontSize: 15.0,
                          fontWeight: FontWeight.normal,
                          color: Colors.white),
                    ),
                  ]),
            ),
          ],
        ),
      );
    }
  }
}
