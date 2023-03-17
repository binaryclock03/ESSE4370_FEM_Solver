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

    plt.title("Viewing model setup")
    plt.axis('equal')
    plt.show()

def plot_model_displacements(model:GlobalGroup, scale:float = 1):
    node_color = '#c7c7c7'
    node2_color = '#2596be'
    node_marker = 'o' 
    node2_marker = 'o' 
    line_params = node_color
    line2_params = 'black'
    
    for node in model.node_dict.values():
        plt.plot(node.node_coordinates[0], node.node_coordinates[1], color = node_color, marker = node_marker, zorder=100)
        plt.plot(node.get_displaced_coordinates(scale = scale)[0], node.get_displaced_coordinates(scale = scale)[1], color = node2_color, marker = node2_marker, zorder=200)

    for element in model.element_dict.values():
        node_1_pos = element.node_1.node_coordinates
        node_2_pos = element.node_2.node_coordinates

        node_disp_1_pos = element.node_1.get_displaced_coordinates(scale = scale)
        node_disp_2_pos = element.node_2.get_displaced_coordinates(scale = scale)

        plt.plot([node_1_pos[0], node_2_pos[0]], [node_1_pos[1], node_2_pos[1]], line_params)
        plt.plot([node_disp_1_pos[0], node_disp_2_pos[0]], [node_disp_1_pos[1], node_disp_2_pos[1]], line2_params)

    plt.title("Viewing displacement")
    plt.axis('equal')
    plt.show()

def console_output_displacements(model:GlobalGroup):
    displacements = model.displacements
    row_tracker = model.row_tracker

    dof_string_dict = {0:"x", 1:"y", 2:"rotation"}

    print("\n-Nodal Displacements-")
    for index, row in enumerate(row_tracker):
        if row[1] == 2:
            print("Node " + str(int(row[0])) + " displaced in " + str(dof_string_dict.get(row[1])) + " by " + eng_notation(displacements[index], base_unit="Rad"))
        else:
            print("Node " + str(int(row[0])) + " displaced in " + str(dof_string_dict.get(row[1])) + " by " + eng_notation(displacements[index], base_unit="m"))

def console_output_stresses(model:GlobalGroup):
    print("\n-Element Stresses-")
    for element in model.element_dict.values():
        for stress_num, stress in enumerate(element.stress):
            print("Element " + str(element.id) + " stress " + str(stress_num) + " " + str(stress))

def eng_notation(value:float, base_unit:str = "") -> str:
    from math import floor, log10
    prefix_dict = {0:"", 1:"k", 2:"M", 3:"G", 4:"T", 5:"P", 6:"E", -1:"m", -2:"u", -3:"n", -4:"p", -5:"f", -6:"a"}

    if value != 0:
        prefix_n = floor((log10(abs(value)))/3)
    else:
        prefix_n = 0

    if prefix_n in prefix_dict.keys():
        return str(round(value/(1000**prefix_n), 3)) + " " + prefix_dict.get(prefix_n) + base_unit
    return value