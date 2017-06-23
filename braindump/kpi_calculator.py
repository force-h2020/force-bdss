class KPICalculator():
    """Base class that defines the equaation to compute the KPIs values from
    the results of the simulators

    input: a list of SimulatorResult
    output: a list of KPIs.
    """
    __metaclass__ = abc.ABCMeta

    def execute(self, datasource_results)
        """Returns the KPIResult"""


KPIResult = namedtuple("KPIResult", "name cuba_key value uncertainty quality")


