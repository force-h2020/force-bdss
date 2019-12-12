from force_bdss.mco.optimizer_engines.base_optimizer_engine import (
    BaseOptimizerEngine,
)


class DummyOptimizerEngine(BaseOptimizerEngine):
    def optimize(self):
        return [0.]
