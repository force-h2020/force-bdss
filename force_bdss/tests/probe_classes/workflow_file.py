from force_bdss.app.workflow_file import WorkflowFile
from force_bdss.core_plugins.factory_registry_plugin import (
    FactoryRegistryPlugin
)
from force_bdss.io.workflow_reader import WorkflowReader

factory_registry = FactoryRegistryPlugin()


class ProbeWorkflowFile(WorkflowFile):

    reader = WorkflowReader(factory_registry)