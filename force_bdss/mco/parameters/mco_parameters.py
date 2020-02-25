import numpy as np

from traits.api import (
    List,
    Str,
    Property,
    Float,
    Any,
    Int,
    on_trait_change,
)
from traitsui.api import (
    ListEditor,
    Item,
    View,
    HGroup,
    RangeEditor,
    TextEditor,
)

from force_bdss.local_traits import PositiveInt
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
    lower_bound = Float(0.1)

    #: Upper bound for parameter values range
    upper_bound = Float(100.0)

    #: Initial value. Defines the parameter bias
    initial_value = Float

    n_samples = Int(5)

    sample_values = Property(
        depends_on="lower_bound,upper_bound,n_samples", visible=False
    )

    def _initial_value_default(self):
        return 0.5 * (self.lower_bound + self.upper_bound)

    def _get_sample_values(self):
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
    lower_bound = List(Float(), value=[0.1])

    #: Upper vector bound for parameter values range
    upper_bound = List(Float(), value=[100.0])

    #: Initial value. Defines the parameter bias
    initial_value = List(Float())

    def _initial_value_default(self):
        return [
            0.5 * (lower_bound + upper_bound)
            for lower_bound, upper_bound in zip(
                self.lower_bound, self.upper_bound
            )
        ]

    def _get_sample_values(self):
        return [
            list(np.linspace(lower_bound, upper_bound, self.n_samples))
            for lower_bound, upper_bound in zip(
                self.lower_bound, self.upper_bound
            )
        ]

    @on_trait_change("dimension")
    def _update_bounds(self):
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
