import os
from distutils.dir_util import copy_tree
import shutil

import RASPA2

from db.__init__ import session
from db.base import Base
from db.material import Material

raspa_dir = os.path.dirname(RASPA2.__file__)
share_dir = os.path.join(raspa_dir, 'share', 'raspa')
cif_dir = os.path.join(share_dir, 'structures', 'cif')
def_dir = os.path.join(share_dir, 'forcefield')

pwd_dir = os.environ['PWD']

def copy_generation(run_id, generation, number_of_materials):
    """
    Args:
        run_id
        generation
        number_of_materials

    Returns:
        None

    """
    print('Copying:')
    print('\t%s materials' % number_of_materials)
    print('\tfrom %s' % run_id)
    print('\tgeneration %s...' % generation)
    uuids = session \
        .query(
            Material.uuid
        ) \
        .filter(
            Material.run_id == run_id,
            Material.generation == generation
        ) \
        .all()[:]

    all_dir = os.path.join(
        pwd_dir,
        '%s_GEN%s_%sMATERIALS' % (run_id, generation, number_of_materials)
    )

    counter = 0
    for uuid in uuids[:number_of_materials]:
        print('%s / %s' % (counter, number_of_materials))
        name = '%s-%s' % (run_id, uuid[0])
        out_dir = os.path.join(all_dir, name)
        os.makedirs(out_dir)
        cif_file = os.path.join(cif_dir, '%s.cif' % name)
        shutil.copy(cif_file, out_dir)
        ff_dir = os.path.join(def_dir, '%s' % name)
        copy_tree(ff_dir, out_dir)
        counter += 1
