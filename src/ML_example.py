import os
import numpy as np
from .dataprocessing import get_sample, get_permarray_FF, get_pot_data_FF 
def init_train_data(l_path:str):
    num_samples = len(os.listdir(l_path+"data/"))
    
    perm_array=list()
    potentials = list()
    
    for idx in range(num_samples):
        tmp,_ = get_sample(l_path,idx)
        perm_array.append(get_permarray_FF(l_path,idx))
        potentials.append(get_pot_data_FF(l_path,idx))
    
    perm_array = np.array(perm_array)
    potentials = np.array(potentials)
    return perm_array, potentials