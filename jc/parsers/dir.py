"""jc - JSON CLI output utility `dir` command output parser

Options supported:
- `/T timefield`
- `/O sortorder`
- `/C, /-C`
- `/S`

The `epoch` calculated timestamp field is naive (i.e. based on the local time of the system the parser is run on)

Usage (cli):

    C:> dir | jc --dir

    or

    C:> jc dir

Usage (module):

    import jc.parsers.dir
    result = jc.parsers.dir.parse(dir_command_output)

Schema:

    [
      {
        "date":         string,
        "time":         string,
        "epoch":        integer,    # naive timestamp
        "dir":          boolean,
        "size":         integer,
        "filename:      string,
        "parent":       string
      }
    ]

Examples:

    C:> dir | jc --dir -p
    [
      {
        "date": "03/24/2021",
        "time": "03:15 PM",
        "dir": true,
        "size": null,
        "filename": ".",
        "parent": "C:\\Program Files\\Internet Explorer",
        "epoch": 1616624100
      },
      {
        "date": "03/24/2021",
        "time": "03:15 PM",
        "dir": true,
        "size": null,
        "filename": "..",
        "parent": "C:\\Program Files\\Internet Explorer",
        "epoch": 1616624100
      },
      {
        "date": "12/07/2019",
        "time": "02:49 AM",
        "dir": true,
        "size": null,
        "filename": "en-US",
        "parent": "C:\\Program Files\\Internet Explorer",
        "epoch": 1575715740
      },
      {
        "date": "12/07/2019",
        "time": "02:09 AM",
        "dir": false,
        "size": 54784,
        "filename": "ExtExport.exe",
        "parent": "C:\\Program Files\\Internet Explorer",
        "epoch": 1575713340
      },
      ...
    ]

    C:> dir | jc --dir -p -r
    [
      {
        "date": "03/24/2021",
        "time": "03:15 PM",
        "dir": true,
        "size": null,
        "filename": ".",
        "parent": "C:\\Program Files\\Internet Explorer"
      },
      {
        "date": "03/24/2021",
        "time": "03:15 PM",
        "dir": true,
        "size": null,
        "filename": "..",
        "parent": "C:\\Program Files\\Internet Explorer"
      },
      {
        "date": "12/07/2019",
        "time": "02:49 AM",
        "dir": true,
        "size": null,
        "filename": "en-US",
        "parent": "C:\\Program Files\\Internet Explorer"
      },
      {
        "date": "12/07/2019",
        "time": "02:09 AM",
        "dir": false,
        "size": "54,784",
        "filename": "ExtExport.exe",
        "parent": "C:\\Program Files\\Internet Explorer"
      },
      ...
    ]
"""
import re
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.2'
    description = '`dir` command parser'
    author = 'Rasheed Elsaleh'
    author_email = 'rasheed@rebelliondefense.com'

    # compatible options: win32
    compatible = ['win32']
    magic_commands = ['dir']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary of Lists) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
    for entry in proc_data:
        # add timestamps
        if 'date' in entry and 'time' in entry:
            dt = entry['date'] + ' ' + entry['time']
            timestamp = jc.utils.timestamp(dt)
            entry['epoch'] = timestamp.naive

        # add ints
        int_list = ["size"]
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = []

    if jc.utils.has_data(data):

        for line in data.splitlines():
            if line.startswith(" Directory of"):
                parent_dir = line.lstrip(" Directory of ")
                continue
            # skip lines that don't start with a date
            if not re.match(r'^\d{2}/\d{2}/\d{4}', line):
                continue

            output_line = {}
            parsed_line = line.split()
            output_line["date"] = parsed_line[0]
            output_line["time"] = " ".join(parsed_line[1:3])
            output_line.setdefault("dir", False)
            output_line.setdefault("size", None)
            if parsed_line[3] == "<DIR>":
                output_line["dir"] = True
            else:
                output_line["size"] = parsed_line[3]

            output_line["filename"] = " ".join(parsed_line[4:])
            output_line["parent"] = parent_dir

            raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
