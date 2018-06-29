import six


class ExtensionPointID:
    """The envisage extension points ids for the factories ExtensionPoints.
    These are populated by the envisage plugins.

    The plugin developer generally does not have to handle these identifiers,
    as they just have to reimplement the plugin base class and implement
    the appropriate default methods.
    """
    MCO_FACTORIES = 'force.bdss.mco.factories'
    DATA_SOURCE_FACTORIES = 'force.bdss.data_source.factories'
    NOTIFICATION_LISTENER_FACTORIES = \
        'force.bdss.notification_listener.factories'
    UI_HOOKS_FACTORIES = 'force.bdss.ui_hooks.factories'


class InternalPluginID:
    CORE_MCO_DRIVER_ID = "force.bdss.core.CoreMCODriver"
    CORE_EVALUATION_DRIVER_ID = "force.bdss.core.CoreEvaluationDriver"
    CORE_RUN_DATASOURCE_DRIVER_ID = "force.bdss.core.CoreRunDataSourceDriver"


def factory_id(plugin_id, identifier):
    """Creates an id for the factory.

    Parameters
    ----------
    plugin_id: str
        the id of the plugin that contains this factory
    identifier: str
        A unique identifier for the factory. The identifier should be unique
        control over the uniqueness of this identifier.

    Returns
    -------
    str: an identifier to be used in the factory.
    """
    return _string_id(plugin_id, "factory", identifier)


def mco_parameter_id(mco_factory_id, parameter_identifier):
    """Creates an ID for an MCO parameter, so that it can be identified
    uniquely."""
    return _string_id(mco_factory_id, "parameter", parameter_identifier)


def plugin_id(producer, identifier, version):
    """Creates an ID for the plugins. These must be defined, otherwise
    the envisage system will complain (but not break)

    Parameters
    ----------
    producer: str
        A unique string identifying the producer (company/research institute)
        of the plugin (e.g. "enthought", "itwm")
    identifier: str
        A string identifying the plugin. It must be unique within the context
        of the producer, who is responsible to guarantee that plugin names
        are unique
    version: int
        A version number for the plugin.
    """
    if not isinstance(version, int) or version < 0:
        raise ValueError("version must be a non negative integer")

    return _string_id("force",
                      "bdss",
                      producer,
                      "plugin",
                      identifier,
                      "v{}".format(version))


def _string_id(*args):
    """Creates an id for a generic entity, by concatenating the given args
    with dots.

    Parameters
    ----------
    *args: str
        The strings to concatenate

    Returns
    -------
    str: an identifier to be used.
    """
    def is_valid(entry):
        return (
            isinstance(entry, six.string_types) and
            " " not in entry and
            len(entry) != 0)

    if not all(map(is_valid, args)):
        raise ValueError("One or more of the specified parameters was "
                         "invalid: {}".format(str(args)))

    return ".".join(list(args))
