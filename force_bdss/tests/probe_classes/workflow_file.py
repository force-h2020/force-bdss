from force_bdss.app.workflow_file import WorkflowFile
from force_bdss.io.workflow_reader import WorkflowReader

from .factory_registry import ProbeFactoryRegistry


class ProbeWorkflowReader(WorkflowReader):

    def __init__(self, *args, **kwargs):
        super().__init__(factory_registry=ProbeFactoryRegistry())


class ProbeWorkflowFile(WorkflowFile):

    def _reader_default(self):
        return ProbeWorkflowReader()