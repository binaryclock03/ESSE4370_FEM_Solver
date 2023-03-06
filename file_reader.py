from FEM_stuff.elements import *
from FEM_stuff.shape_profile import *
from FEM_stuff.material import Material
from FEM_stuff.model import GlobalGroup

import yaml
from yaml.loader import SafeLoader

def load_model(file_path = "thing.yaml") -> GlobalGroup:

    model = GlobalGroup()

    materials_dict = {}
    shape_dict = {}

    groups = {  'materials': load_material,
                'shape_profiles': load_shape_profile,
                'nodes': load_node,
                'elements': load_element,
                'loads': load_load,
                'boundary_conditions': load_boundary_condition}

    with open(file_path, 'r') as file:
        data = list(yaml.load_all(file, Loader=SafeLoader))[0]

        for group_name in groups.keys():
            if group_name in data.keys():
                print("Found " + group_name + " list, proccesing " + str(len(data.get(group_name))) + " " + group_name)
                for group_element in data.get(group_name):
                    groups.get(group_name)(group_element, [model, materials_dict, shape_dict])

            else:
                print("[WARNING] No " + group_name + " list found")
    
    return model

def load_node(node, args):
    model:GlobalGroup = args[0]
    id = node.get('id')
    position = tuple(node.get('position'))
    model.add_node(position, id=id)

def load_element(element, args):
    model:GlobalGroup = args[0]
    material_dict:dict = args[1]
    shape_dict:dict = args[2]

    element_type_dict = {"Bar_Element": Bar_Element,
                         "Beam_Element": Beam_Element}
    id = element.get('id')
    node_1_id = element.get('node_ids')[0]
    node_2_id = element.get('node_ids')[1]
    element_type_str = element.get('element_type')
    model.add_element(element_type_dict.get(element_type_str), 
                      node_1_id, 
                      node_2_id, 
                      id=id)
    
    material = material_dict.get(element.get('material'))
    model.get_element(id).assign_material(material)

    shape = shape_dict.get(element.get('shape_profile'))
    model.get_element(id).assign_shape(shape)
    
def load_load(load, args):
    model:GlobalGroup = args[0]
    id = load.get('id')
    node_id = load.get('node_id')
    force_tuple = tuple(load.get('force'))
    model.add_load(node_id, force_tuple, id=id)

def load_boundary_condition(bc, args):
    model:GlobalGroup = args[0]
    id = bc.get('id')
    node_id = bc.get('node_id')
    dof = bc.get('dof')
    model.add_boundary_condition(node_id, dof, id=id)

def load_material(material, args):
    material_dict:dict = args[1]
    id = material.get('id')
    name = material.get('name')
    youngs_modulus = material.get('youngs_modulus')
    yield_strength = material.get('yield_strength')
    density = material.get('density')
    material_dict.update({name:Material(name = name, 
                                        youngs_modulus=youngs_modulus, 
                                        yield_strength=yield_strength,
                                        density=density)})

def load_shape_profile(shape, args):
    shape_profile_dict:dict = args[2]
    id = shape.get('id')
    name = shape.get('name')
    shape_profile_type_str = shape.get('shape_profile_type')
    parameters = shape.get('parameters')

    if shape_profile_type_str == "ShapeProfileArea":
        shape_profile_dict.update({name:ShapeProfileArea(name = name,area = parameters.get('area'))})