from typing import Union
from .classes import TankProperties32x2, BallObjectProperties, HitBox
import numpy as np


def compute_hitbox(
    tank: TankProperties32x2,
    ball: BallObjectProperties,
    safety_tolerance: Union[int, float] = 5.0,
) -> HitBox:
    """
    Compute the hitbox if a ball object is placed inside the 32x2 tank.

    Parameters
    ----------
    tank : TankProperties32x2
        tank properties [mm]
    ball : BallObjectProperties
        ball properties [mm]
    safety_tolerance : Union[int, float], optional
        border tolerance [mm], by default 5.0

    Returns
    -------
    HitBox
        x,y,z limits for measurements [mm]
    """
    hitbox = HitBox(
        r_min=0,
        r_max=tank.T_bx[1] - ball.r - safety_tolerance,
        x_min=tank.T_bx[0] + ball.r + safety_tolerance,
        x_max=tank.T_bx[1] - ball.r - safety_tolerance,
        y_min=tank.T_by[0] + ball.r + safety_tolerance,
        y_max=tank.T_by[1] - ball.r - safety_tolerance,
        z_min=tank.T_bz[0] + ball.r + safety_tolerance,
        z_max=tank.T_bz[1] - ball.r - safety_tolerance,
    )
    return hitbox


def create_meas_coordinates(
    hitbox: HitBox, x_pts: int, y_pts: int, z_pts: int
) -> np.ndarray:
    """
    Create the measurement trajectory/points with respect on the hitbox.

    Parameters
    ----------
    hitbox : HitBox
        x,y,z limits for measurements [mm]
    x_points : int
        number of measurement points on the x-axis
    y_points : int
        number of measurement points on the y-axis
    z_points : int
        number of measurement points on the z-axis

    Returns
    -------
    np.ndarray
        computed absolute measurement coordinates [mm]
    """
    x = np.linspace(hitbox.x_min, hitbox.x_max, x_pts)
    y = np.linspace(hitbox.y_min, hitbox.y_max, y_pts)
    z = np.linspace(hitbox.z_min, hitbox.z_max, z_pts)

    xx, yy, zz = np.meshgrid(x, y, z)

    distances = np.sqrt(xx**2 + yy**2)
    mask = distances <= hitbox.r_max

    x_flat = xx[mask].flatten()
    y_flat = yy[mask].flatten()
    z_flat = zz[mask].flatten()

    coordinates = np.vstack((x_flat, y_flat, z_flat)).T

    print(
        f"HitBox(x_pts,y_pts,z_pts) leads to {coordinates.shape[0]} available points."
    )
    print(f"So {coordinates.shape[0]} points will be measured.")
    return coordinates


def print_coordinates_props(coordinates: np.ndarray) -> None:
    """
    Print properties of coodinates

    Parameters
    ----------
    coordinates : np.ndarray
        computed absolute measurement coordinates [mm]
    """
    print("Properties of the computed coordinates")
    print("--------------------------------------")
    for ax in range(3):
        print(
            f"min:{np.min(coordinates[:,ax]):.2f}\tmax: {np.max(coordinates[:,ax]):.2f}"
        )
    print(f"\nshape {coordinates.shape}")
