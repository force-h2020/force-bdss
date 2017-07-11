import json

from envisage.api import Application
from traits.api import Unicode
from traits.trait_types import List, Bool, Instance

from force_bdss.workspecs.workflow import Workflow


class BDSSApplication(Application):
    id = "force_bdss.bdss_application"

    workflow_filepath = Unicode()

    workflow = Instance(Workflow)

    evaluate = Bool()

    def _workflow_default(self):
        with open(self.workflow_filepath) as f:
            return Workflow.from_json(json.load(f))
