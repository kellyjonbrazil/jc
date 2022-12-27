"""jc - JSON Convert ISO 8601 Datetime string parser

This parser has been renamed to datetime-iso (cli) or datetime_iso (module).

This parser will be removed in a future version, so please start using
the new parser name.
"""
from jc.parsers import datetime_iso
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = 'Deprecated - please use datetime-iso'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Deprecated - please use datetime-iso'
    compatible = ['linux', 'aix', 'freebsd', 'darwin', 'win32', 'cygwin']
    tags = ['standard', 'string']
    deprecated = True


__version__ = info.version


def parse(data, raw=False, quiet=False):
    """
    This parser is deprecated and calls datetime_iso. Please use datetime_iso
    directly. This parser will be removed in the future.

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    jc.utils.warning_message([
        'iso-datetime parser is deprecated. Please use datetime-iso instead.'
    ])

    return datetime_iso.parse(data, raw=raw, quiet=quiet)
