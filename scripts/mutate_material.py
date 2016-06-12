# standard library imports
from random import choice, uniform

# related third party imports
from numpy import prod

# local application/library specific imports
from PseudoMaterial import lattice_limits, number_density_limits, sigma_limits, epsilon_limits
from PseudoMaterial import PseudoMaterial

def perturb(value, limits, mutation_strength):
    new_value = round(value + mutation_strength * (uniform(*limits) - value), 4)
    return new_value

def mutate_material(material, mutation_strength, name):
    '''Create new material by perturbing the parameters which define a pseudo-material, the
    magnitude of these perturbations is dictated by a mutation strength parameter (0,1)
    '''

    old_material           = material
    old_atom_types         = material.atom_types
    old_lattice_constants  = material.lattice_constants
    old_atom_sites         = material.atom_sites

    new_material           = PseudoMaterial(name)

    ###########################################################################
    # create new atom-types
    new_atom_types = []
    for atom_type in old_atom_types:
        old_sigma    = atom_type['sigma']
        old_epsilon  = atom_type['epsilon']

        new_atom_types.append({
            'chemical-id'  : atom_type['chemical-id'],
            'sigma'        : perturb(old_sigma, sigma_limits, mutation_strength),
            'epsilon'      : perturb(old_epsilon, epsilon_limits, mutation_strength)
        })
    new_material.atom_types = new_atom_types

    ###########################################################################
    # create new lattice constants
    lattice_constants = {
        'a'  : perturb(old_lattice_constants['a'], lattice_limits, mutation_strength),
        'b'  : perturb(old_lattice_constants['b'], lattice_limits, mutation_strength),
        'c'  : perturb(old_lattice_constants['c'], lattice_limits, mutation_strength)
    }
    new_material.lattice_constants = lattice_constants

#    old_number_density = len(material.atom_sites) / prod([old_lattice_constants[i]
#        for i in old_lattice_constants])
#    number_density = perturb(old_number_density, number_density_limits, mutation_strength)
#    number_of_atoms = int(number_density * prod([lattice_constants[i] for i in lattice_constants]))

    ###########################################################################
    # populate unit cell with atom-sites
    new_atom_sites = []
    for atom_site in old_atom_sites:
        new_atom_sites.append({
            'chemical-id'  : atom_site['chemical-id'],
            'x-pos'        : perturb(atom_site['x-pos'], lattice_limits, mutation_strength),
            'y-pos'        : perturb(atom_site['y-pos'], lattice_limits, mutation_strength),
            'z-pos'        : perturb(atom_site['z-pos'], lattice_limits, mutation_strength)
        })
    new_material.atom_sites = new_atom_sites

    return new_material
