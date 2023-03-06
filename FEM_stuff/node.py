"""This module provides the node class"""

import numpy as np

class Node():
    """This class is used to represent a node within the FEM model. It holds the ID of the node as well as a numpy array that contains the nodes coordinates"""
    id: int
    node_coordinates:np.array

    def __init__(self, node_coordinates = np.array([0,0], dtype='f'), id:int = 0):
        self.node_coordinates = node_coordinates.astype(float)
        self.id = id
    
    def set_node_id(self, id):
        self.id = id

    def set_node_y(self, y):
        self.node_coordinates[1] = y
    
    def set_node_x(self, x):
        self.node_coordinates[0] = x

    def apply_displacement(self, value:float, dof:int, scale:float=1):
        self.node_coordinates[dof] += (value * scale)