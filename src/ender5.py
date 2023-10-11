try:
    import serial
except ImportError:
    print("Could not import module: serial")

# from sciopy import available_serial_ports,connect_COM_port
import time

from classes import Ender5Stat


def command(ser, command) -> None:
    """Write a command to the serial connection.

    Parameters
    ----------
    ser : _type_
        serial connection
    command : _type_
        command string
    """
    ser.write(str.encode(command))
    time.sleep(1)
    while True:
        line = ser.readline()
        print(line)

        if line == b"ok\n":
            break


def move_to_absolute_x(ser, enderstat: Ender5Stat) -> None:
    """
    enderstat.abs_x_tgt : absolute x position
    enderstat.motion_speed : movement speed in [mm/min]
    """
    command(ser, f"G0 X{enderstat.abs_x_tgt} F{enderstat.motion_speed}\r\n")
    print(enderstat)


def move_to_absolute_y(ser, enderstat: Ender5Stat) -> None:
    """
    enderstat.abs_x_tgt : absolute x position
    enderstat.motion_speed : movement speed in [mm/min]
    """
    command(ser, f"G0 Y{enderstat.abs_y_tgt} F{enderstat.motion_speed}\r\n")
    print(enderstat)


def move_to_absolute_z(ser, enderstat: Ender5Stat) -> None:
    """
    enderstat.abs_x_tgt : absolute x position
    enderstat.motion_speed : movement speed in [mm/min]
    """
    command(ser, f"G0 Z{enderstat.abs_z_tgt} F{enderstat.motion_speed}\r\n")
    print(enderstat)


def move_to_absolute_x_y(ser, enderstat: Ender5Stat) -> None:
    """
    enderstat.abs_x_tgt : absolute x position
    enderstat.abs_y_tgt : absolute y position
    enderstat.motion_speed : movement speed in [mm/min]
    """
    command(
        ser,
        f"G0 X{enderstat.abs_x_tgt} Y{enderstat.abs_y_tgt} F{enderstat.motion_speed}\r\n",
    )
    print(enderstat)


def disable_steppers(ser) -> None:
    """disable the steppers

    Parameters
    ----------
    ser : _type_
        serial connection
    """
    command(ser, "M18 X Y Z E\r\n")


def enable_steppers(ser) -> None:
    """Enable steppers

    Parameters
    ----------
    ser : _type_
        serial connection
    """
    command(ser, "M17 X Y Z E\r\n")


def x_y_home(ser, enderstat: Ender5Stat) -> None:
    """Move to home position

    Parameters
    ----------
    ser : _type_
        serial connection
    enderstat : Ender5Stat
        ender 5 status dataclass
    """
    command(ser, f"G28 X0 Y0 F{enderstat.motion_speed}\r\n")
    command(ser, f"G28 Z0 F{enderstat.motion_speed}\r\n")
    print(enderstat)


def x_y_center(ser, enderstat: Ender5Stat) -> None:
    """Move to x,y center position

    Parameters
    ----------
    ser : _type_
        serial connection
    enderstat : Ender5Stat
        ender 5 status dataclass
    """
    command(ser, f"G0 X180 Y180 F{enderstat.motion_speed}\r\n")
    print(enderstat)


def turn_off_fan(ser) -> None:
    """Turn off the cooling fans.

    Parameters
    ----------
    ser : _type_
        serial connection
    """
    command(ser, "M106 S0\r\n")


def init_axis(ser) -> None:
    """Initialise the axis

    Parameters
    ----------
    ser : _type_
        serial connection
    """
    x_y_home(ser)
    x_y_center(ser)
    turn_off_fan(ser)
    print("X,Y axis are centered at X(180), Y(180)")


def read_temperature(ser) -> float:  # TB-checked
    """
    Read the bed temperature of the Ender 5

    Parameters
    ----------
    ser : _type_
        serial connection

    Returns
    -------
    float
        temperature value
    """
    ser.write(str.encode(f"M105\r\n"))
    time.sleep(1)
    line = ser.readline()
    temp = float(str(line).split("B:")[1].split(" ")[0])
    return temp
