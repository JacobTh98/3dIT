from dataclasses import dataclass
from typing import Union


@dataclass
class TankProperties32x2:
    """
    T      := tank [mm]
    T_d    := tank diameter [mm]
    T_r    := tank radius [mm]
    T_bx   := tank x-axis boarder [mm]
    T_by   := tank y-axis boarder [mm]
    T_bz   := tank z-axis boarder [mm]
    E_zr1  := electrode ring 1 z-height [mm]
    E_zr2  := electrode ring 2 z-height [mm]
    n_el   := total number of electrodes [mm]
    """

    T_d: int = 194
    T_r: int = 97
    T_bx: tuple = (-T_d / 2, T_d / 2)
    T_by: tuple = (-T_d / 2, T_d / 2)
    T_bz: tuple = (0, 148)
    E_zr1: int = 50
    E_zr2: int = 100
    n_el: int = 64


@dataclass
class BallObjectProperties:
    """
    x        := absolute x-position [mm]
    y        := absolute y-position [mm]
    z        := absolute z-position [mm]
    r        := ball radius [mm]
    material := object material [mm]
    """

    x: Union[int, float]
    y: Union[int, float]
    z: Union[int, float]
    r: Union[int, float]
    material: str


@dataclass
class HitBox:
    """
    r_min := absolute object r min [mm]
    r_max := absolute object r max [mm]
    x_min := absolute object x min [mm]
    x_max := absolute object x max [mm]
    y_min := absolute object y min [mm]
    y_max := absolute object y max [mm]
    z_min := absolute object z min [mm]
    z_max := absolute object z max [mm]
    """

    r_min: Union[int, float]
    r_max: Union[int, float]
    x_min: Union[int, float]
    x_max: Union[int, float]
    y_min: Union[int, float]
    y_max: Union[int, float]
    z_min: Union[int, float]
    z_max: Union[int, float]


@dataclass
class OperatingSystem:
    system: str
    resolution_width: int
    resolution_height: int


@dataclass
class Ender5Stat:
    abs_x_pos: Union[int, float]
    abs_y_pos: Union[int, float]
    abs_z_pos: Union[int, float]
    tank_architecture: Union[None, str]
    motion_speed: Union[int, float]
    abs_x_tgt: Union[None, int, float]
    abs_y_tgt: Union[None, int, float]
    abs_z_tgt: Union[None, int, float]
