import numpy as np

from traits.api import List, Str, Property, Float, Any, Int, on_trait_change
from traitsui.api import (
    ListEditor,
    Item,
    View,
    HGroup,
    RangeEditor,
    TextEditor,
)

from force_bdss.local_traits import PositiveInt
from force_bdss.core.verifier import VerifierError
from .base_mco_parameter import BaseMCOParameter
from .base_mco_parameter_factory import BaseMCOParameterFactory


class FixedMCOParameter(BaseMCOParameter):
    """ Fixed MCO parameter for (dummy) constant-valued data. The value
    must be specified before use: the value is <undefined> by default."""

    #: Fixed parameter value
    value = Any

    sample_values = Property(depends_on="value", visible=False)

    def _get_sample_values(self):
        return [self.value]


class FixedMCOParameterFactory(BaseMCOParameterFactory):
    """ Fixed Parameter factory"""

    #: This identifier must be unique for your parameter.
    #: Once again you are fully responsible for its uniqueness within the scope
    #: of the MCO it belongs to. You can have the same identifier if and only
    #: if they belong to different MCOs.
    #: Again, you are free to choose a uuid if you so prefer.
    def get_identifier(self):
        return "fixed"

    #: A name that will appear in the UI to identify this parameter.
    def get_name(self):
        return "Fixed"

    #: Definition of the associated model class.
    def get_model_class(self):
        return FixedMCOParameter

    #: A long description of the parameter
    def get_description(self):
        return "A parameter with a fixed ReadOnly value."


class RangedMCOParameter(BaseMCOParameter):
    """ Numerical MCO parameter that continuously ranges between
    lower and upper floating point values."""

    #: Lower bound for parameter values range
    lower_bound = Float(0.1, verify=True)

    #: Upper bound for parameter values range
    upper_bound = Float(100.0, verify=True)

    #: Initial value. Defines the parameter bias
    initial_value = Float(verify=True)

    n_samples = Int(5)

    sample_values = Property(
        depends_on="lower_bound,upper_bound,n_samples", visible=False
    )

    def _initial_value_default(self):
        """Default initial value lies on midpoint between lower and
        upper bounds"""
        return 0.5 * (self.lower_bound + self.upper_bound)

    def _get_sample_values(self):
        """Return linearly spaced sample values between lower and
        upper bounds"""
        return list(
            np.linspace(self.lower_bound, self.upper_bound, self.n_samples)
        )

    def default_traits_view(self):
        return View(
            Item(
                "lower_bound",
                editor=TextEditor(
                    auto_set=False, enter_set=True, evaluate=float
                ),
            ),
            Item(
                "upper_bound",
                editor=TextEditor(
                    auto_set=False, enter_set=True, evaluate=float
                ),
            ),
            Item(
                "initial_value",
                editor=RangeEditor(
                    low_name="lower_bound",
                    high_name="upper_bound",
                    format="%.3f",
                    label_width=28,
                ),
            ),
            Item("n_samples"),
        )

    def verify(self):
        """Overloads super method on BaseMCOParameter class to verify that
        initial_value attribute lies between lower and upper bounds"""
        errors = super(RangedMCOParameter, self).verify()

        if (
            self.initial_value > self.upper_bound
            or self.initial_value < self.lower_bound
        ):
            error = (
                "Initial value of the Ranged parameter must be within the "
                "lower and the upper bounds."
            )
            errors.append(
                VerifierError(
                    subject=self,
                    trait_name="initial_value",
                    local_error=error,
                    global_error=error,
                )
            )

        if self.upper_bound < self.lower_bound:
            error = (
                "Upper bound value of the Ranged parameter must be greater "
                "than the lower bound value."
            )
            errors.append(
                VerifierError(
                    subject=self,
                    trait_name="upper_bound",
                    local_error=error,
                    global_error=error,
                )
            )

        return errors


class RangedMCOParameterFactory(BaseMCOParameterFactory):
    """ Ranged Parameter factory"""

    def get_identifier(self):
        return "ranged"

    #: A name that will appear in the UI to identify this parameter.
    def get_name(self):
        return "Ranged"

    #: Definition of the associated model class.
    def get_model_class(self):
        return RangedMCOParameter

    #: A long description of the parameter
    def get_description(self):
        return "A parameter with a ranged level in floating point values."


class RangedVectorMCOParameter(RangedMCOParameter):
    """ Vector-value Ranged MCO Parameter"""

    dimension = PositiveInt(1)

    #: Lower vector bound for parameter values range
    lower_bound = List(Float(), value=[0.1], verify=True)

    #: Upper vector bound for parameter values range
    upper_bound = List(Float(), value=[100.0], verify=True)

    #: Initial value. Defines the parameter bias
    initial_value = List(Float(), verify=True)

    def _initial_value_default(self):
        """Default initial values lie on midpoint between lower and
        upper bounds for each vector"""
        return [
            0.5 * (lower_bound + upper_bound)
            for lower_bound, upper_bound in zip(
                self.lower_bound, self.upper_bound
            )
        ]

    def _get_sample_values(self):
        """Return linearly spaced sample values between lower and
        upper bounds for each vector"""
        return [
            list(np.linspace(lower_bound, upper_bound, self.n_samples))
            for lower_bound, upper_bound in zip(
                self.lower_bound, self.upper_bound
            )
        ]

    @on_trait_change("dimension")
    def _update_bounds(self):
        """Amends number of dimensions in vector in response to update
        in UI."""
        for bound_vector in (
            self.lower_bound,
            self.upper_bound,
            self.initial_value,
        ):
            if len(bound_vector) < self.dimension:
                bound_vector.extend(
                    [0.0 for _ in range(self.dimension - len(bound_vector))]
                )
            elif len(bound_vector) > self.dimension:
                bound_vector[:] = bound_vector[: self.dimension]

    def default_traits_view(self):
        return View(
            Item("dimension"),
            HGroup(
                Item("lower_bound", style="readonly"),
                Item("upper_bound", style="readonly"),
                Item("initial_value", style="readonly"),
            ),
            Item("n_samples"),
        )

    def verify(self):
        """Overloads super method on BaseMCOParameter class to verify that
        all initial_value elements lie between lower and upper bounds. Also
        checks that lower_bound, upper_bound and initial_value vectors
        have the expected dimensionality according to dimension attribute"""
        errors = super(RangedMCOParameter, self).verify()

        for name in ['initial_value', 'upper_bound', 'lower_bound']:
            vector = getattr(self, name)
            if len(vector) != self.dimension:
                error = (
                    f'List attribute {name} must possess same length as '
                    f'determined by dimension attribute: {self.dimension}'
                )
                errors.append(
                    VerifierError(
                        subject=self,
                        trait_name=name,
                        local_error=error,
                        global_error=error,
                    )
                )

        failed_init_values = []
        failed_bounds = []

        for dim in range(self.dimension):
            initial_value = self.initial_value[dim]
            upper_bound = self.upper_bound[dim]
            lower_bound = self.lower_bound[dim]

            if initial_value > upper_bound or initial_value < lower_bound:
                failed_init_values.append(dim)
            if upper_bound < lower_bound:
                failed_bounds.append(dim)

        if failed_init_values:
            error = (
                f"Initial values at indices {failed_init_values} of the "
                "Ranged Vector parameter must be within the lower and "
                "the upper bounds."
            )
            errors.append(
                VerifierError(
                    subject=self,
                    trait_name="initial_value",
                    local_error=error,
                    global_error=error,
                )
            )

        if failed_bounds:
            error = (
                f"Upper bound values at indices {failed_bounds} of the "
                "Ranged Vector parameter must greater than the lower "
                "bound values."
            )
            errors.append(
                VerifierError(
                    subject=self,
                    trait_name="upper_bound",
                    local_error=error,
                    global_error=error,
                )
            )

        return errors


class RangedVectorMCOParameterFactory(BaseMCOParameterFactory):
    """ Ranged Vector Parameter factory"""

    def get_identifier(self):
        return "ranged_vector"

    #: A name that will appear in the UI to identify this parameter.
    def get_name(self):
        return "Ranged Vector"

    #: Definition of the associated model class.
    def get_model_class(self):
        return RangedVectorMCOParameter

    #: A long description of the parameter
    def get_description(self):
        return (
            "A vector parameter with a ranged level in floating point values."
        )


class ListedMCOParameter(BaseMCOParameter):
    """ Listed MCO parameter that has discrete numerical values."""

    #: Discrete set of available numerical values
    levels = List(Float, value=[0.0])

    sample_values = Property(depends_on="levels", visible=False)

    def _get_sample_values(self):
        return sorted(self.levels)


class ListedMCOParameterFactory(BaseMCOParameterFactory):
    """ Listed Parameter factory"""

    def get_identifier(self):
        return "listed"

    #: A name that will appear in the UI to identify this parameter.
    def get_name(self):
        return "Listed"

    #: Definition of the associated model class.
    def get_model_class(self):
        return ListedMCOParameter

    #: A long description of the parameter
    def get_description(self):
        return (
            "A parameter with a listed set of levels"
            " in floating point values."
        )


class CategoricalMCOParameter(BaseMCOParameter):
    """ Categorical MCO Parameter implements unordered, discrete valued,
    categorical data. Available categorical values are strings. """

    categories = List(Str, editor=ListEditor())
    sample_values = Property(depends_on="categories", visible=False)

    def _get_sample_values(self):
        return self.categories


class CategoricalMCOParameterFactory(BaseMCOParameterFactory):
    """ The CategoricalMCOParameter factory"""

    def get_identifier(self):
        return "category"

    #: A name that will appear in the UI to identify this parameter.
    def get_name(self):
        return "Categorical"

    #: Definition of the associated model class.
    def get_model_class(self):
        return CategoricalMCOParameter

    #: A long description of the parameter
    def get_description(self):
        return "A Categorical parameter defining unordered discrete objects."
