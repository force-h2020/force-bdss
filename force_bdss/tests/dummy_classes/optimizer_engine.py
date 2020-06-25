#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from force_bdss.api import BaseOptimizerEngine


class DummyOptimizerEngine(BaseOptimizerEngine):
    def optimize(self):
        return [0.0]
