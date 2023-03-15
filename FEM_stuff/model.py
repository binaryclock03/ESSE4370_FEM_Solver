import copy
import numpy as np
from FEM_stuff.elements import *
from FEM_stuff.node import *
from FEM_stuff.boundary_condition import *
from FEM_stuff.load import *

class GlobalGroup():
    element_dict: dict
    node_dict: dict
    boundary_dict: dict
    load_dict: dict

    global_stiffness_matrix: np.array
    force_vector: np.array
    node_id_index_dict: dict
    node_index_id_dict: dict
    row_tracker: np.array

    solver_global_stiffness_matrix: np.array
    solver_force_vector: np.array
    solver_row_tracker: np.array

    displacements: np.array

    def __init__(self):
        self.element_dict = {}
        self.node_dict = {}
        self.boundary_dict = {}
        self.load_dict = {}

        self.node_id_index_dict = {}
        self.node_index_id_dict = {}

    ## adders
    def add_element(self, element_class:Element2D, node1_id:int, node2_id:int, id:int = -1):
        if id == -1:
            id = 0
            if  self.element_dict:
                id = max(self.element_dict.keys()) + 1

        self.element_dict.update({id: element_class(self.node_dict.get(node1_id), self.node_dict.get(node2_id))})

    def add_node(self, position: tuple, id:int = -1):
        if id == -1:
            id = 0
            if  self.node_dict:
                id = max(self.node_dict.keys()) + 1

        if len(position) == 3:
            self.node_dict.update({id: Node(node_coordinates=np.array(position), id=id)})
        else:
            self.node_dict.update({id: Node(node_coordinates=np.array([position[0], position[1], 0]), id=id)})

    def add_boundary_condition(self, node_id:int, dof:tuple, id:int = -1):
        if id == -1:
            id = 0
            if  self.boundary_dict:
                id = max(self.boundary_dict.keys()) + 1
        
        self.boundary_dict.update({id: BoundaryCondition(node_id, dof, id=id)})
    
    def add_load(self, node_id:int, load_tuple:tuple, id:int=-1):
        if id == -1:
            id = 0
            if  self.load_dict:
                id = max(self.load_dict.keys()) + 1
        
        self.load_dict.update({id: Load(node_id, load_tuple, id=id)})

    ## getters
    def get_element(self, element_id) -> Element2D:
        return self.element_dict.get(element_id)
    
    def get_node(self, node_id) -> Node:
        return self.node_dict.get(node_id)
    
    def get_boundary(self, boundary_id) -> BoundaryCondition:
        return self.boundary_dict.get(boundary_id)
    
    def get_load(self, load_id) -> Load:
        return self.load_dict.get(load_id)
    
    ## functional stuff
    def regenerate_element_lengths(self):
        for element_id in self.element_dict:
            self.element_dict.get(element_id).regenerate_node_geometry()
    
    def regenerate_elements_all(self):
        for element_id in self.element_dict:
            self.element_dict.get(element_id).regenerate_all()

    def assemble_global_stiffness_matrix(self):
        self.regenerate_elements_all()

        n_nodes = len(self.node_dict.keys())
        global_stiffness_matrix = np.zeros((n_nodes * 3, n_nodes * 3))
        row_tracker = np.zeros((n_nodes * 3, 2))

        #making the force vector
        self.force_vector = np.zeros((n_nodes * 3, 1))

        # generating correletaion between node id's and their position in the global stiffness matrix
        sorted_node_ids = sorted(self.node_dict.keys())
        for index,id in enumerate(sorted_node_ids):
            self.node_id_index_dict.update({id: index})
            self.node_index_id_dict.update({index: id})

        #making the row tracker to track nodes and their degrees of freedoms as they correlate to the rows. Will be usefull later when we start eliminating rows and columns
        for row_index in range(len(row_tracker)):
            row_tracker[row_index, 0] = self.node_index_id_dict.get(row_index // 3)
            row_tracker[row_index, 1] = row_index % 3
        self.row_tracker = row_tracker

        for id in self.element_dict.keys():
            element = self.get_element(id)
            e_stiffness_matrix = element.get_e_stiff_mat_global_coords()
            e_node1_id = element.node_1.id
            e_node2_id = element.node_2.id
            e_node1_pos = self.node_id_index_dict.get(e_node1_id) * 3
            e_node2_pos = self.node_id_index_dict.get(e_node2_id) * 3

            # top left
            global_stiffness_matrix[e_node1_pos:e_node1_pos+3, e_node1_pos:e_node1_pos+3] += e_stiffness_matrix[:3, :3]
            # bottom right
            global_stiffness_matrix[e_node2_pos:e_node2_pos+3, e_node2_pos:e_node2_pos+3] += e_stiffness_matrix[3:, 3:]

            # the other two
            global_stiffness_matrix[e_node1_pos:e_node1_pos+3, e_node2_pos:e_node2_pos+3] += e_stiffness_matrix[:3, 3:]
            global_stiffness_matrix[e_node2_pos:e_node2_pos+3, e_node1_pos:e_node1_pos+3] += e_stiffness_matrix[3:, :3]
        
        self.global_stiffness_matrix = global_stiffness_matrix

    def apply_loads(self):
        force_vector = self.force_vector
        tracker = {}
        for index in range(self.row_tracker.shape[0]):
            node_id = self.row_tracker[index, 0]
            dof = self.row_tracker[index, 1]

            tracker.update({(node_id, dof): index})
        
        for load_id in self.load_dict.keys():
            load = self.get_load(load_id)
            for dof_n in range(0,3):
                force_vector[tracker.get((load.node_id, dof_n))] = load.load_tuple[dof_n]

    def apply_boundary_conditions(self):
        bgsm = self.global_stiffness_matrix
        row_tracker = self.row_tracker
        force_vector = self.force_vector

        for bc_id in sorted(self.boundary_dict.keys(), reverse=True):
            bc = self.get_boundary(bc_id)
            node_pos = self.node_id_index_dict.get(bc.node_id) * 3
            
            for i in range(2, -1, -1):
                dof = bc.dof[i]
                if dof == 0:
                    bgsm = np.delete(bgsm, node_pos + i, 0)
                    bgsm = np.delete(bgsm, node_pos + i, 1)
                    row_tracker = np.delete(row_tracker, node_pos + i, 0)
                    force_vector = np.delete(force_vector, node_pos + i, 0)
        
        self.solver_global_stiffness_matrix = bgsm
        self.solver_row_tracker = row_tracker
        self.solver_force_vector = force_vector

    def optimize_bounded_global_stiffness_matrix(self):
        bgsm = self.solver_global_stiffness_matrix
        row_tracker = self.solver_row_tracker
        force_vector = self.solver_force_vector

        #search through matrix and find all zero rows/columns and delete them as they are not needed for solution
        to_delete = []
        for i, row in enumerate(bgsm):
            if not np.any(row):
                to_delete.append(i)
        bgsm = np.delete(bgsm, to_delete, 0)
        row_tracker = np.delete(row_tracker, to_delete, 0)
        force_vector = np.delete(force_vector, to_delete, 0)
        
        to_delete = []
        for i, column in enumerate(np.transpose(bgsm)):
            if not np.any(column):
                to_delete.append(i)
        bgsm = np.delete(bgsm, to_delete, 1)

        self.solver_global_stiffness_matrix = bgsm
        self.solver_row_tracker = row_tracker
        self.solver_force_vector = force_vector

    def find_nodal_displacements(self):
        self.displacements = np.zeros((len(self.row_tracker)))
        solved_displacements = np.matmul(np.linalg.inv(self.solver_global_stiffness_matrix), self.solver_force_vector)
        
        for row_index, node_dof_pair in enumerate(self.solver_row_tracker):
            index_1 = np.where(self.row_tracker[:,0] == node_dof_pair[0])
            index_2 = np.where(self.row_tracker[:,1] == node_dof_pair[1])
            index = int(np.intersect1d(index_1, index_2)[0])
            self.displacements[index] = solved_displacements[row_index]
            self.get_node(int(node_dof_pair[0])).displacement[int(node_dof_pair[1])] = solved_displacements[row_index]
    
    def find_mass(self):
        mass = 0
        for element_id in self.element_dict.keys():
            element = self.get_element(element_id)
            mass += element.length * element.material.density * element.shape_profile.area
        return mass

    def solve(self):
        self.assemble_global_stiffness_matrix()
        self.apply_loads()
        self.apply_boundary_conditions()
        self.optimize_bounded_global_stiffness_matrix()