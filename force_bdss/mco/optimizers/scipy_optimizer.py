#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

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

SCIPY_ALGORITHMS_KEYS = [
    "SLSQP", "Nelder-Mead", "Powell", "CG", "BFGS",
    "Newton-CG", "L-BFGS-B", "TNC", "COBYLA",
    "trust-constr", "dogleg",
    "trust-ncg", "trust-exact", "trust-krylov"
]


class ScipyTypeError(Exception):
    pass


@provides(IOptimizer)
class ScipyOptimizer(HasStrictTraits):
    """ Optimization of an objective function using scipy.
    """

    #: Algorithms available to work with
    algorithms = Enum(*SCIPY_ALGORITHMS_KEYS)

    def optimize_function(self, func, params):
        """ Minimize the passed function.

        Parameters
        ----------
        func: Callable
            The MCO function to optimize
            Takes a list of MCO parameter values.
            Should return a scalar (i.e. a single-objective). If not the
            return (objectives) will be summed.
        params: list of MCOParameter
            The MCO parameter objects corresponding to the parameter values.

        Yields
        ------
        list of float or list:
            The list of parameter values.
            A float if the parameter is a RangedMCO type.
            A list if the parameter is a RangedVector type.

        Exception
        ---------
        ScipyTypeError
            If params has no RangedMCO or RangedVector.
        """
        # verify that all parameters are Ranged or RangedVector
        # (see the notes for this method)
        self.verify_mco_parameters(params)

        # create a "translated" function that only takes a single
        # numpy array as the parameter argument.
        tfunc = partial(self.translated_function, func=func, params=params)

        # get the initial parameter values and their bounds.
        x0, bounds = self.get_initial_and_bounds(params)

        # optimize the function
        optimization_result = scipy_optimize.minimize(
            tfunc,
            x0,
            method=self.algorithms,
            bounds=bounds
        )

        # get the optimal point (list of optimal parameter values)
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
        objective: float
            The result of the objective function. Should be a scalar. If
            it is not scalar (a list of kpis for a multiobjective function),
            then these will be summed.
        """

        # Translate the numpy array into an MCO parameter list
        param_values = self.translate_array_to_mco(array, params)

        # Call the function that takes a list of MCO parameter values
        objective = func(param_values)

        # If objective is not scalar (i.e. > 1 kpi), return its sum.
        if not np.isscalar(objective):
            return np.sum(objective)

        return objective

    @staticmethod
    def verify_mco_parameters(params):
        """ Verify that all the MCO parameters are either
            Ranged or RangedVector.

        Parameters
        ----------
        params: list of MCOParameter
        The MCO parameter objects corresponding to the parameters.

        Exception
        ---------
        ScipyTypeError
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
            if not isinstance(
                    p, (RangedMCOParameter, RangedVectorMCOParameter)):
                raise ScipyTypeError("Parameters must be ranged or vector")

    @staticmethod
    def get_initial_and_bounds(params):
        """ Get initial values ("x0") as a numpy array and bounds as a list.

        Parameters
        ----------
        params: list of MCOParameter
            The MCO parameter objects corresponding to the x0.

        Return
        ------
        numpy.array
            The initial values.
        list of tuples
            The bounds.

        Notes
        -----
        MCO parameter types other than Ranged and RangedVector are ignored.
        """

        initial_values = []
        bounds = []
        for i, p in enumerate(params):
            if isinstance(p, RangedVectorMCOParameter):
                initial_values.extend(p.initial_value)
                bounds.extend(list(zip(p.lower_bound, p.upper_bound)))
            elif isinstance(p, RangedMCOParameter):
                initial_values.append(p.initial_value)
                bounds.append((p.lower_bound, p.upper_bound))

        return np.array(initial_values), bounds

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
        >>> params = [RangedMCOParameter(),
        ...           RangedVectorMCOParameter(dimension=3)
        ...           RangedMCOParameter()]
        >>> param_values = [21, [2, 75, 10], 31]
        >>> ScipyOptimizer.translate_mco_to_array(param_values, params)
        ... array([21, 2, 75, 10, 31])

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
        >>> array = nd.array([21, 2, 75, 10, 31])
        >>> params =
        ...    [RangedMCOParameter(),
        ...     RangedVectorMCOParameter(dimension=3)
        ...     RangedMCOParameter()]
        >>> ScipyOptimizer.translate_array_to_mco(array, params)
        ... [21, [2, 75, 10], 31]

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
