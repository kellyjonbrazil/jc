"""jc - JSON CLI output utility systemctl-luf Parser

Usage:

    specify --systemctl-luf as the first argument if the piped input is coming from systemctl list-unit-files

Compatibility:

    'linux'

Examples:

    $ systemctl list-unit-files | jc --systemctl-luf -p
    [
      {
        "unit_file": "proc-sys-fs-binfmt_misc.automount",
        "state": "static"
      },
      {
        "unit_file": "dev-hugepages.mount",
        "state": "static"
      },
      {
        "unit_file": "dev-mqueue.mount",
        "state": "static"
      },
      ...
    ]
"""
import jc.utils


class info():
    version = '1.1'
    description = 'systemctl list-unit-files command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['systemctl list-unit-files']


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
            "unit_file":   string,
            "state":       string
          }
        ]
    """
    # nothing more to process
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

    linedata = data.splitlines()
    # Clear any blank lines
    linedata = list(filter(None, linedata))
    # clean up non-ascii characters, if any
    cleandata = []
    for entry in linedata:
        cleandata.append(entry.encode('ascii', errors='ignore').decode())

    header_text = cleandata[0]
    header_text = header_text.lower().replace('unit file', 'unit_file')
    header_list = header_text.split()

    raw_output = []

    for entry in cleandata[1:]:
        if 'unit files listed.' in entry:
            break

        else:
            entry_list = entry.split(maxsplit=4)
            output_line = dict(zip(header_list, entry_list))
            raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return process(raw_output)
