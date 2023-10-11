import matplotlib.pyplot as plt
from .classes import TankProperties32x2, HitBox
import numpy as np
from typing import Union


def plot_meas_coords(
    tank: TankProperties32x2,
    meas_coords: np.ndarray,
    p_select: Union[None, int] = None,
    elev: int = 20,
    azim: int = 10,
) -> None:
    """
    Visualize the planned absolute measurement coodinates.

    Parameters
    ----------
    tank : TankProperties32x2
        tank properties [mm]
    meas_coords : np.ndarray
        computed absolute measurement coordinates [mm]
    p_select : Union[None, int], optional
        highlight a single measurement coordinate, by default None
    elev : int, optional
        elevation angle of plot, by default 20
    azim : int, optional
        azimut angle of plot, by default 10
    """
    x_flat = meas_coords[:, 0]
    y_flat = meas_coords[:, 1]
    z_flat = meas_coords[:, 2]

    zyl_pnts = 50
    theta = np.linspace(0, 2 * np.pi, zyl_pnts)
    z = np.linspace(tank.T_bz[0], tank.T_bz[1], zyl_pnts)
    Z, Theta = np.meshgrid(z, theta)
    X = tank.T_r * np.cos(Theta)
    Y = tank.T_r * np.sin(Theta)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    # phantom-tank border
    ax.plot_surface(X, Y, Z, color="C7", alpha=0.2)

    if p_select == None:
        ax.scatter(x_flat, y_flat, z_flat, c="b", marker="o", alpha=0.2)
    else:
        ax.scatter(x_flat, y_flat, z_flat, c="b", marker="o", alpha=0.2)
        ax.scatter(
            meas_coords[p_select, 0],
            meas_coords[p_select, 1],
            meas_coords[p_select, 2],
            c="r",
            marker="o",
            # s=25,
        )
    ax.set_xlim([tank.T_bx[0], tank.T_bx[1]])
    ax.set_ylim([tank.T_by[0], tank.T_by[1]])
    ax.set_zlim([tank.T_bz[0], tank.T_bz[1]])

    ax.set_xlabel("x pos [mm]")
    ax.set_ylabel("y pos [mm]")
    ax.set_zlabel("z pos [mm]")
    ax.view_init(elev=elev, azim=azim)
    plt.tight_layout()
    plt.show()
