try:
    import mock
except ImportError:
    from unittest import mock

from envisage.plugin import Plugin

from traits.api import HasStrictTraits, Function, Str, Int


class ProbeEvaluatorFactory(HasStrictTraits):
    def __init__(self, plugin=None, *args, **kwargs):
        if plugin is None:
            plugin = mock.Mock(Plugin)

        super(ProbeEvaluatorFactory, self).__init__(
            plugin=plugin, *args, **kwargs)

    run_function = Function

    input_slots_type = Str('PRESSURE')
    output_slots_type = Str('PRESSURE')

    input_slots_size = Int(0)
    output_slots_size = Int(0)
