import numpy as np


def substitute_true_false(arr, true_value=10, false_value=0):
    return np.where(arr, true_value, false_value)


def random_voxel_ball(d=3, mask=False, indices_res=(32, 32, 32)):
    x, y, z = np.indices(indices_res)
    x0, y0, z0 = np.random.randint(d, high=indices_res[0] - d, size=3)
    voxel = np.sqrt((x - x0) ** 2 + (y - y0) ** 2 + (z - z0) ** 2) < d
    if mask:
        return voxel
    else:
        return substitute_true_false(voxel)


def gen_voxel_data(num, dim_expansion=True, d=3):
    X = list()
    for n in range(num):
        X.append(random_voxel_ball(d))
    X = np.array(X)
    if dim_expansion:
        return np.expand_dims(X, axis=4)
    else:
        return X
