import os

import numpy as np
import RASPA2

raspa_dir = os.path.dirname(RASPA2.__file__)
share_dir = os.path.join(raspa_dir, 'share', 'raspa')
cif_dir = os.path.join(share_dir, 'structures', 'cif')
def_dir = os.path.join(share_dir, 'forcefield')

def parse_cif(uuid):
    # finding cif-file
    for cif_file in os.listdir(cif_dir):
        if uuid in cif_file:
            cif_path = os.path.join(cif_dir, cif_file)

    # parsing atom-site locations and chemical-ids
    atom_sites = np.genfromtxt(
        cif_path,
        skip_header = 16,
        usecols = (0, 2, 3, 4),
        dtype = None
    )
    lattice_constants = np.genfromtxt(
        cif_path,
        skip_header = 4,
        skip_footer = len(atom_sites) + 9,
        usecols = 1
    )

    return atom_sites, lattice_constants

def parse_mix(uuid):
    # find force_field_mixing_rules.def
    for ff_dir in os.listdir(def_dir):
        if uuid in ff_dir:
            mix_path = os.path.join(
                def_dir,
                ff_dir,
                'force_field_mixing_rules.def'
            )

    # parse file for lennard-jones parameters
    lennard_jones = np.genfromtxt(
        mix_path,
        skip_header = 7,
        skip_footer = 9,
        usecols = (0, 2, 3),
        dtype = None
    )
    
    return lennard_jones
