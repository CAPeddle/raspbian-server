#!/usr/bin/python
# -*- coding:utf-8 -*-
from bottle import get,post,run,route,request,template,static_file
from PCA9685 import PCA9685
import threading
import os
import socket
import time

pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

#Set the Horizontal vertical servo parameters
HPulse = 1500  #Sets the initial Pulse
HStep = 0      #Sets the initial step length
VPulse = 1000  #Sets the initial Pulse
VStep = 0      #Sets the initial step length

HPulseTarget = HPulse
VPulseTarget = VPulse

MIN_HPULSE = 600
MAX_HPULSE = 1600
MIN_VPULSE = 500
MAX_VPULSE = 1200


start = int(time.time())

pwm.setServoPulse(1,HPulse)
pwm.setServoPulse(0,VPulse)

@get("/")
def index():
    return template("index")
    
@route('/<filename>')
def server_static(filename):
    return static_file(filename, root='./')

@route('/fonts/<filename>')
def server_fonts(filename):
    return static_file(filename, root='./fonts/')

@post("/cmd/panangle")
def setpanangle():
    global HPulseTarget, pwm
    body = request.body.read().decode()

    angle = int(body)
    if angle < 10 or angle > 100:
        return "INCORRECT ANGLE"
    else:
        HPulseTarget = pwm.getPulse(angle)
        print (HPulseTarget)
    return "OK"

@post("/cmd/tiltangle")
def settiltangle():
    global VPulseTarget, pwm
    body = request.body.read().decode()

    angle = int(body)
    if angle < 10 or angle > 100:
        return "INCORRECT ANGLE"
    else:
        VPulseTarget = pwm.getPulse(angle)
        print (VPulseTarget)
    return "OK"

@post("/cmd")
def cmd():
    global HStep,VStep,HPulse,VPulse
    code = request.body.read().decode()
    
    if code == "stop":
        HStep = 0.0
        VStep = 0.0
        print("stop")
    elif code == "up":
        VStep = -1
        print("up {}".format(VPulse))
    elif code == "down":
        VStep = 1
        print("down {}".format(VPulse))        
    elif code == "left":
        HStep = 1
        print("{} {}".format(code, HPulse))        
    elif code == "right":
        HStep = -1
        print("{} {}".format(code, HPulse))        
    return "OK"

def get_pulse(angle):    
    if(angle < 0  or  angle >180):
        print("Angle out of range \n")  
        return 45  * (2000 / 180) + 500  
    else:
        temp = angle * (2000 / 180) + 500
        return temp    

def camera():
    Road = 'home/pi/projects/mjpg-streamer/mjpg-streamer-experimental/'
    osCommand = './' + Road + 'mjpg_streamer -i "./' + Road + '/input_uvc.so" -o "./' + Road + 'output_http.so -w ./' + Road + 'www"'
    print (osCommand)
    os.system('./' + Road + 'mjpg_streamer -i "./' + Road + '/input_uvc.so" -o "./' + Road + 'output_http.so -w ./' + Road + 'www"') 
    # ./mjpg_streamer -i "./input_uvc.so" -o "./output_http.so -w ./www"
    
def timerfunc():
    global HPulse,VPulse,HStep,VStep,pwm,start,MAX_HPULSE, MIN_HPULSE, HPulseTarget, VPulseTarget, MAX_VPULSE, MIN_VPULSE
    
    if (HPulseTarget > HPulse and HPulseTarget != -1):
        HStep = 1
    elif (HPulseTarget < HPulse and HPulseTarget != -1):
        HStep = -1
    else:
        HPulseTarget = -1

    if (VPulseTarget > VPulse and VPulseTarget != -1):
        VStep = 1
    elif (VPulseTarget < VPulse and VPulseTarget != -1):
        VStep = -1
    else:
        VPulseTarget = -1

    if(HStep != 0):
        HPulse += HStep
        if(HPulse >= MAX_HPULSE): 
            HPulse = MAX_HPULSE
            HStep = 0
        if(HPulse <= MIN_HPULSE):
            HPulse = MIN_HPULSE
            HStep = 0
        if(HPulse != MAX_HPULSE and HPulse != MIN_HPULSE):
            print ("panning {}:{}".format(HStep,HPulse))
        #set channel 2, the Horizontal servo
        pwm.start_PCA9685()
        pwm.setServoPulse(1,HPulse)
        start = int(time.time())        


    if(VStep != 0):
        VPulse += VStep
        if(VPulse >= MAX_VPULSE): 
            VPulse = MAX_VPULSE
            VStep = 0
        if(VPulse <= MIN_VPULSE):
            VPulse = MIN_VPULSE
            VStep = 0
        if(VPulse != MAX_VPULSE and VPulse != MIN_VPULSE):
            print ("tilting {}:{}".format(VStep,VPulse))
        #set channel 3, the vertical servo
        # print ("tilting {}:{}".format(VStep,VPulse))
        pwm.start_PCA9685()
        pwm.setServoPulse(0,VPulse)   
        start = int(time.time())
        
    end = int(time.time())
    if((end - start) > 3):
        pwm.exit_PCA9685()
        start = int(time.time())

    
    # global t        #Notice: use global variable!
    # t = threading.Timer(0.02, timerfunc)
    # t.start()
    
try:      
    t = threading.Timer(0.02, timerfunc)
    t.setDaemon(True)
    t.start()


    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('192.168.0.115', 80))
    localhost = s.getsockname()[0]

    run(host=localhost, port="8001")
except KeyboardInterrupt:
    print ("KeyboardInterrupt")
    pwm.exit_PCA9685()
    print ("\nProgram end")
    exit()  
except:
    pwm.exit_PCA9685()
    print ("\nProgram end")
    exit()