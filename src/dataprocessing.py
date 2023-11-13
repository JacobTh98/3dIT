import json
import os
import matplotlib.pyplot as plt
import numpy as np
from .classes import PyEIT3DMesh, TankProperties32x2

def get_sample(l_path: str, idx: int) -> np.lib.npyio.NpzFile:
    """
    Load a single sample out of a load path.

    Parameters
    ----------
    l_path : str
        load path
    idx : int
        sample index

    Returns
    -------
    np.lib.npyio.NpzFile
        numpy measurement file
    """
    try:
        tmp = np.load(l_path + "data/sample_{0:06d}.npz".format(idx), allow_pickle=True)
        json_file = open(l_path + "info.json")
        info_dict = json.load(json_file)
        return tmp, info_dict
    except BaseException:
        print("Error during loading")
        return None, None


def temperature_history(
    l_path, plot: bool = True, save_plot: bool = False
) -> np.ndarray:
    """
    Collects all temperature information of a measurement.
    You can plot and save the plottet result to the measurement directory.

    Parameters
    ----------
    l_path : _type_
        load path
    plot : bool, optional
        plot the temperature history, by default True
    save_plot : bool, optional
        save the plot to the l_path directory, by default False

    Returns
    -------
    np.ndarray
        temperature history
    """
    temp_hist = list()
    time_hist = list()
    for idx in range(len(os.listdir(l_path + "data/"))):
        tmp, _ = get_sample(l_path, idx)
        temp_hist.append(tmp["documentation"].tolist().temperature[0])
        time_hist.append(
            ":".join(tmp["documentation"].tolist().timestamp.split("_")[3:])
            .replace("h", "")
            .replace("m", "")
        )
    title = ".".join(tmp["documentation"].tolist().timestamp.split("_")[:3])
    temp_hist = np.array(temp_hist)
    if plot:
        plt.figure(figsize=(6, 4))
        t1 = "=".join(l_path.split("_")[1:3])
        t2 = "=".join(l_path.split("_")[3:5])[:-1]
        plt.title("measurement: " + t1 + ", " + t2 + "mm, " + title)
        plt.plot(time_hist, temp_hist)
        plt.xticks(rotation=65)
        plt.xlabel("Timestamp in hh:mm")
        plt.ylabel("Temperature in °C")
        plt.grid()
        plt.tight_layout()
        if save_plot:
            plt.savefig(l_path + "temperature_history.pdf")
        plt.show()
    return temp_hist


def get_mesh(tmp: np.lib.npyio.NpzFile) -> PyEIT3DMesh:
    mesh_obj = tmp["mesh_obj"].tolist()
    return mesh_obj



def get_trajectory(
    l_path: str,
    tank: TankProperties32x2 = TankProperties32x2(),
    elev: int = 10,
    azim: int = 30,
) -> np.ndarray:
    dir_length = len(os.listdir(l_path + "data/"))
    traj_xyz = np.zeros((dir_length, 3))

    for idx in range(dir_length):
        tmp, _ = get_sample(l_path, idx)
        traj_xyz[idx, 0] = tmp["anomaly"].tolist().x
        traj_xyz[idx, 1] = tmp["anomaly"].tolist().y
        traj_xyz[idx, 2] = tmp["anomaly"].tolist().z

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    # phantom-tank border

    zyl_pnts = 50
    theta = np.linspace(0, 2 * np.pi, zyl_pnts)
    z = np.linspace(tank.T_bz[0], tank.T_bz[1], zyl_pnts)
    Z, Theta = np.meshgrid(z, theta)
    X = tank.T_r * np.cos(Theta)
    Y = tank.T_r * np.sin(Theta)
    ax.plot_surface(X, Y, Z, color="C7", alpha=0.2)

    # plot mesh
    ax.scatter(
        traj_xyz[:, 0],
        traj_xyz[:, 1],
        traj_xyz[:, 2],
        # c=mesh.perm_array,
        marker="o",
        s=25,
        alpha=0.3,
    )
    # ax.set_xlim([tank.T_bx[0], tank.T_bx[1]])
    # ax.set_ylim([tank.T_by[0], tank.T_by[1]])
    # ax.set_zlim([tank.T_bz[0], tank.T_bz[1]])

    ax.set_xlabel("x pos [mm]")
    ax.set_ylabel("y pos [mm]")
    ax.set_zlabel("z pos [mm]")
    ax.view_init(elev=elev, azim=azim)
    plt.tight_layout()
    plt.show()
    return np.unique(traj_xyz, axis=0)