"""jc - JSON CLI output utility pip-show Parser

Usage:

    specify --pip-show as the first argument if the piped input is coming from pip show

Compatibility:

    'linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd'

Examples:

    $ pip show wrapt jc wheel | jc --pip-show -p
    [
      {
        "name": "wrapt",
        "version": "1.11.2",
        "summary": "Module for decorators, wrappers and monkey patching.",
        "home_page": "https://github.com/GrahamDumpleton/wrapt",
        "author": "Graham Dumpleton",
        "author_email": "Graham.Dumpleton@gmail.com",
        "license": "BSD",
        "location": "/usr/local/lib/python3.7/site-packages",
        "requires": null,
        "required_by": "astroid"
      },
      {
        "name": "wheel",
        "version": "0.33.4",
        "summary": "A built-package format for Python.",
        "home_page": "https://github.com/pypa/wheel",
        "author": "Daniel Holth",
        "author_email": "dholth@fastmail.fm",
        "license": "MIT",
        "location": "/usr/local/lib/python3.7/site-packages",
        "requires": null,
        "required_by": null
      }
    ]
"""
import jc.utils


class info():
    version = '1.1'
    description = 'pip show command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    magic_commands = ['pip show', 'pip3 show']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        List of dictionaries. Structured data with the following schema:

        [
          {
            "name":             string,
            "version":          string,
            "summary":          string,
            "home_page":        string,
            "author":           string,
            "author_email":     string,
            "license":          string,
            "location":         string,
            "requires":         string,
            "required_by":      string
          }
        ]

    """
    # no further processing
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
    package = {}

    # Clear any blank lines
    cleandata = list(filter(None, data.splitlines()))

    if jc.utils.has_data(data):

        for row in cleandata:
            if row.startswith('---'):
                raw_output.append(package)
                package = {}
                continue

            item_key = row.split(': ', maxsplit=1)[0].lower().replace('-', '_')
            item_value = row.split(': ', maxsplit=1)[1]

            if item_value == '':
                item_value = None

            package.update({item_key: item_value})

        raw_output.append(package)

    if raw:
        return raw_output
    else:
        return process(raw_output)
