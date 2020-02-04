"""jc - JSON CLI output utility yaml Parser

Usage:

    specify --yaml as the first argument if the piped input is coming from a yaml file

Compatibility:

    'linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd'

Examples:

    $ cat example.yaml | jc --yaml -p
    []

    $ cat example.yaml | jc --yaml -p -r
    []
"""
import jc.utils
from ruamel.yaml import YAML


class info():
    version = '1.0'
    description = 'yaml file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using the ruamel.yaml library at https://pypi.org/project/ruamel.yaml/'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        List of dictionaries. Each dictionary represents a YAML document:

        [
          {
            YAML Document converted to a Dictionary
            See https://pypi.org/project/ruamel.yaml for details
          }
        ]
    """

    # No further processing
    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = []

    # support multiple documents in a file
    cleandata = data.split('---')

    if cleandata:
        for document in cleandata:
            yaml = YAML(typ='safe')
            raw_output.append(yaml.load(document))

    if raw:
        return raw_output
    else:
        return process(raw_output)
