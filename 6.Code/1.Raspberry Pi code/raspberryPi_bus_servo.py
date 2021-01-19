# -*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time
import string
import serial


global ser

# Set GPIO port to BCM coding mode
GPIO.setmode(GPIO.BCM)

# Ignore the warning message
GPIO.setwarnings(False)


# Control the servo, index is the ID number of the servo, 
# value is the position of the servo, s_time is the running time of the servo
def Servo_control(index, value, s_time):
    pack1 = 0xff
    pack2 = 0xff
    id = index & 0xff
    len = 0x07
    cmd = 0x03
    addr = 0x2A
    pos1 = (value >> 8) & 0x00ff
    pos2 = value & 0x00ff
    time1 = (s_time >> 8) & 0x00ff
    time2 = s_time & 0x00ff
    checknum = (~(id + len + cmd + addr + pos1 + pos2 + time1 + time2)) & 0xff

    data = [pack1, pack2, id, len, cmd, addr,
            pos1, pos2, time1, time2, checknum]
    ser.write(bytes(data))


# Set servo ID
def Servo_Set_ID(index):
    if index < 1 or index > 250:
        return None

    pack1 = 0xff
    pack2 = 0xff
    id = 0xfe
    len = 0x04
    cmd = 0x03
    addr = 0x05
    set_id = index & 0xff

    checknum = (~(id + len + cmd + addr + set_id)) & 0xff

    data = [pack1, pack2, id, len, cmd, addr, set_id, checknum]
    ser.write(bytes(data))



try:
    ser = serial.Serial("/dev/ttyS0", 115200, timeout=0.001)
    print ("serial.isOpen()")
    index = 0x01
    Servo_Set_ID(index)
    time.sleep(.01)

    while True:
        Servo_control(index, 3100, 1000)
        time.sleep(2)
        Servo_control(index, 900, 1000)
        time.sleep(2)

except KeyboardInterrupt:
    pass
ser.close()
GPIO.cleanup()
