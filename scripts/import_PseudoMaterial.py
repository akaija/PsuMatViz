#------------------------------------------------------------------------------
# File import_PseudoMaterial.py
#------------------------------------------------------------------------------

# standard library imports
import sys

###############################################################################
# point Blender to third party and application specific packages

def point_blender(package_path):
    system_paths = sys.path

    check_result = [s for s in system_paths if package_path in s]

    if (check_result == []):
        sys.path.append(package_path)

p35_path        = 'C:\\Anaconda\\envs\\py35\\Lib\\site-packages'
PsuMatViz_path  = 'C:\\Users\\Alec\\Documents\\research\\repos\\PsuMatViz\\scripts'
point_blender(p35_path)
point_blender(PsuMatViz_path)

# related third party imports
import yaml
import bpy

# related application/library specific imports
import PseudoMaterial

###############################################################################
# alias bpy functions

scene       = bpy.context.scene
add_cube    = bpy.ops.mesh.primitive_cube_add
add_sphere  = bpy.ops.mesh.primitive_uv_sphere_add

def add_pseudo_material(material_file):
    with open(material_file) as source:
        pseudo_material    = yaml.load(source)
        atom_types         = pseudo_material.atom_types
        lattice_constants  = pseudo_material.lattice_constants
        atom_sites         = pseudo_material.atom_sites

if __name__ == '__main__':
    add_pseudo_material(
        'C:\\Users\\Alec\\Documents\\research\\repos\\PsuMatViz\\scripts\\output\\1732Sunday12June16\\parent.yaml'
    )

