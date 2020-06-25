#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import Enum, HasStrictTraits, Float, Bool

from force_bdss.local_traits import Identifier
from force_bdss.utilities import pop_dunder_recursive

# (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
# All rights reserved.

from .verifier import VerifierError


class KPISpecification(HasStrictTraits):
    #: The user defined name of the variable containing the kpi value.
    name = Identifier()

    #: The expected outcome of the procedure relative to this KPI.
    objective = Enum("MINIMISE", "MAXIMISE", "TARGET")

    #: Whether to perform auto scaling in weighted cost function of MCO.
    auto_scale = Bool(True)

    #: Manual scaling factor for weighted cost function.
    scale_factor = Float(1.)

    #: Target value to be used if optimization objective is set to
    #: "TARGET"
    target_value = Float

    #: Whether or not to use upper or lower boundaries on KPI values;
    #: may be used by some MCO engines
    use_bounds = Bool(False)

    #: Lower threshold of KPI; may be used by some MCO engines
    lower_bound = Float(0)

    #: Upper threshold of KPI; may be used by some MCO engines
    upper_bound = Float(1)

    def __getstate__(self):
        return pop_dunder_recursive(super().__getstate__())

    def verify(self):
        """ Verify the KPI specification.

        Check that the KPI specification:
        - has a name
        - has correctly assigned upper and lower bounds
        - has a correctly assigned target value

        Returns
        -------
        errors : list of VerifierErrors
            The list of all detected errors in the MCO model.
        """
        errors = []
        if not self.name:
            errors.append(
                VerifierError(
                    subject=self,
                    trait_name='name',
                    local_error="KPI is not named",
                    global_error="A KPI is not named",
                )
            )

        if self.use_bounds:
            if self.upper_bound < self.lower_bound:
                error = (
                    "Upper bound value of the KPI must be greater "
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

        if self.objective == "TARGET":
            if self.target_value == 0:
                errors.append(
                    VerifierError(
                        subject=self,
                        trait_name='target_value',
                        local_error="Target value must be non-zero",
                        global_error="A KPI does not have a target value",
                    )
                )
            if self.use_bounds:
                if (
                        self.target_value > self.upper_bound
                        or self.target_value < self.lower_bound
                ):
                    error = (
                        "Target value of the KPI must be within the "
                        "lower and the upper bounds."
                    )
                    errors.append(
                        VerifierError(
                            subject=self,
                            trait_name="target_value",
                            local_error=error,
                            global_error=error,
                        )
                    )

        return errors
