from traits.api import File, HasStrictTraits, Instance, List

from force_bdss.core.workflow import Workflow
from force_bdss.core.verifier import VerifierError
from force_bdss.io.workflow_reader import WorkflowReader
from force_bdss.io.workflow_writer import WorkflowWriter


class WorkflowFile(HasStrictTraits):
    """ A file which contains a serialized workflow. """

    #: The path to the file.
    path = File

    #: The workflow model.
    workflow = Instance(Workflow)

    #: The list of errors in the workflow, if any.
    errors = List(Instance(VerifierError))

    #: The workflow model reader for this file.
    reader = Instance(WorkflowReader)

    #: The workflow model writer for this file.
    writer = Instance(WorkflowWriter)

    @classmethod
    def from_path(cls, path, **traits):
        workflow_file = cls(path=path, **traits)
        workflow_file.read()
        return workflow_file

    def read(self):
        """ Read the workflow from disk. """
        if self.reader is None:
            raise ValueError("No workflow reader specified.")

        with open(self.path, 'r') as input_file:
            self.workflow = self.reader.read(input_file)

    def write(self):
        """ Write the workflow to disk. """
        if self.writer is None:
            raise ValueError("No workflow writer specified.")
        self.writer.write(self.workflow, self.path)

    def verify(self):
        """ Find any errors in the workflow. """
        self.errors = self.workflow.verify()
