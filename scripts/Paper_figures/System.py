class atom():

    def __init__(self):

        self.Name = ''
        self.Mass = 0.0
        self.NLevels = 0

class molecule():

    def __init__(self):

        self.Name = ''
        self.Mass = 0.0

class RateTypes():

    def __init__(self,NbProcesses):

        self.KDiss = 0.0
        self.KInel = 0.0
        self.KExch = [0.0 for iProc in range(2,NbProcesses)]
        
class system():

    def __init__(self, SystemName, NbAtoms, NbMolecules, NbProcesses):

        self.Name = SystemName

        self.NAtoms = NbAtoms
        self.Atom   = [atom() for iA in range(NbAtoms)]

        self.NMolecules = NbMolecules
        self.Molecule   = [molecule() for iMol in range(NbMolecules)]

        self.NbProcesses = NbProcesses
        self.Rates = RateTypes(NbProcesses)
