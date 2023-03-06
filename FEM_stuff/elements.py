import numpy as np
import math

import FEM_stuff.node as nd
import FEM_stuff.shape_profile as sp
import FEM_stuff.material as mt
from FEM_stuff.math_util import apply_rotation

class Element2D():
    length: float
    angle_to_x: float
    tangent_vector: np.array
    normal_vector: np.array
    element_stiffness_matrix: np.array

    shape_profile: sp.ShapeProfile
    material: mt.Material

    def __init__(self, node_1: nd.Node, node_2: nd.Node):
        self.node_1 = node_1
        self.node_2 = node_2
        self.regenerate_node_geometry()

    def assign_material(self, material: mt.Material):
        self.material = material

    def assign_shape(self, shape_profile: sp.ShapeProfile):
        self.shape_profile = shape_profile

    def regenerate_all(self):
        self.regenerate_node_geometry()
        self.regenerate_stiffness_matrix()

    def regenerate_node_geometry(self):
        disp_vec = (self.node_2.node_coordinates - self.node_1.node_coordinates)
        self.length = math.sqrt(sum(pow(value, 2) for value in disp_vec))
        self.tangent_vector = disp_vec/np.linalg.norm(disp_vec)
        self.normal_vector = np.array([-self.tangent_vector[1], self.tangent_vector[0]])
        
        if self.tangent_vector[0] == 0:
            if self.tangent_vector[1] > 0:
                self.angle_to_x = math.pi/2
            else:
                self.angle_to_x = -math.pi/2
        else:
            self.angle_to_x = math.atan(self.tangent_vector[1]/self.tangent_vector[0])

    def regenerate_stiffness_matrix(self):
        print("hi")
        pass

    def get_e_stiff_mat_global_coords(self):
        return apply_rotation(self.element_stiffness_matrix, self.angle_to_x)


class Bar_Element(Element2D):
    def regenerate_stiffness_matrix(self):
        shape_array = np.array([[ 1,  0,  0, -1,  0,  0],
                                [ 0,  0,  0,  0,  0,  0],
                                [ 0,  0,  0,  0,  0,  0],
                                [-1,  0,  0,  1,  0,  0],
                                [ 0,  0,  0,  0,  0,  0],
                                [ 0,  0,  0,  0,  0,  0]])
        
        material_part = ((self.material.youngs_modulus * self.shape_profile.area) / self.length)
        self.element_stiffness_matrix = material_part * shape_array    

class Beam_Element(Element2D):
    def regenerate_stiffness_matrix(self):
        axial_array = np.array([[ 1,  0,  0, -1,  0,  0],
                                [ 0,  0,  0,  0,  0,  0],
                                [ 0,  0,  0,  0,  0,  0],
                                [-1,  0,  0,  1,  0,  0],
                                [ 0,  0,  0,  0,  0,  0],
                                [ 0,  0,  0,  0,  0,  0]]) * ((self.material.youngs_modulus * self.shape_profile.area) / self.length)
    
        L = self.length
        L2 = self.length**2
        bend_array = np.array( [[ 0,   0,    0,  0,    0,    0],
                                [ 0,  12,  6*L,  0,  -12,  6*L],
                                [ 0, 6*L, 4*L2,  0, -6*L, 2*L2],
                                [ 0,   0,    0,  0,    0,    0],
                                [ 0, -12, -6*L,  0,   12, -6*L],
                                [ 0, 6*L, 2*L2,  0, -6*L, 4*L2]]) * ((self.material.youngs_modulus * self.shape_profile.bending_MOI) / self.length**3)
        
        self.element_stiffness_matrix = axial_array + bend_array