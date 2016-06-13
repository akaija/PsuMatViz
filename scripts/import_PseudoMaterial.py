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

def MakeMaterial(name, diffuse, specular, alpha):
    material = bpy.data.materials.new(name)
    material.diffuse_color = diffuse
    material.diffuse_shader = 'LAMBERT'
    material.diffuse_intensity = 1.0
    material.specular_color = specular
    material.specular_shader = 'COOKTORR'
    material.specular_intensity = 0.5
    material.alpha = alpha
    material.ambient = 1
    return material

def SetMaterial(bpy_object, material):
    something = bpy_object.data
    something.materials.append(material)

def create_unit_cell(x, y, z, name):
    add_cube(location=(x / 2.,y / 2.,z / 2.))
    bpy.ops.transform.resize(value=(x / 2., y / 2., z / 2.))
    bpy.data.objects["Cube"].select = True
    bpy.context.scene.objects[0].name = name + '_unit_cell'
    black = MakeMaterial('black', (0, 0, 0), (1, 1, 1), 1)
    SetMaterial(bpy.context.object, black)

def apply_cut_off(name):
    unit_cell = bpy.data.objects[name + '_unit_cell']
    sphere    = bpy.data.objects['Sphere']

#    for obj in scene.objects:
#        if obj.type == 'MESH' and obj.name.startswith('Sphere'):
#            obj.select = True
#        else:
#            obj.select = False

    cut_off = sphere.modifiers.new(type='BOOLEAN', name='cut_off')
    cut_off.object = unit_cell
    cut_off.operation = 'INTERSECT'
    try:
       bpy.context.scene.objects.active = sphere
       bpy.ops.object.modifier_apply(apply_as='DATA', modifier='cut_off')
    except:
       pass

def make_periodic(x, y, z, a, b, c, radius, material, name):
    if x <= 2 * radius:
            add_sphere(location=(x + a, y, z), size=radius)
            SetMaterial(bpy.context.object, material)
            bpy.ops.object.shade_smooth()
    if x + radius >= a:
            add_sphere(location=(x - a, y, z), size=radius)
            SetMaterial(bpy.context.object, material)
            bpy.ops.object.shade_smooth()
    if y <= 2 * radius:
            add_sphere(location=(x, y + b, z), size=radius)
            SetMaterial(bpy.context.object, material)
            bpy.ops.object.shade_smooth()
    if y + radius >= b:
            add_sphere(location=(x, y - b, z), size=radius)
            SetMaterial(bpy.context.object, material)
            bpy.ops.object.shade_smooth()
    if z <= 2 * radius:
            add_sphere(location=(x, y, z + c), size=radius)
            SetMaterial(bpy.context.object, material)
            bpy.ops.object.shade_smooth()
    if z + radius >= c:
            add_sphere(location=(x, y, z - c), size=radius)
            SetMaterial(bpy.context.object, material)
            bpy.ops.object.shade_smooth()
    apply_cut_off(name)
    bpy.data.objects['Sphere'].select = True
    bpy.data.objects[name].select = True
    bpy.ops.object.join()

def add_pseudo_material(material_file):
    with open(material_file) as source:	
        pseudo_material    = yaml.load(source)
        atom_types         = pseudo_material.atom_types
        lattice_constants  = pseudo_material.lattice_constants
        atom_sites         = pseudo_material.atom_sites
        name               = pseudo_material.name

        epsilon_limits = [1.258, 513.264]

        a = lattice_constants['a']
        b = lattice_constants['b']
        c = lattice_constants['c']

        create_unit_cell(a, b, c, name)
        bpy.data.objects[name + '_unit_cell'].select = False

        materials = []
        radii = []
        for atom_type in atom_types:
            shade = atom_type['epsilon'] / epsilon_limits[1]
            color = (1, shade, shade)
            materials.append(
                MakeMaterial(name + '_' + atom_type['chemical-id'], color, (1, 1, 1), 1)
            )
            radii.append(atom_type['sigma'])

        first_atom = True
        for atom_site in atom_sites: 
            index = int(atom_type['chemical-id'][2:])
            radius = radii[index]
            material = materials[index]
            x = a * atom_site['x-pos']
            y = b * atom_site['y-pos']
            z = c * atom_site['z-pos']
            add_sphere(location = (x, y, z), size = radius)
            bpy.ops.object.shade_smooth()
            apply_cut_off(name)
#            if first_atom:
#                for obj in bpy.context.scene.objects:
#                    if obj.type == 'MESH' and obj.name.lower().startswith('s'):
#                        obj.name = name
#                first_atom = False
#            else:
#                bpy.data.objects['Sphere'].select = True
#                bpy.data.objects[name].select = True
#                bpy.ops.object.join()
            make_periodic(x, y, z, a, b, c, radius, material, name)

if __name__ == '__main__':
    add_pseudo_material(
        'C:\\Users\\Alec\\Documents\\research\\repos\\PsuMatViz\\scripts\\output\\1732Sunday12June16\\parent.yaml'
    )

