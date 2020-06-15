"""jc - JSON CLI output utility jobs Parser

Usage:

    specify --jobs as the first argument if the piped input is coming from jobs

    Also supports the -l option

Compatibility:

    'linux', 'darwin', 'cygwin', 'aix', 'freebsd'

Example:

    $ jobs -l | jc --jobs -p
    [
      {
        "job_number": 1,
        "pid": 5283,
        "status": "Running",
        "command": "sleep 10000 &"
      },
      {
        "job_number": 2,
        "pid": 5284,
        "status": "Running",
        "command": "sleep 10100 &"
      },
      {
        "job_number": 3,
        "pid": 5285,
        "history": "previous",
        "status": "Running",
        "command": "sleep 10001 &"
      },
      {
        "job_number": 4,
        "pid": 5286,
        "history": "current",
        "status": "Running",
        "command": "sleep 10112 &"
      }
    ]

    $ jobs -l | jc --jobs -p -r
    [
      {
        "job_number": "1",
        "pid": "19510",
        "status": "Running",
        "command": "sleep 1000 &"
      },
      {
        "job_number": "2",
        "pid": "19511",
        "status": "Running",
        "command": "sleep 1001 &"
      },
      {
        "job_number": "3",
        "pid": "19512",
        "history": "previous",
        "status": "Running",
        "command": "sleep 1002 &"
      },
      {
        "job_number": "4",
        "pid": "19513",
        "history": "current",
        "status": "Running",
        "command": "sleep 1003 &"
      }
    ]
"""
import string
import jc.utils


class info():
    version = '1.2'
    description = 'jobs command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']
    magic_commands = ['jobs']


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
            "job_number":   integer,
            "pid":          integer,
            "history":      string,
            "status":       string,
            "command":      string
          }
        ]
    """
    for entry in proc_data:
        int_list = ['job_number', 'pid']
        for key in int_list:
            if key in entry:
                try:
                    key_int = int(entry[key])
                    entry[key] = key_int
                except (ValueError):
                    entry[key] = None

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

    # Clear any blank lines
    cleandata = list(filter(None, data.splitlines()))

    if jc.utils.has_data(data):

        for entry in cleandata:
            output_line = {}
            remainder = []
            job_number = ''
            pid = ''
            job_history = ''

            parsed_line = entry.split(maxsplit=2)

            # check if -l was used
            if parsed_line[1][0] in string.digits:
                pid = parsed_line.pop(1)
                remainder = parsed_line.pop(1)
                job_number = parsed_line.pop(0)
                remainder = remainder.split(maxsplit=1)

                # rebuild parsed_line
                parsed_line = []

                for r in remainder:
                    parsed_line.append(r)

                parsed_line.insert(0, job_number)

            # check for + or - in first field
            if '+' in parsed_line[0]:
                job_history = 'current'
                parsed_line[0] = parsed_line[0].rstrip('+')

            if '-' in parsed_line[0]:
                job_history = 'previous'
                parsed_line[0] = parsed_line[0].rstrip('-')

            # clean up first field
            parsed_line[0] = parsed_line[0].lstrip('[').rstrip(']')

            # create list of dictionaries
            output_line['job_number'] = parsed_line[0]
            if pid:
                output_line['pid'] = pid
            if job_history:
                output_line['history'] = job_history
            output_line['status'] = parsed_line[1]
            output_line['command'] = parsed_line[2]

            raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return process(raw_output)
