import math
import numpy as np

def apply_rotation(matrix, angle):
    T = return_transformation_matrix(-angle)
    return np.matmul(np.matmul(np.transpose(T), matrix), T)

def return_transformation_matrix(angle):
    c = math.cos(angle)
    s = math.sin(angle)
    return np.array([[ c, -s,  0,  0,  0,  0],
                     [ s,  c,  0,  0,  0,  0],
                     [ 0,  0,  1,  0,  0,  0],
                     [ 0,  0,  0,  c, -s,  0],
                     [ 0,  0,  0,  s,  c,  0],
                     [ 0,  0,  0,  0,  0,  1]])