# raspbian-server
Raspbian-Python webserver that pulls in code from Waveshare for their Pan-Tilt Hat, does basic logging

## Operation
At startup of the RPi the server is started as a service 
The server starts UDP broadcasting the Pi's IP addr
mjpg-streamer is also set to auto start as service
https://github.com/jacksonliam/mjpg-streamer

Endpoints exposed 
/stop-broadcast

/control/{pan-left/pan-right/tilt-up/tilt-down}
/camera/focus
/camera/start
/camera/stop

## Planning
Control on Restful then eventually Websockets. but initially Restful


## Source Projects 
1. For the UDP broadcasting  https://github.com/ninedraft/python-udp

2. For the Linux Service  https://www.raspberrypi.org/documentation/linux/usage/systemd.md

3. Base site code & servo test https://github.com/waveshare/Pan-Tilt-HAT