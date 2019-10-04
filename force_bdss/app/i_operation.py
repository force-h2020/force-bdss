from traits.api import Instance, Interface

from .workflow_file import WorkflowFile


class IOperation(Interface):
    """Provides a generic interface for operations that can be
    performed by the BDSSApplication. It is expected that these
    operations will be performed on a system described by a
    serialized Workflow object, which can be interpreted by a
    WorkflowFile"""

    #: The workflow file being operated on.
    workflow_file = Instance(WorkflowFile)

    def run(self):
        """ Run an operation on the workflow. """
