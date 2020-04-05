"""jc - JSON CLI output utility systemctl-lj Parser

Usage:

    specify --systemctl-lj as the first argument if the piped input is coming from systemctl list-jobs

Compatibility:

    'linux'

Examples:

    $ systemctl list-jobs| jc --systemctl-lj -p
    [
      {
        "job": 3543,
        "unit": "nginxAfterGlusterfs.service",
        "type": "start",
        "state": "waiting"
      },
      {
        "job": 3545,
        "unit": "glusterReadyForLocalhostMount.service",
        "type": "start",
        "state": "running"
      },
      {
        "job": 3506,
        "unit": "nginx.service",
        "type": "start",
        "state": "waiting"
      }
    ]

    $ systemctl list-jobs| jc --systemctl-lj -p -r
    [
      {
        "job": "3543",
        "unit": "nginxAfterGlusterfs.service",
        "type": "start",
        "state": "waiting"
      },
      {
        "job": "3545",
        "unit": "glusterReadyForLocalhostMount.service",
        "type": "start",
        "state": "running"
      },
      {
        "job": "3506",
        "unit": "nginx.service",
        "type": "start",
        "state": "waiting"
      }
    ]

"""
import jc.utils


class info():
    version = '1.1'
    description = 'systemctl list-jobs command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['systemctl list-jobs']


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
            "job":      integer,
            "unit":     string,
            "type":     string,
            "state":    string
          }
        ]
    """
    for entry in proc_data:
        int_list = ['job']
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

    linedata = data.splitlines()
    # Clear any blank lines
    linedata = list(filter(None, linedata))
    # clean up non-ascii characters, if any
    cleandata = []
    for entry in linedata:
        cleandata.append(entry.encode('ascii', errors='ignore').decode())

    header_text = cleandata[0]
    header_text = header_text.lower()
    header_list = header_text.split()

    raw_output = []

    for entry in cleandata[1:]:
        if 'No jobs running.' in entry or 'jobs listed.' in entry:
            break

        else:
            entry_list = entry.split(maxsplit=4)
            output_line = dict(zip(header_list, entry_list))
            raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return process(raw_output)
