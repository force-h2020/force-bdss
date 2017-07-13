import json

from envisage.api import Application
from traits.api import Unicode, Bool, Instance

from force_bdss.workspecs.workflow import Workflow


class BDSSApplication(Application):
    """Main application for the BDSS.
    """
    id = "force_bdss.bdss_application"

    #: The path of the workflow file to open
    workflow_filepath = Unicode()

    #: Deserialized content of the workflow file.
    workflow = Instance(Workflow)

    #: This flags signals to the application not to execute and orchestrate
    #: the MCO, but instead to perform a single evaluation under the
    #: coordination of the MCO itself. See design notes for more details.
    evaluate = Bool()

    def _workflow_default(self):
        with open(self.workflow_filepath) as f:
            return Workflow.from_json(json.load(f))
