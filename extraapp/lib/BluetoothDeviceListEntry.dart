import 'package:flutter/material.dart';
import 'package:flutter_bluetooth_serial/flutter_bluetooth_serial.dart';

class BluetoothDeviceListEntry extends ListTile {
  BluetoothDeviceListEntry({
    @required BluetoothDevice device,
    int rssi,
    GestureTapCallback onTap,
    GestureLongPressCallback onLongPress,
    bool enabled = true,
  }) : super(
          onTap: onTap,
          onLongPress: onLongPress,
          enabled: enabled,
          title: Text(
            "Conectado a...",
            textAlign: TextAlign.center,
          ),
          subtitle: Text(
            device.name ?? "No conocido",
            textAlign: TextAlign.center,
          ),
          // trailing: Row(
          //   mainAxisSize: MainAxisSize.min,
          //   children: <Widget>[
          //     rssi != null
          //         ? Container(
          //             margin: new EdgeInsets.all(8.0),
          //             child: DefaultTextStyle(
          //               style: _computeTextStyle(rssi),
          //               child: Column(
          //                 mainAxisSize: MainAxisSize.min,
          //                 children: <Widget>[
          //                   Text(rssi.toString()),
          //                   Text('dBm'),
          //                 ],
          //               ),
          //             ),
          //           )
          //         : Container(width: 0, height: 0),
          //     device.isConnected
          //         ? Icon(Icons.import_export)
          //         : Container(width: 0, height: 0),
          //     device.isBonded
          //         ? Icon(Icons.link)
          //         : Container(width: 0, height: 0),
          //   ],
          // ),
        );
}
