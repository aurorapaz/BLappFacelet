// Copyright 2018 The Flutter team. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

import 'BluetoothDeviceListEntry.dart';
import 'detailpage.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bluetooth_serial/flutter_bluetooth_serial.dart';

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
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> with WidgetsBindingObserver {
  BluetoothState _bluetoothState = BluetoothState.UNKNOWN;

  List<BluetoothDevice> devices;

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
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state.index == 0) {
      //resume
      if (_bluetoothState.isEnabled) {
        _listBondedDevices();
      }
    }
  }

  _getBTState() {
    FlutterBluetoothSerial.instance.state.then((state) {
      _bluetoothState = state;
      if (_bluetoothState.isEnabled) {
        _listBondedDevices();
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
                } else {
                  FlutterBluetoothSerial.instance.requestDisable();
                }
                setState(() {});
              },
            ),
            ListTile(
              title: Text("Conectate !"),
              trailing: ElevatedButton(
                child: Text("Axustes"),
                onPressed: () {
                  FlutterBluetoothSerial.instance.openSettings();
                },
              ),
            ),
            Expanded(
              child: ListView(
                children: devices
                    .map((_device) => BluetoothDeviceListEntry(
                          device: _device,
                          enabled: true,
                          onTap: () {
                            print("Item");
                            _startCameraConnect(context, _device);
                          },
                        ))
                    .toList(),
              ),
            )
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

  void _startCameraConnect(BuildContext context, BluetoothDevice server) {
    Navigator.of(context).push(MaterialPageRoute(builder: (context) {
      return DetailPage(server: server);
    }));
  }
}
