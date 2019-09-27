from logging import getLogger

logger = getLogger(__name__)


def trait_check(source, target, name, ignore_default=False):
    """Check whether attribute on source matches with the same
    attribute on target

    Parameters
    ----------
    source, target: objects
        Object instances to have attribute checked
    name: str
        Name of an attribute to check
    ignore_default: bool, optional, default: False
        Whether or not to ignore the attribute on source if it is
        equal to its default value. Note: this will not be performed
        if attribute does not have a default.
    """

    source_attr = getattr(source, name)
    target_attr = getattr(target, name)

    # If ignore_default perform a check to see whether attribute on
    # source is its default value, and skip cross check if so
    if ignore_default:
        try:
            if source_attr == source.trait(name).default:
                return True
        except AttributeError:
            pass

    # Return attribute equality check
    return target_attr == source_attr


def attr_checker(source, target, attr_checks, ignore_default=False):
    """Check whether attributes listed in `attr_checks` are equivalent on both
     source and target objects

    Parameters
    ----------
    source, target: objects
        Object instances to perform attribute checks on
    attr_checks: str or list of str
        An attribute or list of attributes to check equivalence on both
        source and target objects
    ignore_default: bool, optional, default: False
        Whether or not to ignore any attributes on source listed in
        attr_checks that are are equal to their default values

    Returns
    -------
    unequal_attr: list of str
        Names of attributes on source and target that fail an
        equality check
    """

    # Ensure attr_checks argument is in an iterable format
    if attr_checks is None:
        attr_checks = []
    elif isinstance(attr_checks, str):
        attr_checks = [attr_checks]
    else:
        attr_checks = list(attr_checks)

    failed_attr = []

    # Iterate through attr_checks list
    for attr_name in attr_checks:
        if not trait_check(source, target, attr_name, ignore_default):
            failed_attr.append(attr_name)

    return failed_attr


def sync_trait_with_check(source, target, name, attr_checks=None,
                          ignore_default=False):
    """Sync an attribute on a HasTraits object (target) with that of another
    HasTraits object (source). Performs the same function as `sync_trait`
    method, but with some extra logic checks on on selected attributes
    supplied by `attr_checks`.

    Parameters
    ----------
    source, target: HasTraits
        HasTraits instances to have an attribute synchronised
    name: str
        Name of an attribute on both source and target to be synced
    attr_checks: str or list of str, optional
        An attribute or list of attributes to check equivalence on both
        source and target objects
    ignore_default: bool, optional, default: False
        Whether or not to ignore any attributes on source listed in
        attr_checks that are are equal to their default values

    Raises
    -----
    RuntimeError, if any attribute checks fail
    """

    # Obtain names of any attributes in `attr_check` on both source and target
    # that do not match
    failed_attr = attr_checker(source, target, attr_checks,
                               ignore_default=ignore_default)

    if len(failed_attr) > 0:
        attr_name = failed_attr[0]
        error_msg = (
            "The {} attribute of source {} ({}) doesn't match the "
            "target {} ({}).".format(
                attr_name, source, getattr(source, name),
                target, getattr(target, name)
            )
        )
        logger.exception(error_msg)
        raise RuntimeError(error_msg)

    # Sync attribute `name` on target with that of source
    source.sync_trait(name, target, mutual=False)
