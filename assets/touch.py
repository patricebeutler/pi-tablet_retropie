#!/usr/bin/python3

import struct
import os
import time
import math
import signal
import glob
import sys
from ft5406 import Touchscreen, TS_PRESS, TS_RELEASE, TS_MOVE
from math import floor
from subprocess import call
from subprocess import check_output
import subprocess as SP
from rpi_backlight import Backlight

screenState = "/home/pi/pi-tablet_retropie/assets/currentDisplayMode"
PNGVIEWPATH = "/home/pi/pi-tablet_retropie/assets/pngview/"
ICONPATH = "/home/pi/pi-tablet_retropie/assets/icons"
brightLast = ""
volumeLast = ""
layerList = []
backlight = Backlight()

def read_and_emulate_mouse(event, touch):
    global startX
    global startY
    global startTime
    global shouldRun
    global brightLast
    global volumeLast
    global killid
    global layerList
    if event == TS_RELEASE:
        os.system("sudo kill " + "$(ps aux | grep '[p]ngview' | awk '{print $2}')")
        layerList = []
    if event == TS_PRESS:
        (startX, startY) = touch.position
        startTime = time.time()

    (x, y) = touch.position
    (last_x, last_y) = touch.last_position

    movement = math.sqrt(pow(x - startX, 2) + pow(y - startY, 2))
	
    # top left: brightness
    if startX < 244 and startY < 140 and x <= 244:
        backlight.brightness = (x + 11) / 2.56
        brightnessValue = x + 11
		
        brightnessPng = ""
		
        if brightnessValue >= 5 and brightnessValue < 29:
            brightnessPng = "10"
        elif brightnessValue >= 30 and brightnessValue < 54:
            brightnessPng = "20"
        elif brightnessValue >= 55 and brightnessValue < 79:
            brightnessPng = "30"
        elif brightnessValue >= 80 and brightnessValue < 104:
            brightnessPng = "40"
        elif brightnessValue >= 105 and brightnessValue < 129:
            brightnessPng = "50"
        elif brightnessValue >= 130 and brightnessValue < 154:
            brightnessPng = "60"
        elif brightnessValue >= 155 and brightnessValue < 179:
            brightnessPng = "70"
        elif brightnessValue >= 180 and brightnessValue < 204:
            brightnessPng = "80"        
        elif brightnessValue >= 205 and brightnessValue < 230:
            brightnessPng = "90"
        elif brightnessValue >= 231:
            brightnessPng = "100"
			
        if brightLast != brightnessPng and brightnessPng != "":
            brightLast = brightnessPng
            if len(layerList) == 0:
                os.system("/home/pi/pi-tablet_retropie/assets/pngview" + "/pngview -b 0 -l 3000" + "1" + " -x 260 -y 150 " + "/home/pi/pi-tablet_retropie/assets/icons/brightness/" + "bar" + ".png &")			
            os.system("/home/pi/pi-tablet_retropie/assets/pngview" + "/pngview -b 0 -l 3000" + brightnessPng + " -x 260 -y 150 " + "/home/pi/pi-tablet_retropie/assets/icons/brightness/" + brightnessPng + ".png &")
            killBrightnessID = check_output("ps aux | grep '[p]ngview' | awk '{print $2}'", shell=True)
            killBrightnessID = killBrightnessID.decode("utf-8")
            killBrightnessID = killBrightnessID.replace("\n", " ")
            killBrightnessID = killBrightnessID.split(" ")
            for layer in killBrightnessID:
                if layer != "" and layer not in layerList:
                    layerList.append(layer)
            if len(layerList) == 3:
                killThisBrightnessID = str(layerList[1])
                os.system("sudo kill " + killThisBrightnessID)
                layerList.remove(layerList[1])
				
    # bottom left: volume
    if startX < 244 and startY > 340 and x <= 244:
        call(["amixer", "cset", "numid=1", "--", str(floor(x/2.44)) + '%'])
		
        volumeValue = floor(x/2.44);
        volumePng = "";
		
		
        if volumeValue >= 0 and volumeValue < 10:
            volumePng = "10"
        elif volumeValue >= 10 and volumeValue < 20:
            volumePng = "20"
        elif volumeValue >= 20 and volumeValue < 30:
            volumePng = "30"
        elif volumeValue >= 30 and volumeValue < 40:
            volumePng = "40"
        elif volumeValue >= 40 and volumeValue < 50:
            volumePng = "50"
        elif volumeValue >= 50 and volumeValue < 60:
            volumePng = "60"
        elif volumeValue >= 60 and volumeValue < 70:
            volumePng = "70"
        elif volumeValue >= 70 and volumeValue < 80:
            volumePng = "80"        
        elif volumeValue >= 80 and volumeValue < 90:
            volumePng = "90"
        elif volumeValue >= 90:
            volumePng = "100"
			
        if volumeLast != volumePng and volumePng != "":
            volumeLast = volumePng
            if len(layerList) == 0:
                os.system("/home/pi/pi-tablet_retropie/assets/pngview" + "/pngview -b 0 -l 3000" + "1" + " -x 260 -y 150 " + "/home/pi/pi-tablet_retropie/assets/icons/volume/" + "bar" + ".png &")			
            os.system("/home/pi/pi-tablet_retropie/assets/pngview" + "/pngview -b 0 -l 3000" + volumePng + " -x 260 -y 150 " + "/home/pi/pi-tablet_retropie/assets/icons/volume/" + volumePng + ".png &")
            killVolumeID = check_output("ps aux | grep '[p]ngview' | awk '{print $2}'", shell=True)
            killVolumeID = killVolumeID.decode("utf-8")
            killVolumeID = killVolumeID.replace("\n", " ")
            killVolumeID = killVolumeID.split(" ")
            for layer in killVolumeID:
                if layer != "" and layer not in layerList:
                    layerList.append(layer)
            if len(layerList) == 3:
                killThisVolumeID = str(layerList[1])
                os.system("sudo kill " + killThisVolumeID)
                layerList.remove(layerList[1])
    
    #bottom right: switch Displaymode
    if startX > 556 and startY > 340:
        if movement < 20 and event == TS_RELEASE and (time.time() - startTime) >= 2:
            stateFile = open(screenState, 'r')
            state = stateFile.readline()
            state = str(state)
            stateFile.close()
            if (state == "lcd"):
                SP.call('echo "hdmi" > /home/pi/pi-tablet_retropie/assets/currentDisplayMode', shell=True)
                SP.call(['sudo','/home/pi/pi-tablet_retropie/assets/hdmi_out'])
            else :
                SP.call('echo "lcd" > /home/pi/pi-tablet_retropie/assets/currentDisplayMode', shell=True)
                SP.call(['sudo','/home/pi/pi-tablet_retropie/assets/lcd_out'])


if __name__ == "__main__":
    global shouldRun
    shouldRun = True
    ts = Touchscreen()

    for touch in ts.touches:
        touch.on_press = read_and_emulate_mouse
        touch.on_release = read_and_emulate_mouse
        touch.on_move = read_and_emulate_mouse

    ts.run()

    while shouldRun:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            ts.stop()
            exit()

    ts.stop()
    exit()
