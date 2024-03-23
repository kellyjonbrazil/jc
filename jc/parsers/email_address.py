r"""jc - JSON Convert Email Address string parser

Usage (cli):

    $ echo "username@example.com" | jc --email-address

Usage (module):

    import jc
    result = jc.parse('email_address', email_address_string)

Schema:

    {
      "username":             string,
      "domain":               string,
      "local":                string,
      "local_plus_suffix":    string or null
    }

Examples:

    $ echo 'joe.user@gmail.com' | jc --email-address -p
    {
      "username": "joe.user",
      "domain": "gmail.com",
      "local": "joe.user",
      "local_plus_suffix": null
    }

    $ echo 'joe.user+spam@gmail.com' | jc --email-address -p
    {
      "username": "joe.user",
      "domain": "gmail.com",
      "local": "joe.user+spam",
      "local_plus_suffix": "spam"
    }
"""
from typing import Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = 'Email Address string parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'string', 'slurpable']


__version__ = info.version


def _process(proc_data: Dict) -> Dict:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> Dict:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: Dict = {}

    if jc.utils.has_data(data):
        data = data.strip()
        domain = data.rsplit('@', maxsplit=1)[1]
        local = data.rsplit('@', maxsplit=1)[0]

        local_plus_prefix = None
        local_plus_suffix = None
        try:
            local_plus_suffix = local.split('+', maxsplit=1)[1]
            local_plus_prefix = local.split('+', maxsplit=1)[0]
        except IndexError:
            pass

        raw_output = {
            'username': local_plus_prefix or local,
            'domain': domain,
            'local': local,
            'local_plus_suffix': local_plus_suffix
        }

    return raw_output if raw else _process(raw_output)
