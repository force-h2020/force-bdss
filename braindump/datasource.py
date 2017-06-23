class DataSource():
    """Base class that performs calculation or extraction of information
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, name):
        self.name = name

    @abstractclassmethod
    def provides(cls):
        return [CUBA.key]

    def execute(self, parameters):
        """Performs the evaluation and returns a list of Result.
        """


class Simulator(DataSource):
    pass


class Database(DataSource):
    pass


# Represents the result of a simulator.
# It contains the resulting cuba key, the associated uncertainty and the
# originating simulator.
# Difference between uncertainty and quality: uncertainty is a numerical value
# of the value, as in the case of an experimental simulation.
# quality is the level of accuracy of the (e.g.c omputational) method, as
# the importance and reliability of that value. It should be an enumeration
# value such as HIGH, MEDIUM, POOR
Result = namedtuple("Result", "cuba_key value uncertainty originator quality")

