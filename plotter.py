from matplotlib import pyplot as plt
import numpy as np
from FEM_stuff.model import GlobalGroup

def plot_model_setup(model:GlobalGroup):
    node_color = 'lime'
    node_marker = 'o' 
    bc_color = node_color
    
    for node in model.node_dict.values():
        plt.plot(node.node_coordinates[0], node.node_coordinates[1], color = node_color, marker = node_marker, zorder=100)

    line_params = 'black'
    for element in model.element_dict.values():
        node_1_pos = element.node_1.node_coordinates
        node_2_pos = element.node_2.node_coordinates

        plt.plot([node_1_pos[0], node_2_pos[0]], [node_1_pos[1], node_2_pos[1]], line_params)
    
    for bc in model.boundary_dict.values():
        bc_node= model.get_node(bc.node_id)
        if bc.dof == [0, 0, 0]:
            marker = '+'
        elif bc.dof == [1, 0, 0]:
            marker = '_'
        elif bc.dof == [0, 1, 0]:
            marker = '|'
        else:
            marker = 'o'

        plt.plot(bc_node.node_coordinates[0], bc_node.node_coordinates[1], marker = marker, color = bc_color, markersize= 15, markeredgewidth = 5)
    
    for force in model.load_dict.values():
        force_node = model.get_node(force.node_id)
        force_scale = 0.01
        direction = force.load_tuple[0:2]
        direction = direction/np.linalg.norm(direction) 
        plt.arrow(force_node.node_coordinates[0], force_node.node_coordinates[1], direction[0]*force_scale, direction[1]*force_scale, color = 'r', shape = 'full', head_width = 0.2, head_length = 0.2)

    plt.axis = 'equal'
    plt.show()

def plot_model_output(model:GlobalGroup, model2:GlobalGroup):
    node_color = '#c7c7c7'
    node2_color = '#2596be'
    node_marker = 'o' 
    node2_marker = 'o' 
    line_params = node_color
    line2_params = 'black'
    
    for node in model.node_dict.values():
        plt.plot(node.node_coordinates[0], node.node_coordinates[1], color = node_color, marker = node_marker, zorder=100)

    for element in model.element_dict.values():
        node_1_pos = element.node_1.node_coordinates
        node_2_pos = element.node_2.node_coordinates

        plt.plot([node_1_pos[0], node_2_pos[0]], [node_1_pos[1], node_2_pos[1]], line_params)


    for node in model2.node_dict.values():
        plt.plot(node.node_coordinates[0], node.node_coordinates[1], color = node2_color, marker = node2_marker, zorder=200)
    
    for element in model2.element_dict.values():
        node_1_pos = element.node_1.node_coordinates
        node_2_pos = element.node_2.node_coordinates

        plt.plot([node_1_pos[0], node_2_pos[0]], [node_1_pos[1], node_2_pos[1]], line2_params)

    plt.axis = 'equal'
    plt.show()

def console_output_displacements(model:GlobalGroup):
    displacements = model.find_nodal_displacements()
    row_tracker = model.row_tracker

    dof_string_dict = {0:"x", 1:"y", 2:"rotation"}

    print("\n-Nodal Displacements-")
    for index, row in enumerate(row_tracker):
        print("Node " + str(int(row[0])) + " displaced in " + str(dof_string_dict.get(row[1])) + " by " + str(displacements[index]))
