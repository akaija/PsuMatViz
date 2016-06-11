# standard library imports
from random import choice, uniform, randrange, random

# local application/library specific imports
from PseudoMaterial import lattice_limits, number_density_limits, sigma_limits, epsilon_limits
from PseudoMaterial import PseudoMaterial

def random_number_density(lattice_constants, number_density_limits):
    max_number_density = number_density_limits[1]
    a = lattice_constants['a']
    b = lattice_constants['b']
    c = lattice_constants['c']
    max_number_of_atoms = int(max_number_density * a * b * c)
    number_of_atoms = randrange(2, max_number_of_atoms, 1)
    return number_of_atoms

def create_material(number_of_atomtypes, name):
    material = PseudoMaterial(name)

    ###########################################################################
    # define atom-types by randomly assigning LJ parameters
    atom_types = []
    for chemical_species in range(number_of_atomtypes):
        chemical_name = 'A_%s' % chemical_species
        atom_types.append({
            'chemical-id'   : chemical_name,
            'sigma'         : round(uniform(*sigma_limits), 4),
            'epsilon'       : round(uniform(*epsilon_limits), 4)
        })
    material.atom_types = atom_types

    ###########################################################################
    # randomly-assign dimensions (crystal lattice constants) and number of atoms per unit cell
    lattice_constants = {
        'a' : round(uniform(*lattice_limits), 4),
        'b' : round(uniform(*lattice_limits), 4),
        'c' : round(uniform(*lattice_limits), 4)
    }
    material.lattice_constants = lattice_constants
    number_of_atoms = random_number_density(lattice_constants, number_density_limits)

    ###########################################################################
    # populate unit cell with randomly=positioned atoms of a randomly-selected species
    atom_sites = []
    for atom in range(number_of_atoms):
        atom_type = choice(atom_types)
        atom_sites.append({
            'chemical-id'  : atom_type['chemical-id'],
            'x-pos'        : round(random(), 4),
            'y-pos'        : round(random(), 4),
            'z-pos'        : round(random(), 4)
        })
    material.atom_sites = atom_sites

    return material
