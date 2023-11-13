import json
import os
import matplotlib.pyplot as plt
import numpy as np


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
