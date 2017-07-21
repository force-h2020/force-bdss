from force_bdss.api import BaseKPICalculator, KPICalculatorResult, bundle_id


class DummyKPICalculator(BaseKPICalculator):
    id = bundle_id("enthought", "dummy_kpi_calculator")

    def run(self, data_source_results):
        return KPICalculatorResult(
            originator=self,
            value_names=data_source_results[0].value_names,
            value_types=data_source_results[0].value_types,
            values=data_source_results[0].values.reshape(
                data_source_results[0].values.shape[:-1]))
