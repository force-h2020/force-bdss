#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import numpy as np


def convert_by_mask(array, kpi_mask, key="MINIMISE"):
    """ Given the `array` of (KPI) values, changes the sign of the
    `array` entries if the corresponding `kpi_mask` entry is different
    from the `key`.
    Example:
        If the `key` is 'MINIMISE', and `kpi_mask[i]` value is 'MINIMISE',
        we don't change the sign of the array entry `array[i]`.
        Otherwise, we do change the sign.

    Parameters
    ----------
    array: List[int, float], np.array
        array of (KPI) values to change sign of
    kpi_mask: List[_type], np.array
        mask array to compare with key value
    key: object(_type)
        reference comparison value

    Returns
    --------
    substituted_values: np.array
        New array with the elements corresponding to kpi_mask == key
        are inverted by _a -> -_a
    """
    np_kpi_mask = np.array(kpi_mask)
    np_array = np.array(array)
    return np.where(np_kpi_mask == key, np_array, -np_array)
