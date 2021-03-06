#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import logging

from traits.api import Any, Enum, HasStrictTraits, Str

logger = logging.getLogger(__name__)


class VerifierError(HasStrictTraits):

    #: How severe the error is.
    severity = Enum('error', 'warning', 'information')

    #: The object that has an error.
    subject = Any

    #: Holds the trait name within :attr:`subject` which is causing the error.
    #: (Optional)
    trait_name = Str()

    #: An error message relevant to a view of the subject.
    local_error = Str()

    #: An error message relevant to the overall workflow.
    global_error = Str()

    def __init__(self, subject, **traits):
        if 'local_error' not in traits:
            traits['local_error'] = traits.get('global_error', '')
        super(VerifierError, self).__init__(subject=subject, **traits)


def verify_workflow(workflow):
    """Verifies if the workflow can be executed, and specifies where the
    error occurs and why.
    """
    result = workflow.verify()
    return result
