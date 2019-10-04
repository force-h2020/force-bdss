from force_bdss.app.workflow_file import WorkflowFile
from force_bdss.io.workflow_reader import WorkflowReader
from force_bdss.io.workflow_writer import WorkflowWriter


from .factory_registry import ProbeFactoryRegistry


class ProbeWorkflowReader(WorkflowReader):

    def __init__(self, *args, **kwargs):
        super().__init__(factory_registry=ProbeFactoryRegistry())


class DummyWorkflowWriter(WorkflowWriter):

    def write(self, *args, **kwargs):
        return True


class ProbeWorkflowFile(WorkflowFile):

    def _reader_default(self):
        return ProbeWorkflowReader()

    def _writer_default(self):
        return DummyWorkflowWriter()
