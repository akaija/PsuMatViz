import bpy

from PseudoMaterial import PseudoMaterial

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

def create_unit_cell(material):
    dimensions = material.lattice_constants / 2.
    add_cube(location = *dimensions)
    bpy.ops.transform.resize(value = *dimensions)
    bpy.data.objects['Cube'].select = True
    cell_name = 'UnitCell_%s' % material.uuid
    bpy.context.scene.objects[0].name = cell_name
    black = MakeMaterial('black', (0, 0, 0), (1, 1, 1), 1)
    SetMaterial(bpy.context.object, black)
    bpy.data.objects[cell_name].select = False

def add_atom_site(x, y, z, radius,  material, site_count):
    add_sphere(location = (x, y, z), size = radius)
    bpy.data.objects['Sphere'].select = True
    bpy.ops.object.shade_smooth()
    SetMaterial(bpy.context.object, material)
    site_name = 'AtomSite_%s' % site_count
    bpy.context.scene.objects[0].name = site_name
    apply_cutoff(site_name, material)
    bpy.data.objects[site_name].select = False
    return site_count += 1

def apply_cut_off(name, material):
    unit_cell = bpy.data.objects['UnitCell_%s' % material.uuid]
    atom_site = bpy.data.objects[name]
    cut_off = atom_site.modifiers.new(type='BOOLEAN', name='cut_off')
    cut_off.object = unit_cell
    cut_off.operation = 'INTERSECT'
    try:
        bpy.context.scene.objects.active = sphere
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier='cut_off')
    except:
        pass

def add_periodic_segments(atom_site, chemical_species, site_count):
    for species in chemical_species:
        if species['chemical'] == atom_site[0]:
            radius = species['radius']
            material = species['material']
    [a, b, c] = [*material.lattice_constants]
    x = atom_site[1] * a
    y = atom_site[2] * b
    z = atom_site[3] * c
    if x <= radius:
        site_count = add_atom_site(x + a, y, z, radius, material, site_count)
    if x + radius >= a:
        site_count = add_atom_site(x - a, y, z, radius, material, site_count)
    if y <= radius:
        site_count = add_atom_site(x, y + b, z, radius, material, site_count)
    if y + radius >= b:
        site_count = add_atom_site(x, y - b, z, radius, material, site_count)
    if z <= radius:
        site_count = add_atom_site(x, y, z + c, radius, material, site_count)
    if z + radius >= c:
        site_count = add_atom_site(x, y, z - c, radius, material, site_count)
    return site_count

def visualise_pseudo_material(uuid):
    material = PseudoMaterial(uuid)
    create_unit_cell(material)    

    epsilon_limits = [1.258, 513.264]

    chemical_species = []
    for species in material.lennard_jones
        specimen = {
            'chemical' : species[0],
            'radius'   : species[2],
            'material' : MakeMaterial(
            '%s_%s' % (species[0], material.uuid),
                (
                    1,
                    species[1] / epsilon_limits[0],
                    species[1] / epsilon_limits[0]
                ),
                (1, 1, 1),
                1
            )
        }
        chemical_species.append(specimen)

    site_count = 0
    for atom_site in material.atom_sites:
        for species in chemical_species:
            if species['chemical'] == atom_site[0]:
                radius = species['radius']
                material = species['material']
        x = atom_site[1] * material.lattice_constants[0]
        y = atom_site[2] * material.lattice_constants[1]
        z = atom_site[3] * material.lattice_constants[2]
        site_count = add_atom_site(x, y, z, radius, material, site_count) 
        site_count = add_periodic_segments(
            atom_site, chemical_species, site_count
        )

    unit_cell_name = 'UnitCell_%s' % uuid
    bpy.data.objects[unit_cell_name].select = True
    bpy.context.scene.objects.active = bpy.data.objects[unit_cell_name]
    bpy.ops.object.modifier_add(type='WIREFRAME')
