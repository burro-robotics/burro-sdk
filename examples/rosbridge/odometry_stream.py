#!/usr/bin/env python
import roslibpy

# Example script that uses the roslibpy API to stream Burro's odometry
# and print out the x and y position of its local coordinate frame

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
