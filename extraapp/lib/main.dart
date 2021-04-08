// Copyright 2018 The Flutter team. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
import 'dart:convert';
import 'dart:typed_data';
import 'dart:async';
import 'package:async/async.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bluetooth_serial/flutter_bluetooth_serial.dart';
import 'package:flutter_svprogresshud/flutter_svprogresshud.dart';
import 'BluetoothDeviceListEntry.dart';
import 'sender.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bluetooth_serial/flutter_bluetooth_serial.dart';
import 'package:flutter/foundation.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: HomePage(),
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
  String _selectedFrameSize = "0";

  List<List<int>> chunks = <List<int>>[];
  int contentLength = 0;
  Uint8List _bytes = new Uint8List(0);

  RestartableTimer _timertakephoto;
  RestartableTimer _timersavephoto;

  BluetoothState _bluetoothState = BluetoothState.UNKNOWN;
  TextEditingController _controller = TextEditingController();

  List<BluetoothDevice> devices;
  Sender _sender = new Sender();
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
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
    }
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
          this.attached = true;
          _device = dev;

          BluetoothConnection.toAddress(_device.address).then((_connection) {
            connection = _connection;
            isConnecting = false;
            isDisconnecting = false;
            setState(() {});
            connection.input.listen(_onDataReceived).onDone(() {
              if (isDisconnecting) {
                print('Disconnecting locally');
              } else {
                print('Disconnecting remotely');
              }
              if (this.mounted) {
                setState(() {});
              }
            });
          }).catchError((error) {});
          _timertakephoto = new RestartableTimer(Duration(seconds: 10), () {
            _sendMessage(_selectedFrameSize);
            setState(() {});
          });
          _timersavephoto = new RestartableTimer(Duration(seconds: 8), () {
            _saveImage();
          });
        }
      }
    }
  }

  void _onDataReceived(Uint8List data) {
    if (data != null && data.length > 0) {
      chunks.add(data);
      contentLength += data.length;
    }
    //print("Data Length: ${data.length}, chunks: ${chunks.length}");
    print(data);
    _timertakephoto.reset();
    _timersavephoto.reset();
  }

  void _sendMessage(String text) async {
    text = text.trim();
    print("I'm going to send a message");
    if (text.length > 0) {
      try {
        connection.output.add(utf8.encode(text));
        await connection.output.allSent;
      } catch (e) {
        setState(() {});
      }
    }
  }

  _saveImage() {
    if (chunks.length == 0 || contentLength == 0) return;

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
                : ListTile(),
            this.connected && this.attached
                ? Expanded(
                    child: ListView(
                      children: devices != null
                          ? devices
                              .map((_device) => BluetoothDeviceListEntry(
                                    device: _device,
                                    enabled: true,
                                  ))
                              .toList()
                          : [],
                    ),
                  )
                : Expanded(child: ListView()),
            this.attached
                ? Container(
                    width: 160,
                    height: 120,
                    decoration: BoxDecoration(
                      image: new DecorationImage(
                          fit: BoxFit.cover,
                          image: MemoryImage(_bytes, scale: 1.0)),
                    ),
                  )
                : Container(),
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
