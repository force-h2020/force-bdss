#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import json
from traits.api import HasStrictTraits, ReadOnly


class WorkflowWriter(HasStrictTraits):
    """A Writer for writing the Workflow onto disk.
    """

    version = ReadOnly("1.1")

    def write(self, workflow, path, *, mode="w"):
        """Writes the workflow model object to a file f in JSON format.

        Parameters
        ----------
        workflow: Workflow
            The Workflow instance to write to file

        path: string
            A path string of the file on which to write the workflow

        mode: string
            file open mode, "w" by default to write
        """
        data = {
            "version": self.version,
            "workflow": self.get_workflow_data(workflow),
        }

        with open(path, mode) as f:
            json.dump(data, f, indent=4)

    def get_workflow_data(self, workflow):
        """ Public method to get a serialized form of workflow"""
        return workflow.__getstate__()
