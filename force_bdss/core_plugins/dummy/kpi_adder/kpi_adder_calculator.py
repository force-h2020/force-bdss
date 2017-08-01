from force_bdss.api import BaseKPICalculator, DataValue


class KPIAdderCalculator(BaseKPICalculator):
    def run(self, model, data_source_results):
        sum = 0.0

        for res in data_source_results:
            if res.type != model.cuba_type_in:
                continue

            sum += res.value

        return [
            DataValue(
                type=model.cuba_type_out,
                value=sum
            )]
