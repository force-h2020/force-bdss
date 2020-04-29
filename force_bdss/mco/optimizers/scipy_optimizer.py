import numpy as np
from functools import partial
from traits.api import (
    Enum,
    provides,
    HasStrictTraits
)

from force_bdss.mco.parameters.mco_parameters import (
    RangedMCOParameter,
    RangedVectorMCOParameter
)

from force_bdss.mco.optimizers.i_optimizer import IOptimizer

from scipy import optimize as scipy_optimize


class ScipyTypeError(Exception):
    pass


@provides(IOptimizer)
class ScipyOptimizer(HasStrictTraits):
    """ Optimization of an objective function using scipy.
    """

    #: Algorithms available to work with
    algorithms = Enum("SLSQP", "Nelder-Mead", "Powell", "CG", "BFGS",
                      "Newton-CG", "L-BFGS-B", "TNC", "COBYLA",
                      "trust-constr", "dogleg",
                      "trust-ncg", "trust-exact", "trust-krylov")

    def optimize_function(self, func, params):
        """ Minimize the passed function.

        Parameters
        ----------
        func: Callable
            The MCO function to optimize
            Takes a list of MCO parameter values.
        params: list of MCOParameter
            The MCO parameter objects corresponding to the parameter values.

        Yields
        ------
        float or list:
            The parameter values (one yield per parameter).
            A float if the parameter is a RangedMCO type.
            A list if the parameter is a RangedVector type.

        Exceptions
        ----------
        If params has no RangedMCO or RangedVector.
        """
        #: verify that all parameters are Ranged or RangedVector
        #: (see the notes for this method)
        self.verify_mco_parameters(params)

        #: create a "translated" function that only takes a single
        #: numpy array as the parameter argument.
        tfunc = partial(self.translated_function, func=func, params=params)

        #: get the intitial parameter values and their bounds.
        x0 = self.get_initial_values(params)
        bounds = self.get_bounds(params)

        #: optimize the function
        optimization_result = scipy_optimize.minimize(
            tfunc,
            x0,
            method=self.algorithms,
            bounds=bounds
        )

        #: get the optimal point (list of optimal parameter values)
        optimal_point = self.translate_array_to_mco(
            optimization_result.x, params)
        yield optimal_point

    def translated_function(self, array, func, params):
        """ A wrapper around the MCO function, where the
        MCO parameter list is replaced by a numpy array.

        Parameters
        ----------
        array: numpy.array
            The numpy array.
        func: Callable
            The MCO function that takes a list of MCO parameter values.
        params: list of MCOParameter
            The MCO parameter objects corresponding to the parameter values.

        Return
        ------
        array: numpy.array
            The optimized
        """

        #: Translate the numpy array into an MCO parameter list
        param_values = self.translate_array_to_mco(array, params)

        #: Call the function that takes a list of MCO parameter values
        print(param_values)
        objective = func(param_values)

        #: Translate the objective (kpis) into a scalar if it is not.
        #: ??????????

        return objective

    @staticmethod
    def verify_mco_parameters(params):
        """ Verify that all the MCO parameters are either
            Ranged or RangedVector.

        Parameters
        ----------
        params: list of MCOParameter
            The MCO parameter objects corresponding to the parameters.

        Exceptions
        ----------
            If any of the parameters are not Ranged or RangedVector.

        Notes
        -----
        The mapping between the numpy array (optimized by scipy) and
        the MCO parameter values, done by the methods below involves simple
        flattening and unflattening.
        e.g.  MCO parameter values <-> nd.array
        [21, [2, 75, 10], 31] <-> ([21, 2, 75, 10, 31])
        With a more complex mapping, we could ignore non-Ranged/RangedVector
        parameters, ignoring them when mapping into the numpy array and upon
        the reverse mapping, giving them their default values (they would
        not therefore be optimized). However it seems simpler (for now)
        just to raise an exception if there are any such parameters.
        """
        for p in params:
            if not (isinstance(p, RangedMCOParameter) or
                    isinstance(p, RangedVectorMCOParameter)):
                raise ScipyTypeError("Parameters must be ranged or vector")

    @staticmethod
    def get_initial_values(params):
        """ Get initial values ("x0") as a numpy array.

        Parameters
        ----------
        params: list of MCOParameter
            The MCO parameter objects corresponding to the x0.

        Return
        ------
        numpy.array
            The initial values.

        Notes
        -----
        MCO parameter types other than Ranged and RangedVector are ignored.
        """

        initial_values = []
        for i, p in enumerate(params):
            if isinstance(p, RangedVectorMCOParameter):
                initial_values.extend(p.initial_value)
            elif isinstance(p, RangedMCOParameter):
                initial_values.append(p.initial_value)

        return np.array(initial_values)

    @staticmethod
    def get_bounds(params):
        """ Get bounds as a list.

        Parameters
        ----------
        params: list of MCOParameter
            The MCO parameter objects corresponding to the x0.

        Return
        ------
        list of tuples
            The bounds.

        Notes
        -----
        MCO parameter types other than Ranged and RangedVector are ignored.
        """
        bounds = []
        for i, p in enumerate(params):
            if isinstance(p, RangedVectorMCOParameter):
                bounds.extend(list(zip(p.lower_bound, p.upper_bound)))
            elif isinstance(p, RangedMCOParameter):
                bounds.append((p.lower_bound, p.upper_bound))

        return bounds

    @staticmethod
    def translate_mco_to_array(param_values, params):
        """ Translate from list of MCO parameter values to numpy array.

        Parameters
        ----------
        param_values: list of numbers or lists
            Each entry is a number/list corresponding to the value of a
            RangedMCOParameter/RangedVectorMCOParameter, respectively
        params: list of MCOParameter
            The MCO parameter objects corresponding to the returned values.

        Return
        ------
        array: numpy.array
            The numpy array. Essentially param_values, flattened.

        Example
        -------
        params =
        [RangedMCOParameter(),
        RangedVectorMCOParameter(dimension=3)
        RangedMCOParameter()]
        param_values = [21, [2, 75, 10], 31]
        array = nd.array([21, 2, 75, 10, 31])

        Notes
        -----
        MCO parameter types other than Ranged and RangedVector are ignored.
        """

        array_values = []
        for i, p in enumerate(params):
            if i >= len(param_values):
                break
            if isinstance(p, RangedVectorMCOParameter):
                array_values.extend(param_values[i])
            elif isinstance(p, RangedMCOParameter):
                array_values.append(param_values[i])

        return np.array(array_values)

    @staticmethod
    def translate_array_to_mco(array, params):
        """ Translate from numpy array to list of MCO parameter values.

        Parameters
        ----------
        array: numpy.array
            The array to be translated.
        params: list of MCOParameter
            The MCO parameter objects corresponding to the returned values.

        Return
        ------
        param_values: list of numbers or lists
            Each entry is a number/list corresponding to the value of a
            RangedMCOParameter/RangedVectorMCOParameter, respectively

        Example
        -------
        array = nd.array([21, 2, 75, 10, 31])
        params =
        [RangedMCOParameter(),
        RangedVectorMCOParameter(dimension=3)
        RangedMCOParameter()]
        param_values = [21, [2, 75, 10], 31]

        Notes
        -----
        MCO parameter types other than Ranged and RangedVector are ignored.
        """

        param_values = []
        i = 0
        for p in params:
            if i >= len(array):
                break
            if isinstance(p, RangedVectorMCOParameter):
                if i + p.dimension > len(array):
                    break
                param_values.append(array[i: i + p.dimension].tolist())
                i += p.dimension
            elif isinstance(p, RangedMCOParameter):
                param_values.append(array[i])
                i += 1

        return param_values
