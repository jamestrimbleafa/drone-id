# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2017 James DeVito for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!

import time
import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

from dataclasses import dataclass

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)

#from socket import *
#import struct
#PORT = 14551
#mavsocket = socket(AF_INET, SOCK_DGRAM)
#mavsocket.bind(("127.0.0.1", PORT))
#mavsocket.setblocking(False)

#@dataclass
#class MavPacket:
#    stx: int
#    length: int
#    seq: int
#    sys_id: int
#    comp_id: int
#    msg_id: int
#    payload: bytes
#    crc: int
#    
#    @classmethod
#    def parse(cls, data: bytes):
#        stx, length, seq, sys_id, comp_id, msg_id = struct.unpack("@BBBBBB", data[:6])
#        payload = data[6:length+6]
#        crc=struct.unpack("@H", data[length+6:length+8])[0]
#        return cls(stx, length, seq, sys_id, comp_id, msg_id, payload, crc)
 

from pymavlink import mavutil
conn = mavutil.mavlink_connection('udpin:localhost:14551')


while True:
    if False:
        try:
            data, addr = mavsocket.recvfrom(1024)
        except:
            pass
        else:
            packet = MavPacket.parse(data)
            if packet.msg_id != 1:
                print(packet)
            if packet.msg_id == 253 or b"PreArm" in packet.payload:
                print(f"LOG: {packet.payload.decode()}")
                draw.rectangle((0, 0, width, height), outline=0, fill=0)
        
    resp = conn.recv_match(blocking=False)
    
    print(resp)
        
    if False:
        tlen = 20
        s = packet.payload.decode()
        draw.text((x, top + 0), s[:min(tlen,len(s))], font=font, fill=255)
        draw.text((x, top + 8), s[min(tlen,len(s)-1):min(2*tlen,len(s))], font=font, fill=255)
        draw.text((x, top + 16), s[min(2*tlen,len(s)-1):min(3*tlen,len(s))], font=font, fill=255)
        draw.text((x, top + 25), s[min(3*tlen,len(s)-1):], font=font, fill=255)
        disp.image(image)
        disp.show()

    # Draw a black filled box to clear the image.

    # Shell scripts for system monitoring from here:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d' ' -f1"
    IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = 'cut -f 1 -d " " /proc/loadavg'
    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "./drone-id --value"
    DroneID = subprocess.check_output(cmd, shell=True).decode("utf-8")

    # Write four lines of text.

    #draw.text((x, top + 0), "IP: " + IP, font=font, fill=255)
    #draw.text((x, top + 8), "CPU load: " + CPU, font=font, fill=255)
    #draw.text((x, top + 16), MemUsage, font=font, fill=255)
    #draw.text((x, top + 25), "Drone ID: " + DroneID, font=font, fill=255)

    # Display image.
    #time.sleep(0.1)
