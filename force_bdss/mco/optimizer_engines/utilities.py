#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import numpy as np


def convert_to_score(array, kpis):
    """ Given the `array` of raw (KPI) values, and `kpis`, return
    an array corresponding to scores in an objective function.

    If the `kpi[i].objective` value is 'MAXIMIZE', we change the
    sign of the array entry `array[i]`. If the `kpi[i].objective`
    value is  'TARGET', we change the value of the array entry
    `array[i]` to the absolute distance between `array[i]` and
    `kpi[i].target`

    Parameters
    ----------
    array: List[int, float], np.array
        array of (KPI) values to process
    kpis: List of KPISpecification
        list of KPI specification

    Returns
    --------
    substituted_values: np.array
        New array with the elements corresponding to
        kpi.objective == 'MAXIMIZE' are inverted by _a -> -_a,
        those with kpi.objective == 'TARGET' are converted by
        abs(_a - kpi.target_value)
    """
    np_kpi_mask = np.array([kpi.objective for kpi in kpis])
    np_array = np.array(
        [value if kpi.target_value is None
         else value - kpi.target_value
         for value, kpi in zip(array, kpis)]
    )

    np_array = np.where(np_kpi_mask == "MAXIMIZE", -np_array, np_array)
    return np.where(np_kpi_mask == "TARGET", np.abs(np_array), np_array)
