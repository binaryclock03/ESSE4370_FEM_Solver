import math
import numpy as np

def apply_element_rotation(matrix, angle):
    T = return_element_transformation_matrix(angle)
    return np.matmul(np.matmul(np.linalg.inv(T), matrix), T)

def return_element_transformation_matrix(angle):
    c = math.cos(angle)
    s = math.sin(angle)
    return np.array([[ c, -s,  0,  0,  0,  0],
                     [ s,  c,  0,  0,  0,  0],
                     [ 0,  0,  1,  0,  0,  0],
                     [ 0,  0,  0,  c, -s,  0],
                     [ 0,  0,  0,  s,  c,  0],
                     [ 0,  0,  0,  0,  0,  1]])

def apply_coordinate_rotaton(coords, angle):
    T = return_coordinate_transformation_matrix(angle)
    return np.matmul(np.linalg.inv(T), coords)

def return_coordinate_transformation_matrix(angle):
    c = math.cos(angle)
    s = math.sin(angle)
    return np.array([[ c, -s,  0],
                     [ s,  c,  0],
                     [ 0,  0,  1]])