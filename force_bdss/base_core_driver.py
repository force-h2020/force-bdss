from envisage.plugin import Plugin
from traits.trait_types import Instance

from .core.i_factory_registry import IFactoryRegistry
from .core.workflow import Workflow
from .io.workflow_reader import WorkflowReader


class BaseCoreDriver(Plugin):
    """Main plugin that handles the execution of the MCO
    or the evaluation.
    """

    #: The registry of the factories
    factory_registry = Instance(IFactoryRegistry)

    #: Deserialized content of the workflow file.
    workflow = Instance(Workflow)

    def _factory_registry_default(self):
        return self.application.get_service(IFactoryRegistry)

    def _workflow_default(self):
        reader = WorkflowReader(self.factory_registry)
        with open(self.application.workflow_filepath) as f:
            return reader.read(f)
