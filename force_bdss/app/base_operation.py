from threading import Event as ThreadingEvent
import logging

from traits.api import (
    DelegatesTo,
    HasStrictTraits,
    Instance,
    provides
)

from .i_operation import IOperation
from .workflow_file import WorkflowFile

log = logging.getLogger(__name__)


@provides(IOperation)
class BaseOperation(HasStrictTraits):
    """ Base class for EvaluateOperation and OptimizeOperation.
    """

    #: The workflow file being operated on.
    workflow_file = Instance(WorkflowFile)

    #: The workflow instance.
    workflow = DelegatesTo("workflow_file")

    #: Threading Event instance that indicates if the optimization operation
    #: should be stopped.
    _stop_event = Instance(ThreadingEvent, visible=False, transient=True)

    #: Threading Event instance that indicates if the optimization operation
    #: should be paused and then resumed.
    _pause_event = Instance(ThreadingEvent, visible=False, transient=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = ThreadingEvent()
        self._pause_event = ThreadingEvent()
        self._pause_event.set()

    def run(self):
        """ Evaluate the workflow. """
        raise NotImplementedError(
            "{} must implement run".format(
                self.__class__))
