import os
import numpy as np
from .dataprocessing import get_sample, get_permarray_FF, get_pot_data_FF
from tqdm import tqdm


def init_train_data(l_path: str, h0: float = 1.0):
    num_samples = len(os.listdir(l_path + "data/"))

    perm_array = list()
    potentials = list()

    for idx in tqdm(range(num_samples)):
        perm_array.append(get_permarray_FF(l_path, idx, h0))
        potentials.append(get_pot_data_FF(l_path, idx))

    perm_array = np.array(perm_array)
    potentials = np.array(potentials)
    return perm_array, potentials
