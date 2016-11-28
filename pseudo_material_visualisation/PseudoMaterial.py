from parse_files import *

class PseudoMaterial:
    '''Material class containing separate attributes for crystal lattice constants, Lennard-Jones
    paramters (atom_types), and atom-site coordinates.'''

    def __init__(self, uuid, forcefield):
        self.uuid = uuid
        # parse cif-file
        atom_sites, lattice_constants = parse_cif(uuid)
        self.atom_sites = atom_sites
        self.lattice_constants = lattice_constants
        # parse force_field_mixing_rules.def
        if forcefield == None:
            self.lennard_jones = parse_mix(uuid)
        elif forcefield != None:
            self.lennard_jones = parse_mix(forcefield)
