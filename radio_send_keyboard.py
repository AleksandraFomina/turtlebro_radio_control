#!/usr/bin/env python

import serial

import sys
from select import select

if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty


msg = """
Reading from the keyboard  and Publishing to Twist!
---------------------------
Moving around:
        w    
   a    s    d
   
anything else : stop

q/z : increase/decrease max speeds by 10%
u/j : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%

CTRL-C to quit
"""


def getKey(settings, timeout):
    if sys.platform == 'win32':
        # getwch() returns a string on Windows
        key = msvcrt.getwch()
    else:
        tty.setraw(sys.stdin.fileno())
        # sys.stdin.read() returns a string on Linux
        rlist, _, _ = select([sys.stdin], [], [], timeout)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def saveTerminalSettings():
    if sys.platform == 'win32':
        return None
    return termios.tcgetattr(sys.stdin)

def restoreTerminalSettings(old_settings):
    if sys.platform == 'win32':
        return
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


if __name__=="__main__":
    settings = saveTerminalSettings()
    key_timeout = 0.5

    ser = serial.Serial()
    ser.baudrate = 19200
    ser.port = "/dev/ttyUSB0"
    ser.dtr = False
    ser.timeout = 0.5
    ser.open()

    ser.flushInput()
    print (msg)
    try:
        while(1):
            key = getKey(settings, key_timeout)
            if key == '\x03': 
                ser.write(key.encode())
                break
            ser.write(key.encode())

    except Exception as e:
        print(e)

    finally:
        restoreTerminalSettings(settings)
