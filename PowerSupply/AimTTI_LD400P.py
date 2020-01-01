#!python3
#!/usr/bin/python
#coding: utf-8

"""
Code to control an Aim TTi LD400P Programmable Power Supply

Control is based on SCPI.
https://en.wikipedia.org/wiki/Standard_Commands_for_Programmable_Instruments

"""

import serial
import time


###############################################################################
class LD400P(object):
    def __init__(self, COM):
        self.s = serial.Serial(COM, timeout=1)
        #self.close_port()
        self.open_port()

    def close_port(self):
        self.s.close()

    def open_port(self):
        try:
            self.s.open()
        except serial.serialutil.SerialException as e:
            print(e)

    def write(self, command):
        print("  {:>8s}: '{}'".format("WRITE", command))
        self.s.write("{}\n".format(command))

    def read(self, command):
        self.write(command)
        result = self.s.readline().strip("\n")
        print("  {:>8s}: '{}'".format("READ", result))

    def sleep(self, delay_in_s):
        increment = 0.1
        s = 0
        t = 0.0
        while s < int(delay_in_s):
            print("{: > 6d} secs{:11s}\r".format(s, "."*int((t/increment)-len(str(s)))), end="")
            time.sleep(increment)
            t += increment
            if int(t) == 1:
                s += 1
                t = 0.0
        print()


###############################################################################
if __name__ == '__main__':

    D = LD400P("COM3")
    D.write("FREQ 1000")
    D.write("MODE C")
    D.write("A 1")
    D.write("INP 1")
    D.sleep(5)
    D.write("A 2.5")
    D.read("FREQ?")
    D.read("*IDN?")
    D.write("INP 0")
