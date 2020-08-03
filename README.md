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

---
### Thoughts
- Control Camera
  - If available
  - Point and "click"
  - pan/tilt

- Temperature and Humidity logging
  - If available

- Log Anything
  - Delete anything
  - By UID ? names/labels only
    - The api shouldn't prescribe entries
  - Get Logged lists by query
    - When was last entry?
  - Database 
    - relational? 
      - data will be relational, eg temps listes

- Api Versions


- Remember last state
  - Cookies
  - Meaning upfront configurable detail

---

## Frontend Technology

React -> over Vue  because it's more like programming. well JS anyway
Vue is a lot like HTML, and I don't like HTML or CSS

React vs Bootstrap -> React can lead to React Native

## Python
Ensure the system wide default is Python 3

## Servo control
Using a MG996R [10] and CYS-3006 [11] servo and the pan tilt kit from DF Robot [9] using the adafruit PCA9685 breakout board. I have the CYS as the tilt servo, servo 0 on the board. 

tiltServo = kit.servo[0]
panServo = kit.servo[1]
tiltServo.set_pulse_width_range(500, 2500)
panServo.set_pulse_width_range(1000, 2000)

Important to note is that setting the panServo.actuation_range = 180 will actually limit the range as well as throw an exception if you try set it past that. I'm not sure but I presume that it then does a pulse width calc to convert the angle to the appropriate value. 

On the CYS servo I had the pwm range as 500 to 2500 but the servo would get a jitter, once checking the data sheet it's indicated as taking 1000 to 2000. Updating that -> no jitter. 

As installed on my gimble the ranges are
panmaxRange = 170
tiltmaxRange = 130


## Source Projects & Forums
1. For the UDP broadcasting  https://github.com/ninedraft/python-udp

2. For the Linux Service  https://www.raspberrypi.org/documentation/linux/usage/systemd.md

3. Base site code & servo test https://github.com/waveshare/Pan-Tilt-HAT

4. Disable ACT LED https://www.raspberrypi.org/forums/viewtopic.php?t=149126

5. Audio  https://snowboy.kitt.ai/docs
arecord --device=hw:1,0 --format S16_LE --duration=10 --rate 44100 -c1 test.wav
Run alsamixer to adjust gain

6. New PWM https://cdn-learn.adafruit.com/downloads/pdf/adafruit-16-channel-servo-driver-with-raspberry-pi.pdf

7. Handy Pin Mappings https://docs.microsoft.com/en-us/windows/iot-core/learn-about-hardware/pinmappings/pinmappingsrpi

8. Additional mappings https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial/all

9. Final Gimble https://www.dfrobot.com/product-146.html

10. https://www.towerpro.com.tw/product/mg996r/

11. # https://www.cysmodel.com/products/cys-s3006-6kg-analog-plastic-gear-servo-standard-size/

