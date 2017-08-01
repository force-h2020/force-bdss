from force_bdss.api import BaseKPICalculator


class DummyKPICalculator(BaseKPICalculator):
    def run(self, model, data_source_results):
        return data_source_results
