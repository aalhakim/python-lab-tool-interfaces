#!python3
#!/usr/bin/python
# coding: utf-8

"""
Programmatic control of the Tenma 72-13210 Electronic Load

Control is based on SCPI.
https://en.wikipedia.org/wiki/Standard_Commands_for_Programmable_Instruments

"""

# Standard Library Imports
import time

# Third-Party Library Imports
import serial


########################################################################
DEVICE_PORT = "COM6"

def bEncode(utf8):
    return utf8.encode("utf-8")


########################################################################
class TPL7213210(object):
    def __init__(self, com):
        self.ser = serial.Serial(com, timeout=1)
        #self.close_port()
        self.open_port()

    def close_port(self):
        self.ser.close()

    def open_port(self):
        try:
            self.ser.open()
        except serial.serialutil.SerialException as e:
            print(e)

    def write(self, command):
        print("  {:>8s}: '{}'".format("WRITE", command))
        self.ser.write("{}\n".format(command).encode("utf-8)"))

    def read(self, command):
        self.write(command)
        result = self.ser.readline().strip(bEncode("\n"))
        print("  {:>8s}: '{}'".format("READ", result))

    def idn(self):
        """ Return device information. """
        self.read("*IDN?")

    def battery_mode(self, ichg, iload, vcutoff, qcutoff, tends):
        """ Create a battery test mode in location 1
        """
        self.write(":BATT 1, {}A, {}A, {}V, {}AH, {}S".format(ichg, iload, vcutoff, qcutoff, tends))

    #-------------------------------------------------------------------
    def voltage(self):
        """ Return voltage measurement. """
        self.read(":MEAS:VOLT?")

    def current(self):
        """ Return current measurement. """
        self.read(":MEAS:CURR?")

    def power(self):
        """ Return power measurement. """
        self.read(":MEAS:POW?")

    # def resistance(self):
    #     """ Return resistance measurement. """
    #     self.read(":MEAS:RES?")

    #-------------------------------------------------------------------
    def set_voltage(self, value):
        """ Change to constant voltage (CV) and set threshold. """
        self.write(":VOLT {}V".format(value))

    def set_current(self, value):
        """ Change to constant current (CC) and set threshold. """
        self.write(":CURR {}A".format(value))

    def set_power(self, value):
        """ Change to constant power (CW) and set threshold. """
        self.write(":POW {}W".format(value))

    def set_resistance(self, value):
        """ Change to constant resistance (CR) and set threshold. """
        self.write(":RES {}OHM".format(value))

    def set_mode(self, mode):
        """ Set the mode to CV, CC, CW or CR.

        Parameters
        ----------
        mode <str>: Select the operating mode.
            CV: constant voltage
            CC: constant current
            CW: constant power
            CR: constant resistance
            SHORt: short circuit

         """
        self.write(":FUNC {}".format(mode))

    def get_mode(self):
        """ Get current system mode. """
        self.read(":FUNC?")

    #-------------------------------------------------------------------
    def get_setVoltage(self):
        """ Return voltage setting value. """
        self.read(":VOLT?")

    def get_setCurrent(self):
        """ Return current setting value measurement. """
        self.read(":CURR?")

    def get_setPower(self):
        """ Return power setting value. """
        self.read(":POW?")

    def get_setResistance(self):
        """ Return resistance setting value. """
        self.read(":RES?")

    #-------------------------------------------------------------------
    def enable(self):
        """ Enable device. """
        self.write(":INP 1")

    def disable(self):
        """ Enable device. """
        self.write(":INP 0")

    def get_input_status(self):
        """ Check output status. """
        self.read(":INP?")

    #-------------------------------------------------------------------
    def beep_on(self):
        """ Turn the system beep on when buttons are pressed. """
        self.write(":SYST:BEEP ON")

    def beep_off(self):
        """ Turn the system beep off when buttons are pressed. """
        self.write(":SYST:BEEP OFF")

    def get_beep_status(self):
        """ Check if the beep is ON or OFF. """
        self.read(":SYST:BEEP?")

    def get_baud_status(self):
        """ Check what the current baud rate is set to. """
        self.read(":SYST:BAUD?")

    #-------------------------------------------------------------------
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
        print("\n")


########################################################################
if __name__ == '__main__':

    d = TPL7213210(DEVICE_PORT)
    d.idn()
    d.voltage()
    d.current()
    d.power()

    # d.set_voltage(12.4)
    # d.get_setVoltage()
    # d.sleep(1)
    # d.set_current(2.8)
    # d.get_setCurrent()
    # d.sleep(1)
    # d.set_power(54)
    # d.get_setPower()
    # d.sleep(1)
    # d.set_resistance(5)
    # d.get_setResistance()
    # d.sleep(1)

    # d.enable()
    # # d.disable()

    d.set_mode("SHORt")
    d.get_mode()

    # # Not Working
    # d.battery_mode(5, 5, 12, 11, 60)
