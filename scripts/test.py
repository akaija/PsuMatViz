import yaml

from create_material import create_material
from mutate_material import mutate_material

number_of_atom_types = 4
mutation_strength = 0.1

parent = create_material(number_of_atom_types, 'parent')
child = mutate_material(parent, mutation_strength, 'child')

output = 'test.yaml'
with open(output, 'w') as file:
    yaml.dump(parent, file, default_flow_style=False)
    yaml.dump(child, file, default_flow_style=False)

