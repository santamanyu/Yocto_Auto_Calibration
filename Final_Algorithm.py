'''
Some limitations with the sensor
1.if(offset > single_bulb_Lux)   ---------> gives negative value
2.Sensor must be placed at equidistant from all the lamps.
    exceptional case:- if we are getting more then number of light for a site,we can ignore
    if sensor is pointed perpendicular towards a light sourse,it will give highest value.(as per fig4,fig5 of datasheet)
3.All car walls must be of equal type(colour and texture).
4.reading should be taken during standby.(no load, door closed state)
5.Sensor and high reflective surface need to cleaned time to time.
6.If sensor placed on the top, after calibration make sure no object like chair or black surface present on the floor. 

'''
from typing import Any

import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

from PIL import Image
import matplotlib.gridspec as gridspec

import os, sys

sys.path.append(os.path.join("C:\\Users\\k64067997\\AppData\\Local\\Programs\\Python\\Python38-32\\Lib\\site-packages\\yoctopuce"))
from yocto_api import *
from yocto_lightsensor import *


ImageAddress = 'C:\\Users\\k64067997\\Desktop\\Job Study\\Python Learning\\beauty.png'
ImageItself = Image.open(ImageAddress)

xs = []
ys = []
ys1 = []#1st cutoff
ys2 = []#2nd cutoff
ys3 = []#3rd cuoff
ys4 = []#4th cutoff

index = 0
no_of_lights = 0
single_bulb_Lux = 0
offset = 0
prev_img_printed = 0

#################### YOCTO SENSOR
errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

def fetch_sensor_data():
    global offset
    SValue = 0

    # retreive any Light sensor
    sensor = YLightSensor.FirstLightSensor()
    if sensor is None:
        print('No module connected')
    if sensor.isOnline():
        i = 0
        while (i < 1000):
            SValue = SValue + int(sensor.get_currentValue())
            i += 1
    SValue /= 1000  # average of 1000 sample
    SValue = SValue - offset
    return SValue

# for plotting the graph
def animate(i):
    global xs
    global ys
    global index
    global no_of_lights
    global offset
    global single_bulb_Lux
    global prev_img_printed
    index = index + 1
    SValue = fetch_sensor_data()

    no_of_lights = SValue / single_bulb_Lux
    Deviation = no_of_lights - int(no_of_lights)

    if(Deviation > (.6)):                       #60% MORE LIGHT lux w.r.t calculated number of light present
        no_of_lights = int(no_of_lights) + 1
        print("no of light is:-",no_of_lights)
    elif(Deviation >= 0):                       #lux is bit higher for actual number of light present
        no_of_lights = int(no_of_lights)
        if(no_of_lights > 0):
            print("no of light is:-",no_of_lights)
    
    if (SValue < offset):                       #this will only work if we calibrate with ambient lights
        no_of_lights = 0
        print("                     All lights OFF")
        if(SValue == -offset):
            print("                                   Ambient light Absent")    

    #plottong
    xs.append(index)
    ys.append(float(SValue))
    ys1.append(single_bulb_Lux)
    ys2.append(2*single_bulb_Lux)
    ys3.append(3*single_bulb_Lux)
    ys4.append(4*single_bulb_Lux)
    
    ax.clear()
    ax.plot(xs, ys1,xs, ys2,xs, ys3,xs, ys4,color='red', linewidth=0.5)
    ax.plot(xs, ys, color='blue', linewidth=0.5)
    
    if(no_of_lights == 1 and prev_img_printed != 1 ):
        prev_img_printed = 1
        ax1.imshow(ImageItself)
        ax2.clear()
        ax3.clear()
        ax4.clear()
    elif(no_of_lights == 2 and prev_img_printed != 2):
        prev_img_printed = 2
        ax1.imshow(ImageItself)
        ax2.imshow(ImageItself)
        ax3.clear()
        ax4.clear()
    elif(no_of_lights == 3 and prev_img_printed != 3):
        prev_img_printed = 3
        ax1.imshow(ImageItself)
        ax2.imshow(ImageItself)
        ax3.imshow(ImageItself)
        ax4.clear()
    elif(no_of_lights == 4 and prev_img_printed != 4):
        prev_img_printed = 4
        ax1.imshow(ImageItself)
        ax2.imshow(ImageItself)
        ax3.imshow(ImageItself)
        ax4.imshow(ImageItself)

    elif (no_of_lights == 0 and prev_img_printed != 0):
        prev_img_printed = 0
        ax1.clear()
        ax2.clear()
        ax3.clear()
        ax4.clear()
    


print("ONE TIME CALIBRATION")
Choice = input("Set ambient light.Switch OFF all light. Enter Y/N to proceed/skip")
if(Choice == 'y' or Choice == 'Y'):
    offset = fetch_sensor_data()
else:
    offset = 0
print("offset value is:-",offset)

no_of_lights1 = input("Switch on the light, Please enter the number of lights present")
single_bulb_Lux = fetch_sensor_data() / int(no_of_lights1)
print("single_bulb_Lux is:-", single_bulb_Lux)
time.sleep(1)
             
# plotting
fig = plt.figure(tight_layout=True)
gs = gridspec.GridSpec(4,2,figure=fig)

ax = fig.add_subplot(gs[0:, 0])
plt.xlabel('Time(Second)', fontsize=15)
plt.ylabel('Lux', fontsize=15)
ax1 = fig.add_subplot(gs[3, 1])
ax2 = fig.add_subplot(gs[2, 1])
ax3 = fig.add_subplot(gs[1, 1])
ax4 = fig.add_subplot(gs[0, 1])

ani = animation.FuncAnimation(fig, animate, interval=200)  # plottong graph
plt.show()

print("This printed only during exit")
YAPI.FreeAPI()
