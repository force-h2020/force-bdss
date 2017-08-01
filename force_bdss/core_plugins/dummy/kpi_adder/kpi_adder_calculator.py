from force_bdss.api import BaseKPICalculator, DataValue


class KPIAdderCalculator(BaseKPICalculator):
    def run(self, model, data_source_results):
        sum = 0.0
        for ds_res in data_source_results:
            for res in ds_res:
                if res.type != model.cuba_type_in:
                    continue

                sum += res.value

        return [
            DataValue(
                type=model.cuba_type_out,
                value=sum
            )]
