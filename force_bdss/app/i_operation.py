from traits.api import Instance, Interface

from .workflow import Workflow


class IOperation(Interface):

    #: The workflow file being operated on.
    workflow_file = Instance(WorkflowFile)

    def run(self):
        """ Run an operation on the workflow. """


