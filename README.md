# raspbian-server
Raspbian-Python webserver that pulls in code from Waveshare for their Pan-Tilt Hat, does basic logging

## Operation
At startup of the RPi the server is started as a service 
The server starts UDP broadcasting the Pi's IP addr
mjpg-streamer is also set to auto start as service
https://github.com/jacksonliam/mjpg-streamer

## Endpoints exposed 

/cmd
body -> {left/right/up/down}
These start a continuous movement until max

/cmd/panangle/
body -> <angle>
Sets the pan angle to move to

/cmd/tiltangle/
body -> <angle>
Sets the tilt angle to move to

/stopbroadcast
Stops the UDP Broadcast thread

/camera/focus
/camera/start
/camera/stop

## Planning
Control on Restful then eventually Websockets. but initially Restful

## Frontend Technology

React -> over Vue  because it's more like programming. well JS anyway
Vue is a lot like HTML, and I don't like HTML or CSS

React vs Bootsrap -> React can lead to React Native


## Source Projects & Forums
1. For the UDP broadcasting  https://github.com/ninedraft/python-udp

2. For the Linux Service  https://www.raspberrypi.org/documentation/linux/usage/systemd.md

3. Base site code & servo test https://github.com/waveshare/Pan-Tilt-HAT

4. Disable ACT LED https://www.raspberrypi.org/forums/viewtopic.php?t=149126


