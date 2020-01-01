#!python3
#!/usr/bin/python

"""
Example code using:
 + Elecktro-Automatik PS 2042-20B Programmable Power Supply [FOR REVIEW]
 + Tenma 72-13210 Programmable Load [INCOMPLETE]

"""

# Standard Library Imports
import os
import sys
import time
import serial

# Third Party Library Imports


# Local Library Imports
from PowerSupply import ElectroAutomatik_PS2000B
from ElectronicLoad import Tenma_7213210

########################################################################
if os.name == "nt":
    PLATFORM = "windows"
elif os.name == "unix":
    PLATFORM = "pi"


########################################################################
# COM port used by PS 2000 B system on Windows
WINDOWS_COM = "COM5"

# Define how to connect to the Power Supply
SUPPLY = WINDOWS_COM if PLATFORM == "windows" else "/dev/ttyACM0"


########################################################################

class PowerSupply(object):
    """
    Abstraction class to EA-PS 2042-20B
    """

    def __init__(self, device):
        print("Connecting to device at {}...".format(device), end=" ")
        self.supply = ElectroAutomatik_PS2000B.PS2000B(device)

        if self.supply.is_open() is True:
            print("success")

            ps_info = self.supply.get_device_information()
            ps_mfg   = ps_info.manufacturer.decode("utf-8")
            ps_type = ps_info.device_type.decode("utf-8")
            ps_sn  = ps_info.device_serial_no.decode("utf-8")
            print("  - Connected to {} {} ({})".format(ps_mfg, ps_type, ps_sn))

        else:
            print("failure")

    def _remote_control(command):
        def send_command(self):
            self.supply.enable_remote_control()
            command(self)
            self.supply.disable_remote_control()
        return send_command


    def set_voltage(self, voltage):
        """ Set the voltage level."""

        self.supply.enable_remote_control()
        self.supply.set_voltage(voltage)
        self.supply.disable_remote_control()

    def set_current(self, current):
        """ Set the voltage level."""

        self.supply.enable_remote_control()
        self.supply.set_current(current)
        self.supply.disable_remote_control()

    def get_voltage(self):
        """ Get the present voltage level."""
        return(self.supply.get_voltage())

    def get_current(self):
        """ Get the present current level."""
        return(self.supply.get_current())

    @_remote_control
    def enable(self):
        """Enable the output."""
        self.supply.enable_output()

    @_remote_control
    def disable(self):
        """ Disable the output."""
        self.supply.disable_output()


########################################################################
if __name__ == "__main__":

    # Connect to Power Supply
    supply = PowerSupply(SUPPLY)

    supply.enable()
    supply.set_voltage(30.00)
    supply.set_current(5.00)
    time.sleep(10)
    supply.disable()
