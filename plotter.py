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

def plot_model_displacements(model:GlobalGroup, scale:float = 1, undeformed = True, stress = False):
    node_color = '#c7c7c7'
    node2_color = '#2596be'
    node_marker = '' 
    node2_marker = '' 
    line_color = node_color
    line2_color = 'black'
    
    if stress:
        stresses = []
        for element in model.element_dict.values():
            stresses.append(element.stress[0][0][0])
        max_stress = max(stresses)
        min_stress = min(stresses)

        if abs(max_stress) > abs(min_stress):
            highest_stress = max_stress
        else:
            highest_stress = -min_stress

    for node in model.node_dict.values():
        if undeformed:
            plt.plot(node.node_coordinates[0], node.node_coordinates[1], color = node_color, marker = node_marker, zorder=100)
        plt.plot(node.get_displaced_coordinates(scale = scale)[0], node.get_displaced_coordinates(scale = scale)[1], color = node2_color, marker = node2_marker, zorder=200)

    for element in model.element_dict.values():
        node_1_pos = element.node_1.node_coordinates
        node_2_pos = element.node_2.node_coordinates

        node_disp_1_pos = element.node_1.get_displaced_coordinates(scale = scale)
        node_disp_2_pos = element.node_2.get_displaced_coordinates(scale = scale)

        if stress:
            color_scale = -(element.stress[0][0][0])/highest_stress

            if color_scale >= (-1) and color_scale <= (-1/3):
                blue = 1
                green = (3/2)*color_scale + (3/2)
                red = 0
            elif color_scale > (-1/3) and color_scale <= (1/3):
                blue = (-3/2)*color_scale + (1/2)
                green = 1
                red = (3/2)*color_scale + (1/2)
            elif color_scale > (1/3) and color_scale <= (1):
                blue = 0
                green = (-3/2)*color_scale + (3/2)
                red = 1
            else:
                blue = 1
                green = 1
                red = 1

            blue = hex(int(255*blue)).replace("0x", "")
            if len(blue) < 2:
                blue = "0" + blue

            green = hex(int(255*green)).replace("0x", "")
            if len(green) < 2:
                green = "0" + green

            red = hex(int(255*red)).replace("0x", "")
            if len(red) < 2:
                red = "0" + red

            line2_color = '#' + red + green + blue
        
        if undeformed:
            plt.plot([node_1_pos[0], node_2_pos[0]], [node_1_pos[1], node_2_pos[1]], color = line_color)
        plt.plot([node_disp_1_pos[0], node_disp_2_pos[0]], [node_disp_1_pos[1], node_disp_2_pos[1]], color = line2_color)

    plt.title("Viewing displacement")
    if stress:
        plt.title("Viewing displacement and stresses")
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
        for stress_num, stress in enumerate(element.stress[0]):
            if max(stress) > element.material.yield_strength or abs(min(stress)) > element.material.yield_strength:
                print("WARNING ELEMENT " + str(element.id) + " HAS EXCEEDED MATERIAL YIELD STRENGTH")
            print("Element " + str(element.id) + " stress " + str(stress_num) + " (" 
                  + eng_notation(stress[0], "Pa") + ", "
                  + eng_notation(stress[1], "Pa") + ")")

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