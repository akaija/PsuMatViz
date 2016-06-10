#----------------------------------------------------------
# File create_material.py
#----------------------------------------------------------

# standard library imports
import os
from random import choice, random, randrange, uniform
import sys

# related third party imports
import bpy
import numpy as np

scene = bpy.context.scene
add_sphere = bpy.ops.mesh.primitive_uv_sphere_add

lattice_limits          = [13.098, 52.392]
number_density_limits   = [0.00000013907, 0.00084086]
sigma_limits            = [1.052, 6.549]
epsilon_limits          = [1.258, 513.264]

def closest_distance(x, y):
    """Find the `closest` distance over a periodic boundary.
    """
    a = 1 - y + x
    b = abs(y - x)
    c = 1 - x + y
    return min(a, b, c)

def random_position(x_o, x_r, strength):
    """Given two values, return some random point between them.
    """
    dx = closest_distance(x_o, x_r)
    if (x_o > x_r
            and (x_o - x_r) > 0.5):
        xfrac = round((x_o + strength * dx) % 1., 4)
    if (x_o < x_r
            and (x_r - x_o) > 0.5):
        xfrac = round((x_o - strength * dx) % 1., 4)
    if (x_o >= x_r
            and (x_o - x_r) < 0.5):
        xfrac = round(x_o - strength * dx, 4)
    if (x_o < x_r
            and (x_r - x_o) < 0.5):
        xfrac = round(x_o + strength * dx, 4)
    return xfrac


def MakeMaterial(name, diffuse, specular, alpha):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    mat.diffuse_shader = 'LAMBERT' 
    mat.diffuse_intensity = 1.0 
    mat.specular_color = specular
    mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = 0.5
    mat.alpha = alpha
    mat.ambient = 1
    return mat
 
def SetMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)

def random_number_density(number_density_limits, lattice_constants):
    max_number_density = number_density_limits[1]
    a = lattice_constants["a"]
    b = lattice_constants["b"]
    c = lattice_constants["c"]
    max_number_of_atoms = int(max_number_density * a * b * c)
    number_of_atoms = randrange(2, max_number_of_atoms, 1)
    return number_of_atoms
        
def apply_unit_cell(lattice_constants, material_name):
    x = lattice_constants["a"] / 2.
    y = lattice_constants["b"] / 2.
    z = lattice_constants["c"] / 2.
    add_cube = bpy.ops.mesh.primitive_cube_add
    add_cube(location=(x, y, z))
    bpy.ops.transform.resize(value=(x, y, z))
    bpy.data.objects["Cube"].select = True
    bpy.context.scene.objects[0].name = material_name + '_unit_cell'
    black = MakeMaterial('grey', (0, 0, 0), (1, 1, 1), 1)
    SetMaterial(bpy.context.object, black)
    
    unit_cell         = bpy.data.objects[material_name + '_unit_cell']
    pseudo_material   = bpy.data.objects[material_name]
    
    cut_off = pseudo_material.modifiers.new(type="BOOLEAN", name="cut_off")
    cut_off.object = unit_cell
    cut_off.operation = 'INTERSECT'
    try:
        bpy.context.scene.objects.active = pseudo_material
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="cut_off")
    except:
        pass
    bpy.context.scene.objects.active = unit_cell
    bpy.ops.object.modifier_add(type='WIREFRAME')

def make_periodic(x, y, z, a, b, c, radius, atom_material):
    if x <= 2 * radius:
            add_sphere(location=(x + a, y, z), size=radius)
            SetMaterial(bpy.context.object, atom_material)
#            bpy.ops.object.shade_smooth()
    if x + radius >= a:
            add_sphere(location=(x - a, y, z), size=radius)
            SetMaterial(bpy.context.object, atom_material)
#            bpy.ops.object.shade_smooth()
    if y <= 2 * radius:
            add_sphere(location=(x, y + b, z), size=radius)
            SetMaterial(bpy.context.object, atom_material)
#            bpy.ops.object.shade_smooth()
    if y + radius >= b:
            add_sphere(location=(x, y - b, z), size=radius)
            SetMaterial(bpy.context.object, atom_material)
#            bpy.ops.object.shade_smooth()
    if z <= 2 * radius:
            add_sphere(location=(x, y, z + c), size=radius)
            SetMaterial(bpy.context.object, atom_material)
#            bpy.ops.object.shade_smooth()
    if z + radius >= c:
            add_sphere(location=(x, y, z - c), size=radius)
            SetMaterial(bpy.context.object, atom_material)
#            bpy.ops.object.shade_smooth()
    
def create_material(number_of_atomtypes, name):
    ########################################################################
    # define pseudo atom types by randomly-generating sigma and epsilon values
    atom_types = []
    for chemical_id in range(number_of_atomtypes):
        chem_name = "A_%s" % chemical_id
        epsilon = round(uniform(*epsilon_limits), 4)
        shade = epsilon / epsilon_limits[1]
        color = (1, shade, shade)
        atom_types.append({
            "chemical-id" : chem_name,
            "sigma"       : round(uniform(*sigma_limits), 4),
            "epsilon"     : epsilon,
            "material"    : MakeMaterial(chem_name, color, (1, 1, 1), 1)
        })

    ########################################################################
    # randomly-assign dimensions (crystal lattice constants) and number of atoms per unit cell
    lattice_constants = {"a" : round(uniform(*lattice_limits), 4),
                         "b" : round(uniform(*lattice_limits), 4),
                         "c" : round(uniform(*lattice_limits), 4)}
    a = lattice_constants["a"]
    b = lattice_constants["b"]
    c = lattice_constants["c"]
    number_of_atoms   = random_number_density(number_density_limits, lattice_constants)

    ########################################################################
    # populate unit cell with randomly-positioned atoms of a randomly-selected species
    atoms = []
    for atom in range(number_of_atoms):
        atom_type = choice(atom_types)
        x = round(random(), 4)
        y = round(random(), 4)
        z = round(random(), 4)
        radius = atom_type["sigma"]
        atom_material = atom_type["material"]
        add_sphere(location=(x *a, y * b, z * c), size=radius)
        SetMaterial(bpy.context.object, atom_material)
        make_periodic(x * a, y * b, z * c, a, b, c, radius, atom_material)
        atoms.append({
            "chemical-id" : atom_type["chemical-id"],
            "x-pos"       : x,
            "y-pos"       : y,
            "z-pos"       : z
        })
    add_sphere(location=(3 * a, 3 * b, 3 * c), size = 1)
    grey = MakeMaterial('grey', (0.5, 0.5, 0.5), (1, 1, 1), 1)
    SetMaterial(bpy.context.object, grey)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.shade_smooth()
    
    bpy.ops.object.join()
    for obj in bpy.context.selected_objects:
        obj.name = name
        
    apply_unit_cell(lattice_constants, name)
    
    return lattice_constants, atom_types, atoms
    
def mutate(mutation_strength, lattice_constants, atom_types, atoms, name):
    new_atom_types = []
    for atom_type in atom_types:
        old_sigma = atom_type["sigma"]
        sigma = round(old_sigma + mutation_strength * (uniform(*sigma_limits) - old_sigma), 4)
        old_epsilon = atom_type["epsilon"]
        epsilon = round(old_epsilon + mutation_strength * (uniform(*epsilon_limits) - old_epsilon), 4)
        shade = epsilon / epsilon_limits[1]
        color = (1, shade, shade)
        name = "new_" + atom_type["chemical-id"]
        new_atom_types.append({
            "chemical-id" : name,
            "sigma"       : round(uniform(*sigma_limits), 4),
            "epsilon"     : epsilon,
            "material"    : MakeMaterial(name, color, (1, 1, 1), 1)
        })

    ########################################################################
    # randomly-assign dimensions (crystal lattice constants) and number of atoms per unit cell
    old_a = lattice_constants["a"]
    old_b = lattice_constants["b"]
    old_c = lattice_constants["c"]
    random_a = round(uniform(*lattice_limits), 4)
    random_b = round(uniform(*lattice_limits), 4)
    random_c = round(uniform(*lattice_limits), 4)
    a = round(old_a + mutation_strength * (random_a - old_a), 4)
    b = round(old_b + mutation_strength * (random_b - old_b), 4)
    c = round(old_c + mutation_strength * (random_c - old_c), 4)
    new_lattice_constants = {"a" : a, "b" : b, "c": c}

    old_ND = len(atoms) / (old_a * old_b * old_c)
    random_ND = round(uniform(*number_density_limits), 4)
    number_density = old_ND + mutation_strength * (random_ND - old_ND)
    number_of_atoms = int(number_density * a * b * c)

    ########################################################################
    # populate unit cell with randomly-positioned atoms of a randomly-selected species
    new_atoms = []
    for atom in atoms:
        chem_id = atom["chemical-id"][2:]
        old_x = atom["x-pos"]
        x = random_position(old_x, random(), mutation_strength) * a + 75
        old_y = atom["y-pos"]
        y = random_position(old_y, random(), mutation_strength) * b
        old_z = atom["z-pos"]
        z = random_position(old_z, random(), mutation_strength) * c
        atom_type = new_atom_types[int(chem_id)]
        radius = atom_type["sigma"]
        atom_material = atom_type["material"]
        add_sphere(location=(x, y, z), size=radius)
        SetMaterial(bpy.context.object, atom_material)
        make_periodic(x, y, z, a, b, c, radius, atom_material)
        new_atoms.append({
            "chemical-id" : atom_type["chemical-id"],
            "x-pos"       : x,
            "y-pos"       : y,
            "z-pos"       : z
        })
        
    add_sphere(location=(3 * a, 3 * b, 3 * c), size = 1)
    grey = MakeMaterial('grey', (0.5, 0.5, 0.5), (1, 1, 1), 1)
    SetMaterial(bpy.context.object, grey)
    
    for obj in scene.objects:
        if obj.type == 'MESH' and obj.name.startswith('Sphere'):
            obj.select = True
        else:
            obj.select = False
    bpy.ops.object.shade_smooth()
    bpy.ops.object.join()
    bpy.context.selected_objects[0].name = name

    apply_unit_cell(new_lattice_constants, name)
    
    return new_lattice_constants, new_atom_types, new_atoms

    
def run(origin):
    PLC, PAT, PA = create_material(4, 'parent')
    CLC, CAT, CA = mutate(0.1, PLC, PAT, PA, 'child')
    
if __name__ == "__main__":
    run((0, 0, 0))
