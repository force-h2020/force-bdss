class MCO():
    """Receives a list of KPIResult to decide the next step in the parameter
    space"""
    __metaclass__ = abc.ABCMeta
    starting_point
    variable_constraints
    objectives

    def get_next_parameters(kpi_results):
        pass


class Dakota(MCO):
    def __init__(self, options):
        pass


class DakotaInput():
    """Read the parameters from the dakota input file and returns
    the parameters for further consumption"""
    def parse(filename):
        """Returns the parameters"""


class DakotaOutput():
    """Writes the KPIs to the file for consumption by Dakota"""
