"""jc - JSON CLI output utility `uname -a` command output parser

Note: Must use `uname -a`

Usage (cli):

    $ uname -a | jc --uname

    or

    $ jc uname -a

Usage (module):

    import jc.parsers.uname
    result = jc.parsers.uname.parse(uname_command_output)

Schema:

    {
        "kernel_name":        string,
        "node_name":          string,
        "kernel_release":     string,
        "operating_system":   string,
        "hardware_platform":  string,
        "processor":          string,
        "machine":            string,
        "kernel_version":     string
    }

Example:

    $ uname -a | jc --uname -p
    {
      "kernel_name": "Linux",
      "node_name": "user-ubuntu",
      "kernel_release": "4.15.0-65-generic",
      "operating_system": "GNU/Linux",
      "hardware_platform": "x86_64",
      "processor": "x86_64",
      "machine": "x86_64",
      "kernel_version": "#74-Ubuntu SMP Tue Sep 17 17:06:04 UTC 2019"
    }
"""
import jc.utils
from jc.exceptions import ParseError


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.7'
    description = '`uname -a` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'freebsd']
    magic_commands = ['uname']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    # nothing to process
    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):

        # check for macOS or FreeBSD output
        if data.startswith('Darwin') or data.startswith('FreeBSD'):
            parsed_line = data.split()

            if len(parsed_line) < 5:
                raise ParseError('Could not parse uname output. Make sure to use "uname -a".')

            raw_output['machine'] = parsed_line.pop(-1)
            raw_output['kernel_name'] = parsed_line.pop(0)
            raw_output['node_name'] = parsed_line.pop(0)
            raw_output['kernel_release'] = parsed_line.pop(0)
            raw_output['kernel_version'] = ' '.join(parsed_line)

        # otherwise use linux parser
        else:
            # fixup for cases where 'machine' exists but 'processor' and 'hardware_platform' fields are blank.
            # if the fields exist then at least two of the three will be the same.
            # if the fields do not exist then none of the fields in those positions will be the same.
            # case of only two existing is undefined. Must either be one or all three existing, otherwise
            # there will be unexpected results during parsing.
            fixup = data.split()
            if len(fixup) >= 4:
                fixup_set = set([fixup[-2], fixup[-3], fixup[-4]])
                if len(fixup_set) > 2:
                    fixup.insert(-1, 'unknown')
                    fixup.insert(-1, 'unknown')
                    data = ' '.join(fixup)
            
            parsed_line = data.split(maxsplit=3)

            if len(parsed_line) < 3:
                raise ParseError('Could not parse uname output. Make sure to use "uname -a".')

            raw_output['kernel_name'] = parsed_line.pop(0)
            raw_output['node_name'] = parsed_line.pop(0)
            raw_output['kernel_release'] = parsed_line.pop(0)

            parsed_line = parsed_line[-1].rsplit(maxsplit=4)

            raw_output['operating_system'] = parsed_line.pop(-1)
            raw_output['processor'] = parsed_line.pop(-1)
            raw_output['hardware_platform'] = parsed_line.pop(-1)
            raw_output['machine'] = parsed_line.pop(-1)

            raw_output['kernel_version'] = parsed_line.pop(0)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
