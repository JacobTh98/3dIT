import numpy as np
import json


def substitute_true_false(arr, true_value=1, false_value=0):
    return np.where(arr, true_value, false_value)


def voxel_ball(x0, y0, z0, d=3, mask=False, indices_res=(32, 32, 32)):
    x, y, z = np.indices(indices_res)
    voxel = np.sqrt((x - x0) ** 2 + (y - y0) ** 2 + (z - z0) ** 2) < d
    if mask:
        return voxel
    else:
        return substitute_true_false(voxel)


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


def scale_realworld_to_intdomain(coordinate, hitbox, new_min=0, new_max=32, d=3):
    y_r, x_r, z_r = coordinate
    new_min += d
    new_max -= d
    # set minus x,y to origin
    y_r += hitbox.y_max
    x_r += hitbox.x_max

    scaled_value_y = ((y_r) / (hitbox.y_max * 2)) * (new_max - new_min) + new_min
    scaled_value_y = int(round(min(max(scaled_value_y, new_min), new_max)))

    scaled_value_x = ((x_r) / (hitbox.x_max * 2)) * (new_max - new_min) + new_min
    scaled_value_x = int(round(min(max(scaled_value_x, new_min), new_max)))

    scaled_value_z = ((z_r - hitbox.z_min) / (hitbox.z_max - hitbox.z_min)) * (
        new_max - new_min
    ) + new_min
    scaled_value_z = int(round(min(max(scaled_value_z, new_min), new_max)))
    return scaled_value_y, scaled_value_x, scaled_value_z


def read_json_file(file_path):
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file {file_path}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
