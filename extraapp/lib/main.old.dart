import 'package:flutter/material.dart';
import 'package:flutter_bluetooth_serial/flutter_bluetooth_serial.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Welcome to Flutter',
      home: Scaffold(
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
          child: Padding(
            padding: EdgeInsets.all(20.0),
            child: Text(
              'Bo día!\n\nEsta aplicación está incluida na fase de proba do noso producto.\n\nServe para enviar as imaxes capturadas polo noso dispositivo ao teléfono móbil.\n\nUtilizará Bluetooth, o cal estará activo todo o tempo.',
              style: TextStyle(
                  fontSize: 25.0,
                  fontWeight: FontWeight.bold,
                  color: Colors.black45),
            ),
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
      ),
    );
  }
}
