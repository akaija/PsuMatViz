lattice_limits         = [13.098, 52.392]
number_density_limits  = [0.00000013907, 0.00084086]
sigma_limits           = [1.052, 6.549]
epsilon_limits         = [1.258, 513.264]

class PseudoMaterial:
    '''Material class containing separate attributes for crystal lattice constants, Lennard-Jones
    paramters (atom_types), and atom-site coordinates.'''

    def __init__(self, name):
        self.name = name
