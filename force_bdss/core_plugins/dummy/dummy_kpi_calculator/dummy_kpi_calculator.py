from force_bdss.api import BaseKPICalculator, bundle_id


class DummyKPICalculator(BaseKPICalculator):
    id = bundle_id("enthought", "dummy_kpi_calculator")

    def run(self, model, data_source_results):
        return data_source_results
