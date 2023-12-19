import matplotlib.pyplot as plt
from .classes import TankProperties32x2, BallAnomaly, PyEIT3DMesh
import numpy as np
from typing import Union


def plot_meas_coords(
    tank: TankProperties32x2,
    meas_coords: np.ndarray,
    p_select: Union[None, int] = None,
    elev: int = 20,
    azim: int = 10,
    save_img: bool = False,
    s_path: str = "images/",
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
    save_img : bool, optional
        save the image, by default False
    s_path : str, optional
        save path, by default "images/"
    """
    x_flat = meas_coords[:, 0]
    y_flat = -meas_coords[:, 1]
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
            -meas_coords[p_select, 0],
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
    if save_img:
        plt.savefig(s_path + "plot_meas_coords.png", dpi=250)
    plt.show()


def plot_meas_coords_wball(
    tank: TankProperties32x2,
    meas_coords: np.ndarray,
    ball: BallAnomaly,
    p_select: int = 0,
    elev: int = 20,
    azim: int = 10,
    save_img: bool = False,
    s_path: str = "images/",
) -> None:
    """
    Visualize the planned absolute measurement coordinates with the placed ball object.

    Parameters
    ----------
    tank : TankProperties32x2
        tank properties [mm]
    meas_coords : np.ndarray
        computed absolute measurement coordinates [mm]
    ball : BallAnomaly
        ball properties [mm]
    p_select : Union[None, int], optional
        highlight a single measurement coordinate, by default 0
    elev : int, optional
        elevation angle of plot, by default 20
    azim : int, optional
        azimut angle of plot, by default 10
    save_img : bool, optional
        save the image, by default False
    s_path : str, optional
        save path, by default "images/"
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

    bwl_pts = 10
    u = np.linspace(0, 2 * np.pi, bwl_pts)
    v = np.linspace(0, np.pi, bwl_pts)
    x_c = meas_coords[p_select, 0] + ball.d / 2 * np.outer(np.cos(u), np.sin(v))
    y_c = meas_coords[p_select, 1] + ball.d / 2 * np.outer(np.sin(u), np.sin(v))
    z_c = meas_coords[p_select, 2] + ball.d / 2 * np.outer(
        np.ones(np.size(u)), np.cos(v)
    )

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    # phantom-tank border
    ax.plot_surface(X, Y, Z, color="C7", alpha=0.2)
    # selected bowl
    ax.plot_surface(x_c, y_c, z_c, color="C1", alpha=0.3)

    ax.scatter(x_flat, y_flat, z_flat, c="b", marker="o", alpha=0.1)
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
    if save_img:
        plt.savefig(s_path + "plot_meas_coords_wball.png", dpi=250)
    plt.show()


def plot_mesh(
    mesh: PyEIT3DMesh,
    tank: TankProperties32x2 = TankProperties32x2(),
    obj_only: bool = True,
    bg: int = 1,
    elev: int = 10,
    azim: int = 30,
    show_tank_brdr: bool = True,
) -> None:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    # phantom-tank border
    if show_tank_brdr:
        zyl_pnts = 50
        theta = np.linspace(0, 2 * np.pi, zyl_pnts)
        z = np.linspace(tank.T_bz[0], tank.T_bz[1], zyl_pnts)
        Z, Theta = np.meshgrid(z, theta)
        X = tank.T_r * np.cos(Theta)
        Y = tank.T_r * np.sin(Theta)
        ax.plot_surface(X, Y, Z, color="C7", alpha=0.2)

    # plot mesh
    if obj_only:
        ax.scatter(
            mesh.x_nodes[np.where(mesh.perm_array > bg)],
            mesh.y_nodes[np.where(mesh.perm_array > bg)],
            mesh.z_nodes[np.where(mesh.perm_array > bg)],
            marker="o",
            s=25,
            alpha=1,
        )
    else:
        ax.scatter(
            mesh.x_nodes,
            mesh.y_nodes,
            mesh.z_nodes,
            c=mesh.perm_array,
            marker="o",
            s=25,
            alpha=0.3,
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
