"""A simple adaptor for RuNNer io file formats"""


ANGSTROM_TO_BOHR = 1.8897261328
EV_TO_HARTREE = 0.0367493254
KCALMOL_TO_HARTREE = 0.001593602


def read_and_tokenize_line(in_file):
    return next(in_file).rstrip("/n").split()


class AtomicData:
    """A class that holds atomic data such as positions, forces, total_energy, charges, etc."""

    def __init__(self, atomid=0, position=(0.0, 0.0, 0.0), symbol='X', charge=0.0, energy=0.0, force=(0.0, 0.0, 0.0)):
        self.atomid = atomid
        self.position= position
        self.symbol = symbol
        self.charge = charge
        self.energy = energy
        self.force = force


class CollectiveData:
    """A class that holds collective quantities of simulated system such as total energy or charge."""

    def __init__(self, box=(0.0, 0.0, 0.0), total_energy=0.0, total_charge=0.0):
            self.box = box
            self.total_energy = total_energy
            self.total_charge = total_charge


class Sample:
    """ A class that holds a list of atomic data and also collective data for a single sample."""

    def __init__(self):
        self.atomic = []
        self.collective = None

    @property
    def number_of_atoms(self):
        return len(self.atomic)

    @property
    def total_energy(self):
        tot = 0.0
        for atom in self.atomic:
            tot += atom.energy
        return tot

    @property
    def total_charge(self):
        tot = 0.0
        for atom in self.atomic:
            tot += atom.charge
        return tot

    def find_atoms_with_symbol(self, symbol):
        sel_atoms = []
        for atom in self.atoms:
            if atom.symbol == symbol:
                sel_atoms.append(atom)
        return sel_atoms

    def get_number_of_atoms_with_symbol(self, symbol):
        return len(self.find_atoms_with_symbol(symbol))


class DataSet:
    """This class holds a collection of samples."""

    def __init__(self):
        self.samples = []

    def append(self, sample):
        """Append a sample to list of samples."""
        self.samples.append(sample)

    @property
    def number_of_samples(self):
        return len(self.samples)


class UnitConversion:
    """A class for unit conversion of RuNNer package."""

    def __init__(self, energy_conversion=1.0, length_conversion=1.0):
        self.energy = energy_conversion
        self.length = length_conversion
        self.charge = 1.0
        self.force = energy_conversion / length_conversion

    @property
    def inverse(self):
        """A method that applies inverse unit conversion."""
        return UnitConversion(1.0/self.energy, 1.0/self.length)


class RunnerAdaptor:
    """A bas class for conversion file formats of RuNNer package."""

    def __init__(self):
        self.dataset = DataSet()

    def clean(self):
        self.dataset = DataSet()

    def write_runner(self, filename, uc=UnitConversion()):
        """Write RuNNer input data."""

        with open(filename, "w") as out_file:
            # loop over samples
            for sample in self.dataset.samples:
                out_file.write("begin\n")
                out_file.write("lattice %.10f %.10f %.10f\n" % (sample.collective.box[0]*uc.length, 0.0, 0.0))
                out_file.write("lattice %.10f %.10f %.10f\n" % (0.0, sample.collective.box[1]*uc.length, 0.0))
                out_file.write("lattice %.10f %.10f %.10f\n" % (0.0, 0.0, sample.collective.box[2]*uc.length))
                # loop over atoms in a sample
                for atom in sample.atomic:
                    out_file.write("atom ")
                    out_file.write("%15.10f %15.10f %15.10f " % tuple([pos*uc.length for pos in atom.position]))
                    out_file.write("%s %15.10f %15.10f " % (atom.symbol, atom.charge*uc.charge, atom.energy*0.0))
                    out_file.write("%15.10f %15.10f %15.10f\n" % tuple([frc*uc.force for frc in atom.force]))
                out_file.write("energy %.10f\n" % (sample.collective.total_energy*uc.energy))
                out_file.write("charge %.10f\n" % (sample.collective.total_charge*uc.charge))
                out_file.write("end\n")
        return self

    def read_nnforces(self, filename, uc=UnitConversion()):
        """A method that reads predicted force for a given structure"""
        nnforces = []
        with open(filename, 'r') as infile:
            for line in infile:
                if "NNforces" in line:
                    line = line.rstrip("/n").split()
                    nnforces.append([float(_)*uc.force for _ in line[2:5]])
        return nnforces

    def read_nnenergy(self, filename, uc=UnitConversion()):
        """A method that reads predicted force for a given structure"""
        nnenergy = None
        with open(filename, 'r') as infile:
            for line in infile:
                if "NNenergy" in line:
                    line = line.rstrip("/n").split()
                    nnenergy = float(line[1])*uc.energy
                    break
        return nnenergy


class RuNNerAdaptorLAMMPS(RunnerAdaptor):
    """An inherited class for conversion file formats between RuNNer and LAMMPS packages."""

    def __init__(self):
        RunnerAdaptor.__init__(self)

    def read_lammps(self, filename, symbol_dict=None):

        with open(filename, 'r') as in_file:
            # loop over lines in file
            for line in in_file:

                # create a instance of sample data
                sample = Sample()

                # number of steps
                line = next(in_file)
                steps = int(line.split()[0])
                # number of atoms
                line = next(in_file)
                line = next(in_file)
                number_of_atoms = int(line.split()[0])
                # read box sizes, TODO: only orthogonal box
                box = []
                line = next(in_file)
                for n in range(3):
                    line = next(in_file)
                    line = line.rstrip("/n").split()
                    box.append(float(line[1]) - float(line[0]))

                # read atomic positions, symbol, charge, forces, energy, etc.
                line = next(in_file)
                for n in range(number_of_atoms):
                    line = next(in_file).rstrip("/n").split()
                    atomid = int(line[0])
                    position = (float(line[1]), float(line[2]), float(line[3]))
                    symbol = line[4]
                    charge = float(line[5])
                    energy = float(line[6])
                    force = (float(line[7]), float(line[8]), float(line[9]))
                    # convert number to an atomic symbol
                    if symbol_dict is not None:
                        symbol = symbol_dict[symbol]

                    # create atomic data and append it to sample
                    sample.atomic.append(AtomicData(atomid, position, symbol, charge, energy, force))

                # set collective data
                sample.collective = CollectiveData(tuple(box), sample.total_energy, sample.total_charge)

                # add sample to DataSet (list of samples)
                self.dataset.append(sample)

        return self

    def write_lammps(self, filename, uc=UnitConversion()):
        """A method that writes lammps input data."""
        pass


class RuNNerAdaptorVASP(RunnerAdaptor):
    """An inherited class for conversion file formats between RuNNer and VASP packages."""

    def __init__(self):
        RunnerAdaptor.__init__(self)

    def write_POSCAR(self, filename, uc=UnitConversion()):

        # with open(filename, 'w') as out_file:

            # H2O
            # 0.52918   ! scaling parameter
            #  15 0 0
            #  0 15 0
            #  0 0 15
            # 2 1
            # select
            # cart
            #       1.10    -1.43     0.00 T T F
            #       1.10     1.43     0.00 T T F
            #       0.00     0.00     0.00 F F F

            # for sample in self.dataset.samples:
            #
            #     out_file.write("H2O\n")
            #     out_file.write("1.00  ! scaling factor\n")
            #     out_file.write("%.10f %.10f %.10f\n" % (sample.collective.box[0] * uc.length, 0.0, 0.0))
            #     out_file.write("%.10f %.10f %.10f\n" % (0.0, sample.collective.box[1] * uc.length, 0.0))
            #     out_file.write("%.10f %.10f %.10f\n" % (0.0, 0.0, sample.collective.box[2] * uc.length))
            #
            #     for atom in sample.atomic:
            #         out_file.write("%15.10f %15.10f %15.10f\n" % tuple([pos*uc.length for pos in atom.position]))

        # It is already implemented in N2P2 :D
        pass

    def read_POSCAR(self, filename='POSCAR', symbol_list=None, uc=UnitConversion()):

        # create a instance of sample data
        sample = Sample()

        with open(filename, 'r') as in_file:

            # loop over lines in file
            for line in in_file:

                # create a instance of sample data
                sample = Sample()

                # read scaling factor
                line = read_and_tokenize_line(in_file)
                scaling_factor = float(line[0])
                # print (scaling_factor)

                # read box info
                box = []
                for n in range(3):
                    line = read_and_tokenize_line(in_file)
                    box.append(float(line[n])*scaling_factor*uc.length)
                # print(box)

                line = read_and_tokenize_line(in_file)
                natoms_each_type = [int(_) for _ in line]
                # print (natoms_each_type)

                # skip the line
                next(in_file)

                # check cartesian coordinates
                line = next(in_file)
                if "cart" not in line.lower():
                    raise AssertionError("Expected cartesian coordinates!")

                # read atomic positions
                atomid = 0
                for natoms, n in zip(natoms_each_type, range(len(natoms_each_type))):

                    for i in range(natoms):

                        atomid += 1
                        line = read_and_tokenize_line(in_file)

                        position = [float(_)*uc.length for _ in line[0:3]]
                        symbol = symbol_list[n]

                        # create atomic data and append it to sample
                        sample.atomic.append(AtomicData(atomid, tuple(position), symbol, 0.0, 0.0, (0.0, 0.0, 0.0)))
                        # (charge, energy, and force) * uc = 0
                        # print (symbol, position)
                # Assuming it is the end of the POSCAR
                break

            # set collective data
            sample.collective = CollectiveData(tuple(box), 0, 0)  # (total charge & energy) * uc = 0

            # add sample to DataSet (list of samples)
            self.dataset.append(sample)

        return self


    def read_OUTCAR(self, filename='OUTCAR', uc=UnitConversion()):

        with open(filename, 'r') as in_file:
            # loop over lines in file

            for line in in_file:

                # read line
                line = next(in_file)

                # read the force section
                if "POSITION" in line:
                    next(in_file)
                    for atom in self.dataset.samples[0].atomic:
                        line = read_and_tokenize_line(in_file)
                        force = [float(_)*uc.force for _ in line[3:6]]
                        atom.force = tuple(force)
                        # print(line, atom.force)

                if "total energy   ETOTAL" in line:
                    total_energy = float(line.rstrip("/n").split()[-2])
                    print (total_energy)
                    self.dataset.samples[0].collective.total_energy = total_energy

        return self

    def read_vasp(self, symbol_list=None, uc=UnitConversion()):
        self.read_POSCAR(symbol_list=symbol_list, uc=uc)
        self.read_OUTCAR(uc=uc)


if __name__ == "__main__":

    vasp = RuNNerAdaptorVASP()
    uc = UnitConversion(energy_conversion=0.1, length_conversion=1)
    vasp.read_vasp(symbol_list=['O', 'H'], uc=uc)
    vasp.write_runner(filename='inpu.data.vasp')
    # vasp.read_POSCAR(symbol_list=['O', 'H'], uc=uc)
    # vasp.read_OUTCAR(uc=uc)