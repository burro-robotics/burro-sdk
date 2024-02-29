# Burro SDK

This user manual provides instructions for using the serial command interface of the API. It outlines various requests, responses, and commands available for controlling and querying the status of a robotic system.

We currently support two modes of connection - serial (RS232) and ethernet (Websocket). They differ in their functionality as ethernet allows higher bandwidth streams at higher frequencies.

In either case, speak with Burro technical support to enable the API use on your robots.

See the [examples](examples) in this repository to get started.

## Serial (RS232 / TTL)

The serial interface provides an easy way to communicate with Burro. You will need to aquire a USB-to-Serial converter as we don't currently support connection for the on-board serial (this may be enabled in the future depending on customer needs). It is **imperative** that a USB isolator is used in conjunction with the converter. Burro will not be held liable for damage if one is not used.

For the time being, a Burro technician will need to enable the device remotely. Let us know when you are ready to connect the device and we can walk you through it. This will be an automated step in the future.

For embdedded devices, we have included an [example](examples/serial/ClearCore/) that runs on the ClearCore I/O controller. Other devices should be similar.

### Setup

1. Plug in the isolator and USB-to-Serial converter into the USB port on the side of the robot.
2. Call a Burro technician to enable the API.
3. Activate the Serial API once it has been enabled (see images).
4. Run one of the example scripts, such as the `examples/serial/serial_api_client.py` and enter the command: `?SYSP_`

| ![](doc/images/usb_not_plugged_into_burro.jpg) | ![](doc/images/ui_navigation.jpg) |
| --- | --- |
| 1. Plug the USB-to-Serial converter into the exposed USB port | 2. Activate the API from the screen |


### RS232/TTL Configuration

| Parameter | Value |
| --- | --- |
| baudrate | 115200 |


### Overview of commands

Requests and Responses are formed as a string. A Request begins with a key character and ends in `_`. A response begins with `%`, contains the original command and has a list of responses following the `=` sign.

### Requests

| Request | Key | Purpose | Example |
| --- | --- | --- | --- |
| GetValue | ? | Retrieve a value or status | `?STTN_` - Requests the current status of the station (stopped or not). |
| SetValue | ^ | Set a specific parameter | `^STNT 1_` - Sets the Station timeout. |
| Action | @ | Command the robot to do something | `@TDIR 1_` - Commands the robot to move forward. |

### Responses

| Response | Key | Example |
| --- | --- | --- |
| Acknowledge | `#ACK` |  `%@TDIR=#ACK_` - Acknowledges the TDIR command.
| Error | `#ERR` |  `%@TDIR=#ERR_` - Indicates an error in the Target Direction command.
| Unknown | `#UNK` |  `%?TDIR=#UNK` - Indicates that the queried value is in an unknown state or has not been set.
| Value | `<list>` |  `%?STTN=1616173082013918219 1_` - Returns the timestamp (nanoseconds) and value 1 for the STTN command.

### Available Commands

| CMD | Args | Response | Description
| --- | --- | --- | --- |
| `?STTN` | - | ts bool | Returns timestamp and True if currently stopped at a station.
| `?SYSP` | - | ts bool |  Returns timestamp and True if the system is powered on and available.
| `?TDIR` | - | ts int | Gets the Target Direction in autonomy mode. Result will be -1, 0, or 1 for Reverse, Paused, and Forward respectively.
| `@TDIR` | int | ack | Sets the Target Direction in autonomy mode. This will move the robot in the desired direction. Send -1, 0, or 1 for Reverse, Paused, and Forward respectively. Mimics the Forward/Back/Stop buttons on the robot.

### String Datatypes

| Type | Description | Examples |
| --- | --- | --- |
| `bool` | True / False | `1` / `0` |
| `ts` | System timestamp in nanoseconds (Epoch / UTC) | `1616173082013918219` |
| `int` | Integer | `213`, `-31` |
| `float` | Floating point number | `8.123`, `-3.14159` |

## Websocket (Ethernet)

### Setup

1. Call a Burro technician to enable the API, who will also guide you through connecting the ethernet cable to the right port.
2. Ensure that your remote PC is setup with a static IP address in the same subnet as Burro, e.g. `192.168.3.68`. Confirm that the network configuration is correct by running `ping 192.168.3.42`.
3. Run one of the example scripts, such as `examples/rosbridge/odometry_stream.py`

The easiest way to develop using the Websocket API is to use [roslibpy](https://roslibpy.readthedocs.io/en/latest/). Here is an example that will listen to the robot's odometry:

``` python
#!/usr/bin/env python
import roslibpy

client = roslibpy.Ros(host='192.168.3.42', port=9090)
client.run()

def callback(msg):
    position = msg['pose']['pose']['position']
    print(f"Received Pose: x={position['x']}, y={position['y']}")

listener = roslibpy.Topic(client, '/odometry/filtered', 'nav_msgs/Odometry')
listener.subscribe(callback)

try:
    while True:
        pass
except KeyboardInterrupt:
    client.terminate()

```

A similar library can be created in C or C++ that follows the same Websocket protocol.

### Available Streams
The definitions of these can be found in the ROS documentation.

| Stream ID | Type | Description |
| --- | --- | --- |
|`/motion/speed` | `std_msgs/Float64` | The current maximum speed the robot is set to travel at. Negative values means the robot intends to travel in reverse. If the value is zero, then the robot will be stopped. |
| `/odometry/filtered` | `nav_msgs/Odometry` | The local fused odometry from all odometry sources, i.e. the best source of locally smooth and consistent odometry. |
| `/gps_rover/fix` | `sensor_msgs/NavSatFix` | The GNSS solution. This will return the GNSS position of the antenna (not the robot center). |

More to come


### Available Commands

Future work


# Changelog

## v5.1
- Added Websocket support with ROS Bridge
- Available streams: `/motion/speed`, `/odometry/filtered`, `/gps_rover/fix`
- Add Serial commands: `@TDIR`

## v5.0
- Introduction of the SDK with Serial (RS232/TTL) support
- Available commands: `?STTN`,  `?SYSP`, `?TDIR`
