import os
import shutil

import RASPA2

raspa_dir = os.path.dirname(RASPA2.__file__)
share_dir = os.path.join(raspa_dir, 'share', 'raspa')
cif_dir = os.path.join(share_dir, 'structures', 'cif')
def_dir = os.path.join(share_dir, 'forcefield')

pwd_dir = os.environ['PWD']

def move_to_raspa(directory):
    """
    Args:
        directory

    Returns:
        None

    """
    in_dir = os.path.join(pwd_dir, directory)
    materials = os.listdir(in_dir)
    for material in materials:
        print('\ncopying files for %s' % material)
        mat_dir = os.path.join(in_dir, material)
        ff_dir = os.path.join(def_dir, material)
        mat_files = os.listdir(mat_dir)
        os.makedirs(ff_dir)
        for file in mat_files:
            file_to_copy = os.path.join(mat_dir, file)
            print('\t%s' % file)
            if '.cif' in file:
                shutil.copy(file_to_copy, cif_dir)
            elif '.def' in file:
                shutil.copy(file_to_copy, ff_dir)
