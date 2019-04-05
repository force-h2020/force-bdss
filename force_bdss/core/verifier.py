import logging

from itertools import groupby

from traits.api import Any, Enum, HasStrictTraits, Unicode

logger = logging.getLogger(__name__)


class VerifierError(HasStrictTraits):

    #: How severe the error is.
    severity = Enum('error', 'warning', 'information')

    #: The object that has an error.
    subject = Any

    #: An optional trait that holds the error value.
    trait_name = Unicode

    #: An error message relevant to a view of the subject.
    local_error = Unicode

    #: An error message relevant to the overall workflow.
    global_error = Unicode

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


def multi_error_format(index_list):
    """Takes a list of integers and returns a string where they are grouped
    consecutively wherever possible.
    For example an input of [0,1,2,4,5,7] returns the string '0-2, 4-5, 7' """
    index_list.sort()
    # Single, consecutive or non-consecutive
    if len(index_list) == 1:
        return str(index_list[0])
    else:
        repl = []

        for i, index_group in groupby(enumerate(index_list), lambda val:
                                      val[0]-val[1]):
            group_index_list = []
            for enum_idx, error_idx in index_group:
                group_index_list.append(error_idx)
            if len(group_index_list) == 1:
                repl.append(str(group_index_list[0]))
            else:
                repl.append('{}-{}'.format(group_index_list[0],
                                           group_index_list[-1]))
        # Conversion from list of strings to comma separated string
        return_string = ', '.join(repl)

    return return_string
