import unittest

from force_bdss.core.data_value import DataValue
from force_bdss.core_driver_events import MCOProgressEvent


class TestCoreDriverEvents(unittest.TestCase):
    def test_getstate_for_progress_event(self):
        ev = MCOProgressEvent()
        ev.optimal_kpis = [DataValue(value=10)]
        ev.optimal_point = [DataValue(value=12), DataValue(value=13)]
        ev.weights = [1.0]

        self.maxDiff = 1000
        self.assertEqual(
            ev.__getstate__(),
            {
                'optimal_kpis': [
                    {
                        'accuracy': None,
                        'name': '',
                        'quality': 'AVERAGE',
                        'type': '',
                        'value': 10
                    }],
                'optimal_point': [
                   {
                       'accuracy': None,
                       'name': '',
                       'quality': 'AVERAGE',
                       'type': '',
                       'value': 12},
                   {
                       'accuracy': None,
                       'name': '',
                       'quality': 'AVERAGE',
                       'type': '',
                       'value': 13
                   }
                ],
                'weights': [1.0]
            }
        )
