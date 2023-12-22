import numpy as np


def substitute_true_false(arr, true_value=1, false_value=0):
    return np.where(arr, true_value, false_value)


def random_voxel_ball(d=3, mask=False, indices_res=(32, 32, 32)):
    x, y, z = np.indices(indices_res)
    x0, y0, z0 = np.random.randint(d, high=indices_res[0] - d, size=3)
    voxel = np.sqrt((x - x0) ** 2 + (y - y0) ** 2 + (z - z0) ** 2) < d
    if mask:
        return voxel
    else:
        return substitute_true_false(voxel)


def gen_voxel_ball_data(num, dim_expansion=True, d=3):
    X = list()
    for n in range(num):
        X.append(random_voxel_ball(d))
    X = np.array(X)
    if dim_expansion:
        return np.expand_dims(X, axis=4)
    else:
        return X


def random_voxel_brick(d_xyz=[5, 5, 5], mask=False, indices_res=(32, 32, 32)):
    x, y, z = np.indices(indices_res)
    x0, y0, z0 = np.random.randint(
        np.max(d_xyz), high=indices_res[0] - np.max(d_xyz), size=3
    )
    voxel = (
        (x >= x0 - d_xyz[0])
        & (x < x0 + d_xyz[0])
        & (y >= y0 - d_xyz[1])
        & (y < y0 + d_xyz[1])
        & (z >= z0 - d_xyz[2])
        & (z < z0 + d_xyz[2])
    )

    if mask:
        return voxel
    else:
        return substitute_true_false(voxel)


def gen_voxel_brick_data(num, dim_expansion=True, d_xyz=[5, 5, 5]):
    X = list()
    for n in range(num):
        X.append(random_voxel_brick(d_xyz))
    X = np.array(X)
    if dim_expansion:
        return np.expand_dims(X, axis=4)
    else:
        return X
