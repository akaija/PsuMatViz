import os

from datetime import datetime
import yaml

from create_material import create_material
from mutate_material import mutate_material
from PseudoMaterial import PseudoMaterial

number_of_atom_types = 4
mutation_strength = 0.1
segments = 5

output_dir = os.path.join(os.getcwd(), 'output')
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
output_path = os.path.join(output_dir, datetime.now().strftime('%H%M%A%d%B%y'))
os.mkdir(output_path)

print('Creating materials in:\n%s\n' % output_path)

parent = create_material(number_of_atom_types, 'parent')
child = mutate_material(parent, mutation_strength, 'child')

def translate(value, i, frac):
    if value == 'sigma' or value == 'epsilon':
        p = parent.atom_types[i][value]
        c = child.atom_types[i][value]
    if value == 'a' or value == 'b' or value == 'c':
        p = parent.lattice_constants[value]
        c = child.lattice_constants[value]
    if value == 'x-pos' or value == 'y-pos' or value == 'z-pos':
        p = parent.atom_sites[i][value]
        c = child.atom_sites[i][value]
    new_value = p + frac * (c - p)
    return new_value

def write_to_file(file_path, pseudo_material):
    with open(file_path, 'w') as file:
        yaml.dump(pseudo_material, file, default_flow_style=False)

def transition(parent, child, segments):
    print('...')
    similarity = [i / segments for i in range(1, segments - 1)]

    counter = 0
    for frac in similarity:
        name = 'intermediate_%s' % counter
        intermediate = PseudoMaterial(name)

        atom_types = []
        for i in range(len(parent.atom_types)):
            atom_types.append({
                'chemical-id'  : parent.atom_types[i]['chemical-id'],
                'sigma'        : translate('sigma', i, frac),
                'epsilon'      : translate('epsilon', i, frac)
            })
        intermediate.atom_types = atom_types

        lattice_constants = {
            'a' : translate('a', i, frac),
            'b' : translate('b', i, frac),
            'c' : translate('c', i, frac)
        }
        intermediate.lattice_constants = lattice_constants

        atom_sites = []
        for i in range(len(parent.atom_sites)):
            atom_sites.append({
                'chemical-id'  : parent.atom_sites[i]['chemical-id'],
                'x-pos'        : translate('x-pos', i, frac),
                'y-pos'        : translate('y-pos', i, frac),
                'z-pos'        : translate('z-pos', i, frac)
            })
        intermediate.atom_sites = atom_sites

        output_file = os.path.join(output_path, name + '.yaml')
        write_to_file(output_file, intermediate)
        counter += 1

            
print('...')
write_to_file(os.path.join(output_path, 'parent.yaml'), parent)
print('...')
write_to_file(os.path.join(output_path, 'child.yaml'), child)
transition(parent, child, segments)

print('...done!')
