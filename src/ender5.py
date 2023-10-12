try:
    import serial
except ImportError:
    print("Could not import module: serial")

import time
import numpy as np
from .classes import Ender5Stat


def command(
    ser: serial.serialwin32.Serial, command: str, print_msg: bool = True
) -> None:
    """
    Write a command to the serial connection.

    Parameters
    ----------
    ser : serial.serialwin32.Serial
        serial connection
    command : str
        GCODE command
    print_msg : bool, optional
        print log, by default True
    """
    ser.write(str.encode(command))
    time.sleep(1)
    while True:
        line = ser.readline()
        if print_msg:
            print(line)

        if line == b"ok\n":
            break


def init_ender5(
    ser: serial.serialwin32.Serial, enderstat: Ender5Stat, print_msg: bool = False
):
    """
    Initialize the Ender 5

    Parameters
    ----------
    ser : serial.serialwin32.Serial
        serial connection
    enderstat : Ender5Stat
        ender 5 dataclass
    print_msg : bool, optional
        print log, by default False
    """
    command(ser, f"G28 X0 Y0 F{enderstat.motion_speed}\r\n", print_msg=print_msg)
    command(ser, f"G28 Z0 F{enderstat.motion_speed}\r\n", print_msg=print_msg)
    enderstat.abs_x_pos = 180
    enderstat.abs_y_pos = 180
    enderstat.abs_z_pos = 0
    if print_msg:
        print(enderstat)


def x_y_center(
    ser: serial.serialwin32.Serial, enderstat: Ender5Stat, print_msg: bool = False
):
    """
    Move x,y axis to center position.

    Parameters
    ----------
    ser : serial.serialwin32.Serial
        serial connection
    enderstat : Ender5Stat
        ender 5 dataclass
    print_msg : bool, optional
        print log, by default False
    """
    command(ser, f"G0 X180 Y180 F{enderstat.motion_speed}\r\n")
    enderstat.abs_x_pos = 180
    enderstat.abs_y_pos = 180
    if print_msg:
        print(enderstat)


def turn_off_fan(ser) -> None:
    """Turn off the cooling fans.

    Parameters
    ----------
    ser : serial
        serial connection
    """
    command(ser, "M106 S0\r\n")


def read_temperature(ser: serial.serialwin32.Serial) -> float:
    """
    Read the bed temperature of the Ender 5

    Parameters
    ----------
    ser : serial.serialwin32.Serial
        serial connection

    Returns
    -------
    float
        temperature [°C]
    """
    ser.write(str.encode(f"M105\r\n"))
    time.sleep(1)
    line = ser.readline()
    temp = float(str(line).split("B:")[1].split(" ")[0])
    return temp


def move_to_absolute_x_y_z(
    ser: serial.serialwin32.Serial, enderstat: Ender5Stat, print_msg: bool = False
) -> None:
    """
    Move to given x,y,z coordinates.

    Parameters
    ----------
    ser : serial.serialwin32.Serial
        serial connection
    enderstat : Ender5Stat
        ender 5 dataclass
    print_msg : bool, optional
        print log, by default False
    """
    command(
        ser,
        f"G0 X{enderstat.abs_x_pos} Y{enderstat.abs_y_pos} Z{enderstat.abs_z_pos} F{enderstat.motion_speed}\r\n",
    )
    if print_msg:
        print(enderstat)


def move_ender_to_coordinate(
    ser: serial.serialwin32.Serial,
    coordinate: np.ndarray,
    enderstat: Ender5Stat,
    print_msg: bool = False,
) -> None:
    """
    Move to the P(x,y,z) position of a np.array([x,y,z]).

    Parameters
    ----------
    ser : serial.serialwin32.Serial
        serial connection
    coordinate : np.ndarray
        array with [x,y,z] coordinate
    enderstat : Ender5Stat
        ender 5 dataclass
    print_msg : bool, optional
        print log, by default False
    """
    x_y_offset = 180  # x,y center point
    y_ender, x_ender, z_ender = coordinate  # switch x,y for ender koordinate system

    enderstat.abs_x_pos = x_y_offset + x_ender
    enderstat.abs_y_pos = x_y_offset + y_ender
    enderstat.abs_z_pos = z_ender
    move_to_absolute_x_y_z(ser, enderstat, print_msg)
    if print_msg:
        print(enderstat)
